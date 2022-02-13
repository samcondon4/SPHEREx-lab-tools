import logging
import importlib

import numpy as np
import pandas as pd
from ..thread import QueueThread


logger = logging.getLogger(__name__)


class HDF5Recorder(QueueThread):
    """ Base recorder class.
    """

    META_GROUP = "Meta"
    PARAMS_GROUP = "Params"

    def __init__(self, cfg, **kwargs):
        """ Initialize a recorder.
        """
        super().__init__(**kwargs)
        self.filename = cfg["filename"]
        self.store = pd.HDFStore(self.filename)
        # if this is a new hdf file, with no Meta group, add the group #
        if self.META_GROUP not in self.store.keys():
            meta_series = pd.Series({"Records": 0})
            self.store.put(self.META_GROUP, meta_series)
            self.records = 0
        else:
            self.records = self.store.get(self.META_GROUP)

        self.record_group_ind = None
        self.record_group_size = None

    def handle(self, record):
        """ HDF5 recorder handle.
        """
        kwargs = record.handle
        if "group" not in kwargs:
            err_msg = "required group argument not provided to the HDF5Recorder!"
            logger.error(err_msg)
            assert ValueError("The group argument is required for the HDF5Recorder!")
        group = kwargs.pop("group")

        # update record number and write this new value to the global meta-data group
        write_params = False
        if "group_records" in kwargs:
            self.record_group_size = kwargs.pop("group_records")
            if self.record_group_ind is None or not self.record_group_ind < self.record_group_size:
                write_params = True
                self.records += 1
                self.record_group_ind = 0
            else:
                self.record_group_ind += 1
        else:
            write_params = True
            self.records += 1
        self.store.put(self.META_GROUP, pd.Series({"Records": self.records}))

        # write record parameters if they are provided #
        params = record.params
        if params is not None and write_params:
            index = pd.Index([self.records], name="Record")
            param_df = pd.DataFrame(params, index=index)
            self.store.append(self.PARAMS_GROUP, param_df)

        # get data, create index and write to the store #
        data = record.data
        shape = data.shape
        index = pd.MultiIndex.from_product([[self.records], np.arange(shape[0])], names=["Record", "Row"])
        df = pd.DataFrame(data, index=index)
        self.store.append(group, df, index=False, **kwargs)


def create_recorders(exp_pkg):
    """ Create and return a set of recorder objects given the configuration dictionary.

    :param: exp_pkg: Experiment package module object.
    """
    rec_cfgs = exp_pkg.RECORDERS
    recorders = {}
    for cfg in rec_cfgs:
        name = cfg["instance_name"]

        # instantiate the recorder object. Search order for a recorder class is:
        # 1) User defined recorders in the provided experiment package.
        # 2) spherexlabtools core recorders.
        try:
            rec_class = getattr(exp_pkg.recorders, cfg["type"])
        except (AttributeError, ModuleNotFoundError):
            rec_mod = importlib.import_module(__name__)
            rec_class = getattr(rec_mod, cfg["type"])

        logger.info("Initializing %s as %s" % (cfg["instance_name"], rec_class))
        recorders[name] = rec_class(cfg)

    return recorders
