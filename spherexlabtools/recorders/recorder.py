import os
import logging
import numpy as np
import pandas as pd
from datetime import datetime

from ..thread import QueueThread


logger = logging.getLogger(__name__)


class CsvRecorder(QueueThread):
    """ Basic csv recorder class.
    """

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(**kwargs)

    def handle(self, record):
        """ Handle incoming records and append to existing csv or create a new one. Note that specific file paths should
            be specified with the 'filepath' keyword in calls to :py:meth:`BaseProcedure.emit`. If this key-word is not
            provided, then the current working directory will be used as the output.
        """
        data = record.data
        filepath = record.emit_kwargs.get("filepath", os.getcwd())
        data = pd.DataFrame(data)
        header = not (os.path.exists(filepath))
        data.to_csv(filepath, mode="a", header=header, index=False)


class PyhkRecorder(QueueThread):
    """ Basic recorder to log data to a .txt file in a Pyhk database.
    """

    _data_dir = "/data/hk"
    _delimiter_map = {
        " ": "%20"
    }
    _separator = "\t"

    def __init__(self, cfg, exp, **kwargs):
        """ Initialize a Pyhk recorder.

        :param data_dir: Path to directory where the pyhk database lives.
        """
        super().__init__(**kwargs)

    def handle(self, record):
        """ Handle incoming records by appending to the appropriate .txt. Pyhk requires the `sensor_type` and
            'sensor_name' to be specified, so these values must be provided as keywords in calls to
            :py:meth:`BaseProcedure.emit`. Also note that "timestamp" must be indexable within record.data.
        """
        kwargs = record.emit_kwargs
        assert "sensor_type" in kwargs.keys(), "Pyhk sensor type must be provided as a keyword in emit()!"
        assert "sensor_name" in kwargs.keys(), "Pyhk sensor name must be provided as a keyword in emit()!"
        sens_type = kwargs["sensor_type"]
        sens_name = kwargs["sensor_name"]
        for c, dc in self._delimiter_map.items():
            sens_name = sens_name.replace(c, dc)

        data = record.data
        ts = data["timestamp"]

        # convert timestamp to datetime and create the file-path #
        dt = datetime.fromtimestamp(ts)
        dt_str = dt.strftime("%Y:%m:%d")
        dt_str_split = dt_str.split(":")
        fp = os.path.join(self._data_dir, dt_str_split[0], dt_str_split[1], dt_str_split[2], sens_type, sens_name,
                          ".txt")

        # convert data to DataFrame if it is not already that type #
        if type(data) is not pd.DataFrame:
            data = pd.DataFrame(data)

        data.to_csv(fp, sep=self._separator, header=False, index=False)


class HDF5Recorder(QueueThread):
    """ Basic HDF5 recorder class.
    """

    META_GROUP = "Meta"
    GROUP_DELIMITER = "/"
    META_PROC_SEQ_SUBGROUP = f"{META_GROUP}{GROUP_DELIMITER}ProcSeq"
    META_PROC_PARAMS_SUBGROUP = f"{META_GROUP}{GROUP_DELIMITER}ProcParams"
    META_INST_PARAMS_SUBGROUP = f"{META_GROUP}{GROUP_DELIMITER}InstParams"
    DATA_GROUP = "Data"

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
        self.record_group_ind = 0
        # number of data entries in a record #
        self.record_group_size = 1

    def handle(self, record):
        """ HDF5 recorder handle.
        """
        kwargs = record.emit_kwargs
        # get record group size #
        if "group_records" in kwargs:
            self.record_group_size = kwargs.pop("group_records")

        # append to the Meta group ##################################################################################
        params_index = pd.MultiIndex.from_tuples([(self.record_num, self.record_group_ind)], names=["RecordNum",
                                                                                                    "RecordInd"])
        proc = record.proc
        seq = record.sequence
        proc_params = record.proc_params
        inst_params = record.inst_params
        proc_seq_group_df = pd.DataFrame({
            "Procedure": proc,
            "Sequence": seq,
        }, index=params_index)
        proc_params_group_df = pd.DataFrame(proc_params, index=params_index)
        inst_params_group_df = pd.DataFrame(inst_params, index=params_index)
        self.store.append(self.META_PROC_SEQ_SUBGROUP, proc_seq_group_df)
        self.store.append(self.META_PROC_PARAMS_SUBGROUP, proc_params_group_df)
        self.store.append(self.META_INST_PARAMS_SUBGROUP, inst_params_group_df)

        # append to the Data group ##################################################################################
        data = record.data
        shape = data.shape
        index = pd.MultiIndex.from_product([[self.record_num], [self.record_group_ind], np.arange(shape[0])],
                                           names=["RecordGroupNum", "RecordGroupInd", "Row"])
        data_df = pd.DataFrame(data, index=index)
        self.store.append(self.DATA_GROUP + self.GROUP_DELIMITER + record.name, data_df)

        # update the record index ###################################################################################
        record_complete = False
        if self.record_group_ind < (self.record_group_size - 1):
            self.record_group_ind += 1
        else:
            self.record_group_ind = 0
            record_complete = True

        # update record number #
        if record_complete:
            self.record_num += 1
