import os
import logging
import numpy as np
import pandas as pd
import scipy.io as spio
from datetime import datetime

from ..thread import QueueThread

logger = logging.getLogger(__name__)


class SltRecorder(QueueThread):
    """ Abstract base-class for SPHERExLabTools specific recorders. This class generates the indices used in the
    :py:class:`pd.DataFrame` objects that are written out to results files with subclasses of this base. The indices
    that are tracked are as follows:

        - "RecordGroup": Used to index procedure sequences. This value is incremented whenever a new procedure sequence
          is set on the "sequence" attribute of the incoming record, or when this same attribute is set
          to None. The latter case corresponds to when the record was generated from within an individual
          procedure and not a procedure sequence.

        - "RecordGroupInd": Used to index a specific procedure within a procedure sequence. This value is incremented on
          every call of :py:meth:`SltRecorder.handle` or is reset to 0 if the "RecordGroup" value was
          just changed.

        - "RecordRow": Only used in the "data" dataframe and is determined by the shape of the incoming record.data

    :ivar record_group: Integer attribute corresponding to the "RecordGroup" index described above.
    :ivar record_group_ind: Integer attribute corresponding to the "RecordGroupInd" index described above.
    :ivar record_row: Integer (or array-like) attribute corresponding to the "RecordRow" index described above.
    :ivar data_index: Pandas index object for the record data.
    :ivar meta_index: Pandas index object for the record procedure and instrument parameters.
    :ivar sequence_index: Pandas index object for the record procedure sequence.
    :cvar _rgroup_str: String name used in dataframes to identify the "RecordGroup" index described above.
    :cvar _rgroupind_str: String name used in dataframes to identify the "RecordGroupInd" index described above.
    :cvar _rrow_str: String name used in dataframes to identify the "RecordRow" index described above.
    """

    _rgroup_str = "RecordGroup"
    _rgroupind_str = "RecordGroupInd"
    _rrow_str = "RecordRow"

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(**kwargs)
        self.results_path = None
        self.opened_results = None
        self.prev_seq_ts = None
        self.record_row = None
        self.record_group = None
        self.record_group_ind = None
        self.data_index = None
        self.meta_index = None
        self.sequence_index = None

    def handle(self, record):
        """ Update the record_group, record_group_ind, and record_row attributes based on information provided in
            the record.
        """
        if record.filepath != self.results_path:
            self.results_path = record.filepath
            self.close_results()
            self.record_group, self.record_group_ind = self.open_results(self.results_path)

        # update record_group #
        rec_group_changed = False
        if record.sequence is None:
            self.record_group += 1
            rec_group_changed = True
        elif self.prev_group_ts != record.sequence_timestamp:
            self.record_group += 1
            rec_group_changed = True

        # update record_group_ind #
        if rec_group_changed:
            self.record_group_ind = 0
        else:
            self.record_group_ind += 1

        self.record_row = record.data.shape[0]

        # update the pandas index objects #
        self.data_index = pd.MultiIndex.from_product([[self.record_group], [self.record_group_ind],
                                                      np.arange(self.record_row)], names=[self._rgroup_str,
                                                                                          self._rgroupind_str,
                                                                                          self._rrow_str])

        self.meta_index = pd.MultiIndex.from_tuples([(self.record_group, self.record_group_ind)],
                                                    names=[self._rgroup_str, self._rgroupind_str])

        self.sequence_index = [self.record_group]

        # update the results file with the new indices #
        self.update_results(record)

    def open_results(self, results_path):
        """ Open the results file and return the record_group and record_group_ind. This method must be implemented in
        subclasses and must return those values after opening (or creating) the results file.

        :param results_path: Path to the results.
        :return: Return the initial record_group and record_group_ind for a new file.
        """
        raise NotImplementedError("The open_results() method must be implemented in a subclass!")

    def close_results(self):
        """ Close the currently opened results file. This method must be implemented in subclasses.
        """
        raise NotImplementedError("The close_results() method must be implemented in a subclass!")

    def update_results(self, record):
        """ Update the results file in the format determined by recorder subclasses.
        """
        raise NotImplementedError("The update_results() method must be implemented in a subclass!")


class MatRecorder(SltRecorder):
    """ Basic class used to save records to a Matlab .mat file.
    """

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)

    def open_results(self, results_path):
        """ Open existing or create new .mat file.
        """
        fn = results_path + ".mat"
        try:
            self.opened_results = spio.loadmat(fn)
        except FileNotFoundError:
            with open(fn, "wb") as f:
                spio.savemat(f, {})
            rec_group = 0
            rec_group_ind = 0
            self.opened_results = spio.loadmat(fn)
        else:
            rec_group = len(self.opened_results["sequence"])
            rec_group_ind = 0

        return rec_group, rec_group_ind

    def close_results(self):
        """ Close the opened results.
        """
        self.opened_results = None

    def update_results(self, record):
        """ Update the dataframes saved in the .mat file.
        """
        try:
            data = self.opened_results["data"]
            proc_params = {key: val for key, val in self.opened_results.items() if "proc" in key}
            inst_params = {key: val for key, val in self.opened_results.items() if "inst" in key}
        except KeyError:
            data = record.data
            proc_params = {"proc_"+key: val for key, val in record.proc_params}
            inst_params = {"inst_"+key: val for key, val in record.inst_params}
        else:
            data = np.append(data, record.data, axis=0)
            for key, val in record.proc_params.items():
                proc_params["proc_"+key] = np.append(proc_params[key], val)
            for key, val in record.inst_params.items():
                inst_params["inst_"+key] = np.append(inst_params[key], val)

        # write dataframes back to .mat and reopen the updated results file. #
        mat_dict = {
            "data": data,
        }
        mat_dict.update(proc_params)
        mat_dict.update(inst_params)
        spio.savemat(self.results_path + ".mat", mat_dict)
        self.opened_results = spio.loadmat(self.results_path+".mat")


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
        filepath = record.recorder_write_path
        if ".csv" not in filepath:
            filepath += ".csv"
        data = pd.DataFrame(data)
        if record.timestamp is not None:
            data["timestamp"] = [record.timestamp]
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
        """
        super().__init__(**kwargs)

    def handle(self, record):
        """ Handle incoming records by appending to the appropriate .txt.
        """
        data = record.data
        ts = record.timestamp

        sens_name = record.__dict__.get("alias", record.name)
        sens_type = record.type
        for c, dc in self._delimiter_map.items():
            sens_name = sens_name.replace(c, dc)

        # convert timestamp to datetime and create the file-path #
        dt = datetime.fromtimestamp(ts)
        dt_str = dt.strftime("%Y:%m:%d")
        dt_str_split = dt_str.split(":")
        fp = os.path.join(self._data_dir, dt_str_split[0], dt_str_split[1], dt_str_split[2], sens_type,
                          sens_name + ".txt")

        # convert data to DataFrame if it is not already that type #
        data = pd.DataFrame(
            {"timestamp": [ts], "data": [data]}
        )

        data.to_csv(fp, mode="a", sep=self._separator, header=False, index=False)


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
