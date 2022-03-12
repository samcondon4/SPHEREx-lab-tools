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

