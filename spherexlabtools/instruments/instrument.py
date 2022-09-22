"""instrument:

    This module contains the classes :class:`.CompoundInstrument` and :class:`.InstrumentSuite`
"""
import logging
import importlib
import spherexlabtools.log as slt_log
from pymeasure.instruments.instrument import DynamicProperty

log_name = f"{slt_log.LOGGER_NAME}.{__name__.split('.')[-1]}"
logger = logging.getLogger(log_name)


def instantiate_instrument(inst_dict, exp, dev_links=None, **instance_kwargs):
    """ Instantiate and return the appropriate PyMeasure Instrument class based on the inst_dict arguments.
    :param: inst_dict: dictionary corresponding to a single instrument. This dictionary should take the form seen at
                       :ref:`Instrument Dictionaries`
    """
    instance_kwargs.update({"exp": exp})

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
                logger.error(err_msg)
                raise AttributeError("No instrument driver found for %s.%s" % (manufacturer_string,
                                                                               inst_dict["instrument"]))

    logger.info(slt_log.INIT_MSG % inst_dict["instance_name"])
    # instantiate the instrument class with key-word arguments #
    if "kwargs" in inst_dict:
        instance_kwargs.update(inst_dict["kwargs"])
    try:
        rec_name = inst_dict["resource_name"]
        if type(dev_links) is dict and rec_name.__hash__ is not None and rec_name in dev_links.keys():
            rec_name = dev_links[rec_name]
        inst = inst_class(rec_name, **instance_kwargs)
    except Exception as e:
        logger.error("Error while instantiating {}.{}: \n {}".format(manufacturer_string, inst_dict["instrument"],
                                                                     e))
        raise e

    # set initial instrument parameters if any are given #
    if "params" in inst_dict:
        for param, param_val in inst_dict["params"].items():
            setattr(inst, param, param_val)
        logger.info(slt_log.CMPLT_MSG % f"{inst_dict['instance_name']} initialization")

    # - set the instrument name - #
    inst.name = inst_dict["instance_name"]
    return inst


class MergeInstrumentMetaclass(type):

    def __new__(mcs, clsname, bases, attrs, instruments, *args, **kwargs):
        # - add the instrument dictionary to returned class attributes - #
        attrs.update({"instruments": instruments})

        # - merge all class attributes of all instances - #
        for instKey, instClass in instruments.items():
            inst_class_attrs = [
                (iattr, getattr(instClass, iattr)) for iattr in dir(instClass) if not
                (iattr.startswith("__") and iattr.endswith("__"))
            ]
            new_attrs = {
                "_".join([instKey, new_attr[0]]): new_attr[1] for new_attr in inst_class_attrs
            }
            attrs.update(new_attrs)

        # - create the new __init__ method - #
        init_func = attrs.get("__init__", None)
        attrs.update({
            "__init__": mcs.get_init(mcs, init_func)
        })
        return super().__new__(mcs, clsname, bases, attrs)

    def instantiate_instruments(self, *args, **kwargs):
        assert "sub_instruments" in kwargs, "Merged instruments must have 'sub_instruments' passed as a kwarg!"
        subinstruments = kwargs["sub_instruments"]
        for cfg_dict in subinstruments:
            self.instruments[cfg_dict["instance_name"]] = instantiate_instrument(cfg_dict, **kwargs)

    def get_init(cls, init=None):

        def __init(self, *args, obj_init=init, **kwargs):
            cls.instantiate_instruments(self, *args, **kwargs)
            if obj_init is not None:
                obj_init(self, *args, **kwargs)

        return __init


class CompoundInstrument:
    """ Dynamic class that merges two or more Instruments into a single object.
    """

    def __init__(self, resource_name, merge_instances=None, dev_links=None):
        # - get all class attributes from passed in instrument instances - #
        cls_attrs = []
        for instance in merge_instances:
            cls = instance.__class__
            attr_name_str = instance.name + "_%s"
            attrs = [(attr_name_str % attr, getattr(cls, attr)) for attr in dir(cls) if not (attr.startswith("__") and
                                                                                             attr.endswith("__"))]
            cls_attrs.extend(attrs)

        # - merge all class attributes retrieved above - #
        for attr_tup in cls_attrs:
            setattr(self.__class__, attr_tup[0], attr_tup[1])


class InstrumentSuite:
    """ Top-level instrument object to encapsulate all instruments within an experiment.
    """

    def __init__(self, inst_cfg, exp, dev_links=None):
        for inst in inst_cfg:
            if "subinstruments" not in inst:
                self.__dict__[inst["instance_name"]] = instantiate_instrument(inst, exp, dev_links=dev_links)
            elif "manufacturer" in inst and "instrument" in inst:
                merge_instances = [instantiate_instrument(cfg, exp, dev_links=dev_links) for cfg in
                                   inst["subinstruments"]]
                self.__dict__[inst["instance_name"]] = instantiate_instrument(inst, exp, dev_links=dev_links,
                                                                              merge_instances=merge_instances)
            else:
                merge_instances = [instantiate_instrument(cfg, exp, dev_links=dev_links) for cfg in
                                   inst["subinstruments"]]
                self.__dict__[inst["instance_name"]] = CompoundInstrument(inst, exp, merge_instances)
