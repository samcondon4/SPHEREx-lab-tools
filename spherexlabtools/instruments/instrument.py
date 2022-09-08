"""instrument:

    This module contains the original instrument base class :class:`.PylabInstrument`, as well as the class
    :class:`.CompoundInstrument`, which inherits from the pymeasure base instrument class. Work is ongoing to deprecate
    the use of :class:`.PylabInstrument`.

Sam Condon, 06/30/2021
"""
import logging
import importlib
from pymeasure.instruments.instrument import DynamicProperty
import spherexlabtools.log as slt_log


log_name = f"{slt_log.LOGGER_NAME}.{__name__.split('.')[-1]}"
logger = logging.getLogger(log_name)


def instantiate_instrument(inst_dict, exp, dev_links=None):
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

    manufacturer_string = inst_dict["manufacturer"]

    # first try to instantiate the instrument from the local instruments folder, then from spherexlabtools, then
    # from pymeasure.
    try:  # - local instruments module - #
        inst_mod = getattr(exp.instruments, manufacturer_string)
        inst_class = getattr(inst_mod, inst_dict["instrument"])
    except (AttributeError, ModuleNotFoundError):
        try:  # - spherexlabtools - #
            inst_mod = importlib.import_module(name="spherexlabtools.instruments.%s" % manufacturer_string)
            inst_class = getattr(inst_mod, inst_dict["instrument"])
        except (AttributeError, ModuleNotFoundError):
            try:  # - pymeasure - #
                inst_mod = importlib.import_module(name="pymeasure.instruments.%s" % manufacturer_string)
                inst_class = getattr(inst_mod, inst_dict["instrument"])
            except (AttributeError, ModuleNotFoundError):
                # - if the instrument driver class is still not found, then throw the error - #
                err_msg = "No instrument driver found for %s.%s" % (manufacturer_string, inst_dict["instrument"])
                #logger.error(err_msg)
                raise AttributeError("No instrument driver found for %s.%s" % (manufacturer_string,
                                                                               inst_dict["instrument"]))

    logger.info(slt_log.INIT_MSG % inst_dict["instance_name"])
    # instantiate the instrument class with key-word arguments #
    if "kwargs" in inst_dict:
        kwargs = inst_dict["kwargs"]
    else:
        kwargs = {}
    try:
        rec_name = inst_dict["resource_name"]
        if type(dev_links) is dict and rec_name.__hash__ is not None and rec_name in dev_links.keys():
            rec_name = dev_links[rec_name]
        inst = inst_class(rec_name, **kwargs)
    except Exception as e:
        #logger.error("Error while instantiating {}.{}: \n {}".format(manufacturer_string, inst_dict["instrument"],
                                                                     #e))
        raise e

    # set initial instrument parameters if any are given #
    if "params" in inst_dict:
        for param, param_val in inst_dict["params"].items():
            setattr(inst, param, param_val)
        logger.info(slt_log.CMPLT_MSG % f"{inst_dict['instance_name']} initialization")

    # - set the instrument name - #
    inst.name = inst_dict["instance_name"]
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

    def __init__(self, cfg, exp, dev_links=None):
        """
        :param: cfg: :ref:`Compound Instrument Dictionary` specifying subinstruments and optional property
                     configurations.
        """
        assert "subinstruments" in cfg.keys(), "Subinstruments must be specified!"
        self.subinstruments = {}
        # instantiate all subinstruments
        for inst_dict in cfg["subinstruments"]:
            self.subinstruments[inst_dict["instance_name"]] = instantiate_instrument(inst_dict, exp, dev_links=dev_links)

        # perform the initial property merge
        for inst_key, subinst in self.subinstruments.items():
            self.merge_subinst_clsattrs(subinst, inst_key, recursive=True)

        # apply the property configuration, if one is present
        if "property_config" in cfg.keys():
            for prop_cfg in cfg["property_config"]:
                prop_name, fget, fset = prop_cfg
                self.__dict__[prop_name] = property(self.__dict__[fget].fget, self.__dict__[fset].fset)
                #self.__dict__.pop(fget)
                #self.__dict__.pop(fset)
                self.property_map[prop_name] = {"fget": fget.split("_")[0], "fset": fset.split("_")[0]}

        # apply the attribute configuration, if one is present
        if "attr_config" in cfg.keys():
            for attr_cnfg in cfg["attr_config"]:
                attr_name, attr = attr_cnfg
                self.__dict__[attr_name] = attr
                self.attrs.append(attr_name)

    def merge_subinst_clsattrs(self, subinst, name, recursive=False):
        """ Merge all subinstrument class attributes into the instance's namespace.

        :param subinst: Instrument object to get properties from.
        :param name: String identifying the subinstrument.
        :param recursive: Recursively merge all subinstrument properties including those within baseclasses
                           until the base :class:`.Instrument` class is reached.
        """
        class_attrs = dir(subinst.__class__)
        for cls_attr_str in class_attrs:
            if not cls_attr_str.startswith("_"):
                cls_attr = getattr(subinst.__class__, cls_attr_str)
                attr_name = f"{name}_{cls_attr_str}"
                if attr_name not in self.__dict__.keys():
                    self.__dict__[attr_name] = cls_attr

                cls_attr_typ = type(cls_attr)
                if cls_attr_typ is property or cls_attr_typ is DynamicProperty:
                    self.property_map[attr_name] = {"fget": name, "fset": name}
                else:
                    self.method_map[attr_name] = name

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

    def __init__(self, inst_cfg, exp, dev_links=None):
        for inst in inst_cfg:
            if "subinstruments" not in inst:
                self.__dict__[inst["instance_name"]] = instantiate_instrument(inst, exp, dev_links=dev_links)
            else:
                self.__dict__[inst["instance_name"]] = CompoundInstrument(inst, exp, dev_links=dev_links)

