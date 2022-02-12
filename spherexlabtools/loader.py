""" Module supporting dynamic loading of class instances. Implements the functions:

        :func:`.load_objects_from_cfg_list`
"""
import logging
import importlib


logger = logging.getLogger(__name__)


class LoaderError(Exception):
    """ Exception raised when a class definition for an instance cannot be found.
    """
    pass


def load_objects_from_cfg_list(search_order, cfg_list, **kwargs):
    """ Load a set of object instances from a list of configs with a specific module search order.

    :param search_order: List of module objects to search for class definitions.
    :param cfg_list: List of instance configuration dictionaries. These dictionaries must have at least
                     an 'instance_name' and 'type' key-value pair.
    :param kwargs: Key-word arguments passed to the class instantiation.
    """
    objects = {}
    for cfg in cfg_list:
        name = cfg["instance_name"]
        typ = cfg["type"]
        inst_class = None
        for mod in search_order:
            try:
                inst_class = getattr(mod, typ)
            except AttributeError:
                pass
            else:
                logger.info("Initializing %s as %s" % (cfg["instance_name"], inst_class))
                objects[name] = inst_class(cfg, **kwargs)

        # if all modules searched and class def not found, raise and log error.
        if inst_class is None:
            err_msg = "Could not find type %s for instance %s" % (cfg["type"], cfg["instance_name"])
            logger.error(err_msg)
            raise LoaderError(err_msg)

    return objects

