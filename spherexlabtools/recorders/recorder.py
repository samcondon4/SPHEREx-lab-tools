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
    PROC_PARAMS_GROUP = "ProcParams"
    INST_PARAMS_GROUP = "InstParams"
    GROUP_DELIMITER = "/"

    def __init__(self, cfg, exp, **kwargs):
        """ Initialize a recorder.
        """
        super().__init__(**kwargs)
        self.filename = cfg["filename"]
        self.exp = exp
        self.store = pd.HDFStore(self.filename)
        # if this is a new hdf file, with no Meta group, add the group #
        if (self.GROUP_DELIMITER + self.META_GROUP) not in self.store.keys():
            meta_series = pd.Series({"Records": 0})
            self.store.put(self.META_GROUP, meta_series)
            self.record_num = 0
        else:
            self.record_num = self.store.get(self.META_GROUP)["Records"]

        # data index within the record #
        self.record_ind = 0
        # number of data entries in a record #
        self.record_size = 1

    def handle(self, record):
        """ HDF5 recorder handle.
        """
        kwargs = record.emit_kwargs
        if "group" not in kwargs:
            err_msg = "required group argument not provided to the HDF5Recorder!"
            logger.error(err_msg)
            assert ValueError("The group argument is required for the HDF5Recorder!")
        group = kwargs.pop("group")

        # get record size #
        if "group_records" in kwargs:
            self.record_size = kwargs.pop("group_records")

        # append received data to the store with the current record number and index #
        data = record.data
        shape = data.shape
        index = pd.MultiIndex.from_product([[self.record_num], [self.record_ind], np.arange(shape[0])],
                                           names=["RecordGroupNum", "RecordGroupInd", "Row"])
        df = pd.DataFrame(data, index=index)
        df.sort_index(inplace=True)
        self.store.append(group, df, **kwargs)

        # write procedure parameters #
        param_index = pd.MultiIndex.from_tuples([(self.record_num, self.record_ind)], names=["RecordNum", "RecordInd"])
        proc_params = record.proc_params
        if proc_params is not None:
            param_df = pd.DataFrame(proc_params, index=param_index)
            self.store.append(self.PROC_PARAMS_GROUP, param_df, data_columns=True)

        # write instrument parameters #
        inst_params = record.inst_params
        if inst_params is not None:
            param_df = pd.DataFrame(inst_params, index=param_index)
            self.store.append(self.INST_PARAMS_GROUP, param_df, data_columns=True)

        # update record index #
        record_complete = False
        if self.record_ind < (self.record_size - 1):
            self.record_ind += 1
        else:
            self.record_ind = 0
            record_complete = True

        # update record number #
        if record_complete:
            self.record_num += 1
            self.store.put(self.META_GROUP, pd.Series({"Records": self.record_num}), data_columns=True)
