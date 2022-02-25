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
    GROUP_DELIMITER = "/"

    def __init__(self, cfg, **kwargs):
        """ Initialize a recorder.
        """
        super().__init__(**kwargs)
        self.filename = cfg["filename"]
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
        kwargs = record.handle
        if "group" not in kwargs:
            err_msg = "required group argument not provided to the HDF5Recorder!"
            logger.error(err_msg)
            assert ValueError("The group argument is required for the HDF5Recorder!")
        group = kwargs.pop("group")

        # get record size #
        if "group_records" in kwargs:
            self.record_size = kwargs.pop("group_records")

        # append received data to store with the current record number and index #
        data = record.data
        #shape = data.shape
        index = pd.MultiIndex.from_product([[self.record_num], [self.record_ind]],
                                           names=["RecordNum", "RecordInd"])
        df = pd.DataFrame(data, index=index)
        df.sort_index(inplace=True)
        self.store.append(group, df, **kwargs)

        # write parameters #
        params = record.params
        index = pd.MultiIndex.from_tuples([(self.record_num, self.record_ind)], names=["RecordNum", "RecordInd"])
        param_df = pd.DataFrame(params, index=index)
        self.store.append(self.PARAMS_GROUP, param_df, data_columns=True)

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
