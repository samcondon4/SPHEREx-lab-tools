"""instrument:

    This module contains the original instrument base class :class:`.PylabInstrument`, as well as the class
    :class:`.CompoundInstrument`, which inherits from the pymeasure base instrument class. Work is ongoing to deprecate
    the use of :class:`.PylabInstrument`.

Sam Condon, 06/30/2021
"""
import logging
import asyncio
import importlib
from pymeasure.instruments import Instrument
from pymeasure.instruments.instrument import DynamicProperty


logger = logging.getLogger(__name__)


class PymeasureInstrumentSub(Instrument):
    """ Basic Pymeasure Instrument subclass to add the quick_properties attributes.
    """
    def __init__(self, adapter, name, includeSCPI=True, **kwargs):
        super().__init__(adapter, name, includeSCPI, **kwargs)

    @property
    def quick_properties_list(self):
        return self.quick_props_list

    @quick_properties_list.setter
    def quick_properties_list(self, prop_list):
        if type(prop_list) is str:
            self.quick_props_list = [prop_list]
        elif type(prop_list) is list:
            self.quick_props_list = prop_list
        else:
            raise TypeError("Expected input of type str or list")

    @property
    def quick_properties(self):
        prop_dict = {}
        for prop_name in self.quick_props_list:
            prop_dict[prop_name] = getattr(self, prop_name)

        return prop_dict

    @quick_properties.setter
    def quick_properties(self, setter_dict):
        for key in setter_dict:
            if key in self.quick_props_list:
                setattr(self, key, setter_dict[key])
            else:
                raise RuntimeError("Property {} has not been placed in the quick properties list!".format(key))


class PylabInstrument:

    def __init__(self, identifier=None):
        self.open_method = None
        self.identifier = identifier
        self.parameters = []
        self.get_methods = {}
        self.get_method_coros = {}
        self.getter_proc = None
        self.set_methods = {}
        self.set_method_coros = {}
        self.top_setter = None

    def set_top_setter(self, top_setter):
        self.top_setter = top_setter

    def set_getter_proc(self, getter_proc):
        self.getter_proc = getter_proc

    def set_open_method(self, open_method):
        """set_open_method: set the open communication interface method

        :param open_method: function pointer that can be called to open
                            the communication interface
        :return:
        """
        self.open_method = open_method

    async def open(self):
        """open: open the communication interface by calling the previously set open_method()

        :return: communication interface object
        """
        if asyncio.iscoroutinefunction(self.open_method):
            ret = await self.open_method()
        else:
            ret = self.open_method()
        return ret

    def add_parameter(self, parameter_name, getter, setter, coro=False):
        """add_parameter: add functions to the getter and setter dictionaries for the specified parameter name.

        :param parameter_name: <string> name of parameter to be added.
        :param getter: <function object> function object corresponding to parameter getter.
        :param setter: <function object> function object corresponding to parameter setter.
        :return: None
        """
        if not coro:
            self.get_methods[parameter_name] = getter
            self.set_methods[parameter_name] = setter
        else:
            self.get_method_coros[parameter_name] = getter
            self.set_method_coros[parameter_name] = setter

        if parameter_name not in self.parameters:
            self.parameters.append(parameter_name)

    def add_get_parameter(self, parameter_name, getter, coro=False):
        """add_get_parameter: add function to the getter dictionary for the specified parameter name.

        :param parameter_name: <string> name of parameter to be added.
        :param getter: <function> function object corresponding to parameter getter.
        :return: None
        """
        if not coro:
            self.get_methods[parameter_name] = getter
        else:
            self.get_method_coros[parameter_name] = getter

        if parameter_name not in self.parameters:
            self.parameters.append(parameter_name)

    def add_set_parameter(self, parameter_name, setter, coro=False):
        """add_set_parameter: add function to the setter dictionary for the specified parameter name.

        :param parameter_name: <string> name of parameter to be added.
        :param setter: <function> function object corresponding to parameter setter.
        :return: None
        """
        if not coro:
            self.set_methods[parameter_name] = setter
        else:
            self.set_method_coros[parameter_name] = setter

        if parameter_name not in self.parameters:
            self.parameters.append(parameter_name)

    async def get_parameters(self, params):
        """get_parameters: return the specified instrument parameters as a dictionary

        :param params: string, list of strings, or "All" to specify which parameters
                       to query.
        :return: parameters dictionary
        """
        coro_list = {}
        return_dict = {}
        if params == 'All':
            for getter in self.get_methods:
                return_dict[getter] = self.get_methods[getter]()
            for getter in self.get_method_coros:
                coro_list[getter] = self.get_method_coros[getter]

        elif type(params) is list:
            for getter in params:
                if getter in self.get_methods:
                    return_dict[getter] = self.get_methods[getter]()
                elif getter in self.get_method_coros:
                    coro_list[getter] = self.get_method_coros[getter]
                else:
                    raise RuntimeError("Getter {} not found!".format(getter))

        elif type(params) is str:
            if params in self.get_methods:
                return_dict[params] = self.get_methods[params]()
            elif params in self.get_method_coros:
                coro_list[params] = self.get_method_coros[params]

        # Execute all getter coroutines ####
        for key in coro_list:
            get_task = asyncio.create_task(coro_list[key]())
            await get_task
            return_dict[key] = get_task.result()

        if self.getter_proc is not None:
            return_dict = self.getter_proc(return_dict)
        return return_dict

    async def set_parameters(self, params_dict):
        """set_params: set the specified parameters in the dialog display.

        :param params_dict: dictionary with keys and values of parameters to update
        :return: None
        """
        if self.top_setter is not None:
            if asyncio.iscoroutinefunction(self.top_setter):
                params_dict = await self.top_setter(params_dict)
            else:
                params_dict = self.top_setter(params_dict)
        else:
            coro_list = []
            func_list = []
            # Separate setters into coroutines and normal functions ######################
            for p in params_dict:
                if p in self.set_method_coros:
                    task = asyncio.create_task(self.set_method_coros[p](params_dict[p]))
                    coro_list.append(task)
                elif p in self.set_methods:
                    func_list.append((self.set_methods[p], params_dict[p]))
            ##############################################################################

            # Execute coroutines ###############################
            if len(coro_list) > 0:
                done, pending = await asyncio.wait(coro_list)
            ####################################################

            # Execute functions ################################
            # The above loop created a list of tuples of the format: (<function pointer>, <function parameters>)
            for func in func_list:
                func[0](func[1])
            ####################################################

    def start_measurement(self, *args, **kwargs):
        """Description: some instruments can read and return data. This method should be overridden by such instruments

        :return:
        """
        raise RuntimeError("start_measurement has not been overridden by a suitable measurement function.")

    def get_identifier(self):
        """get_identifier: get the instrument identifier string.

        :return: <string> instrument id
        """
        return self.identifier

    def set_identifier(self, new_id):
        """set_identifier: set the instrument identifier string.

        :param new_id: <string> instrument id
        :return: None
        """
        self.identifier = new_id


