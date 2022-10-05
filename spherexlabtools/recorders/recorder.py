import os
import logging
import numpy as np
import pandas as pd

import spherexlabtools.log as slt_log
from spherexlabtools.thread import QueueThread

log_name = f"{slt_log.LOGGER_NAME}.{__name__.split('.')[-1]}"
logger = logging.getLogger(log_name)


class Recorder(QueueThread):
    """ Abstract base-class for all recorders. This class generates the 'RecordGroup', 'RecordGroupInd', and
    'RecordRow' indices used in output dataframes.
    """

    _rgroup_col_str = "RecordGroup"
    _rgroupind_col_str = "RecordGroupInd"
    _rrow_col_str = "RecordRow"
    _merge_on = [_rgroup_col_str, _rgroupind_col_str]

    _rgroup_val_str = "%06i"
    _rgroupind_val_str = "%06i"
    _rrow_val_str = "%06i"

    def __init__(self, cfg, exp, extension, merge=False, **kwargs):
        super().__init__(**kwargs)
        self.name = cfg["instance_name"]
        self.extension = extension
        self.results_path = None
        self.opened_results = None
        self.record_group = None
        self.record_group_ind = None
        self.record_row = None
        self.record_group_changed = False
        self.data_index = None
        self.meta_index = None
        self.procedure_start_time = None
        # - should record tables be merged before written out? - #
        self.merge = merge

        # - copies of record tables - #
        self.data_df = None
        self.pp_df = None
        self.meta_df = None
        self.merged_df = None


    def handle(self, record):
        """ Update the record_group, record_group_ind, and record_row attributes, then call overridden methods to
        write to the output file.
        """
        fp, file_exists = self.should_open(record)
        if fp is not False:
            # - if data_df is None, then no file has been opened at all yet, so don't close - #
            if self.data_df is not None:
                self.close_results()
            self.results_path = fp
            self.record_group, self.record_group_ind = self.open_results(file_exists)

        self.update_record_group(record)
        self.update_dataframes(record)
        self.update_results()

    def update_record_group(self, record):
        # - update record_group - #
        self.record_group_changed = False
        if self.procedure_start_time != record.procedure_start_time:
            self.record_group += 1
            self.record_group_changed = True
            self.procedure_start_time = record.procedure_start_time

        # - update record_group_ind - #
        if self.record_group_changed:
            self.record_group_ind = 0
        else:
            self.record_group_ind += 1

        self.record_row = record.data.shape[0]

    def update_dataframes(self, record):
        """ Update the pandas indices based on the current record_group and record_group_ind.
        """
        rgroup_str = self._rgroup_val_str % self.record_group
        rgroupind_str = self._rgroupind_val_str % self.record_group_ind
        # - update indices - #
        self.data_index = pd.MultiIndex.from_product([[rgroup_str], [rgroupind_str],
                                                      [self._rrow_val_str % i for i in np.arange(self.record_row)]],
                                                      names=[self._rgroup_col_str, self._rgroupind_col_str, self._rrow_col_str])

        self.meta_index = pd.MultiIndex.from_tuples([(rgroup_str, rgroupind_str)],
                                                    names=[self._rgroup_col_str, self._rgroupind_col_str])

        # - update dataframes - #
        # - data
        if type(record.data) is pd.DataFrame:
            self.data_df = record.data
            self.data_df.index = self.data_index
        else:
            self.data_df = pd.DataFrame(record.data, index=self.data_index)

        # - procedure parameters
        if type(record.proc_params) is pd.DataFrame:
            self.pp_df = record.proc_params
            self.pp_df.index = self.meta_index
        else:
            self.pp_df = pd.DataFrame(record.proc_params, index=self.meta_index)

        # - metadata
        if type(record.meta) is pd.DataFrame:
            self.meta_df = record.meta
            self.meta_df.index = self.meta_index
        else:
            self.meta_df = pd.DataFrame(record.meta, index=self.meta_index)

        print(self.data_df)
        print(self.meta_df)
        print(self.pp_df)

        # - if merge, then merge all dataframes into one - #
        if self.merge:
            self.pp_df.columns = ["_".join(["proc", col]) for col in self.pp_df.columns]
            self.meta_df.columns = ["_".join(["meta", col]) for col in self.meta_df.columns]
            merged0 = pd.merge(self.pp_df, self.meta_df, on=self._merge_on)
            self.merged_df = pd.merge(self.data_df, merged0, on=self._merge_on)
            self.merged_df.index = self.data_df.index

    def should_open(self, record):
        """ Check if new results should be opened via open_results().

        :param write_path: Path to results file.
        :return: Tuple of the form (file-path, Boolean indicating if the file exists).
        """
        fp = record.recorder_write_path
        if not fp.endswith(self.extension):
            fp += self.extension

        fp_exists = os.path.exists(fp)
        if (not fp_exists) or (self.results_path != fp):
            ret = fp
        else:
            ret = False

        return (ret, fp_exists)

    def open_results(self, exists):
        """ Open the results file and return the record_group and record_group_ind. This method must be implemented in
        subclasses and must return those values after opening (or creating) the results file.

        Overrides of this method in subclasses should use the self.results_path attribute as the path to the output
        file to open.

        :param: Boolean indicating if the file exists or not.
        :return: Return the initial record_group and record_group_ind for a new file.
        """
        raise NotImplementedError("The open_results() method must be implemented in a subclass!")

    def update_results(self):
        """ Update the results file in the format determined by recorder subclasses.
        """
        raise NotImplementedError("The update_results() method must be implemented in a subclass!")

    def close_results(self):
        """ Close the currently opened results file. This method must be implemented in subclasses.
        """
        raise NotImplementedError("The close_results() method must be implemented in a subclass!")