def instantiate_instrument(inst_dict):
    """ Instantiate and return the appropriate PyMeasure Instrument class based on the inst_dict arguments.
    :param: inst_dict: dictionary corresponding to a single instrument. This dictionary should take the form seen at
                       :ref:`Instrument Dictionaries`
    """
    # check that the instrument dictionary contains valid arguments #
    assert "instance_name" in inst_dict, "Missing required argument 'instance_name' in instrument dictionary!"
    assert "manufacturer" in inst_dict, "Missing required argument 'manufacturer' in instrument dictionary!"
    assert "instrument" in inst_dict, "Missing required argument 'instrument' in instrument dictionary!"
    assert "resource_name" in inst_dict, "Missing required argument 'resource_name' in instrument dictionary!"
    assert not ("include_attrs" in inst_dict and "exclude_attrs" in inst_dict), \
        "Only one of {'include_attrs', 'exclude_attrs'} is allowed in an instrument dictionary!"

    # get the instrument module and class #
    if inst_dict["manufacturer"] != "":
        manufacturer_string = ".%s" % inst_dict["manufacturer"]
    else:
        manufacturer_string = ""

    # try to instantiate the instrument from pymeasure. If it is not found, then try to instantiate from
    # the local instruments folder
    try:
        inst_mod = importlib.import_module(name="pymeasure.instruments%s" % manufacturer_string)
        inst_class = getattr(inst_mod, inst_dict["instrument"])
    except (AttributeError, ModuleNotFoundError):
        try:
            inst_mod = importlib.import_module(name="spherexlabtools.instruments%s" % manufacturer_string)
            inst_class = getattr(inst_mod, inst_dict["instrument"])
        except (AttributeError, ModuleNotFoundError):
            err_msg = "No instrument driver found for %s.%s" % (manufacturer_string, inst_dict["instrument"])
            logger.error(err_msg)
            raise AttributeError("No instrument driver found for %s.%s" % (manufacturer_string,
                                                                           inst_dict["instrument"]))

    # instantiate the instrument class with key-word arguments #
    if "kwargs" in inst_dict:
        kwargs = inst_dict["kwargs"]
    else:
        kwargs = {}
    try:
        inst = inst_class(inst_dict["resource_name"], **kwargs)
    except Exception as e:
        logger.error("Error while instantiating {}.{}: \n {}".format(manufacturer_string, inst_dict["instrument"],
                                                                     e))
        raise e

    # set initial instrument parameters if any are given #
    if "params" in inst_dict:
        for p in inst_dict["params"]:
            setattr(inst, p, inst_dict["params"][p])

    # remove undesired attributes specified by include/exclude attrs #
    if "include_attrs" in inst_dict:
        for attr in dir(inst):
            if not attr.startswith("_") and attr not in dir(Instrument) and attr not in inst_dict["include_attrs"]:
                delattr(inst, attr)
    elif "exclude_attrs" in inst_dict:
        for attr in inst_dict["exclude_attrs"]:
            delattr(inst, attr)

    return inst


class CompoundInstrument:
    """ Dynamic class that merges two or more Instruments into a single object. CompoundInstruments are instantiated
        with a :ref:`Compound Instrument Dictionary`. See LINK TO TUTORIAL for an example of creating and using
        CompoundInstrument instances in a procedure.
    """

    subinstruments = {}
    property_map = {}
    method_map = {}
    attrs = []

    def __init__(self, cfg):
        """
        :param: cfg: :ref:`Compound Instrument Dictionary` specifying subinstruments and optional property
                     configurations.
        """
        assert "subinstruments" in cfg.keys(), "Subinstruments must be specified!"
        self.subinstruments = {}
        # instantiate all subinstruments
        for inst_dict in cfg["subinstruments"]:
            self.subinstruments[inst_dict["instance_name"]] = instantiate_instrument(inst_dict)

        # perform the initial property merge
        for inst_key in self.subinstruments.keys():
            subinst = self.subinstruments[inst_key]
            self.merge_subinst_clsattrs(subinst, inst_key, recursive=True)

        # apply the property configuration, if one is present
        if "property_config" in cfg.keys():
            for prop_cfg in cfg["property_config"]:
                prop_name, fget, fset = prop_cfg
                self.__dict__[prop_name] = property(self.__dict__[fget].fget, self.__dict__[fset].fset)
                self.__dict__.pop(fget)
                self.__dict__.pop(fset)
                self.property_map[prop_name] = {"fget": fget.split("_")[0], "fset": fset.split("_")[0]}

        # apply the attribute configuration, if one is present
        if "attr_config" in cfg.keys():
            for attr_cnfg in cfg["attr_config"]:
                attr_name, attr = attr_cnfg
                self.__dict__[attr_name] = attr
                self.attrs.append(attr_name)

    def merge_subinst_clsattrs(self, subinst, name, recursive=False):
        """ Merge all subinstrument class attributes into the instance's namespace.

            :param: subinst: Instrument object to get properties from.
            :param: name: String identifying the subinstrument.
            :param: recursive: Recursively merge all subinstrument properties including those within baseclasses
                               until the base :class:`.Instrument` class is reached.
        """
        attr_access = lambda sinst: sinst.__class__ if type(sinst) is not type else sinst
        if "pymeasure.instruments.instrument.Instrument" not in str(subinst) and subinst.__module__ != "builtins":
            merge_cls = attr_access(subinst)
            for cls_attr in merge_cls.__dict__:
                attr = merge_cls.__dict__[cls_attr]
                if not cls_attr.startswith("_"):
                    prop_name = "%s_%s" % (name, cls_attr)
                    # place class attribute in instance namespace if it is not already there. #
                    # This check preserves subclass attribute overrides #
                    if prop_name not in self.__dict__.keys():
                        self.__dict__[prop_name] = attr
                    # write attribute into the appropriate mapping based on its type #
                    attr_typ = type(attr)
                    if (attr_typ is property) or (attr_typ is DynamicProperty):
                        self.property_map[prop_name] = {"fget": name, "fset": name}
                    else:
                        self.method_map[prop_name] = name
        else:
            recursive = False

        if recursive:
            self.merge_subinst_clsattrs(subinst.__class__.__bases__[0], name, recursive=True)

    def shutdown(self):
        """ Shutdown all subinstruments
        """
        for subinst in self.subinstruments.values():
            subinst.shutdown()

    def __getattribute__(self, name):
        """ Override to call the fget method when the attribute being accessed is a property.
        """
        attr = object.__getattribute__(self, name)
        attr_typ = type(attr)
        if (attr_typ is property) or (attr_typ is DynamicProperty):
            subinst_key = self.property_map[name]["fget"]
            val = attr.fget(self.subinstruments[subinst_key])
        elif "function" in str(attr_typ) and name in self.method_map:
            subinst_key = self.method_map[name]
            val = lambda *args, s=self.subinstruments[subinst_key], **kwargs: attr(s, *args, **kwargs)
        elif "function" in str(attr_typ) and name in self.attrs:
            val = lambda *args, s=self, **kwargs: attr(s, *args, **kwargs)
        else:
            val = attr
        return val

    def __setattr__(self, name, value):
        """ Override the call to the fset method when an attribute being set is a property.
        """
        attr = object.__getattribute__(self, name)
        attr_typ = type(attr)
        if (attr_typ is property) or (attr_typ is DynamicProperty):
            subinst_key = self.property_map[name]["fset"]
            attr.fset(self.subinstruments[subinst_key], value)
        else:
            object.__setattr__(self, name, value)


class InstrumentSuite:
    """ Top-level instrument object to encapsulate all instruments within an experiment.
    """

    def __init__(self, inst_cfg):
        for inst in inst_cfg:
            if "subinstruments" not in inst:
                self.__dict__[inst["instance_name"]] = instantiate_instrument(inst)
            else:
                self.__dict__[inst["instance_name"]] = CompoundInstrument(inst)


def create_instrument_suite(exp_pkg):
    """ Instantiate an InstrumentSuite object.

    :param exp_pkg: User experiment configuration package.
    """
    inst_cfg = exp_pkg.INSTRUMENT_SUITE
    return InstrumentSuite(inst_cfg)

