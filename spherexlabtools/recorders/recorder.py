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

    _rgroup_str = "RecordGroup"
    _rgroupind_str = "RecordGroupInd"
    _rrow_str = "RecordRow"

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(**kwargs)
        self.name = cfg["instance_name"]
        self.results_path = None
        self.opened_results = None
        self.record_group = None
        self.record_group_ind = None
        self.record_row = None
        self.record_group_changed = False
        self.data_index = None
        self.meta_index = None
        self.procedure_start_time = None

    def handle(self, record):
        """ Update the record_group, record_group_ind, and record_row attributes, then call overridden methods to
        write to the output file.
        """
        if record.recorder_write_path != self.results_path:
            self.results_path = record.recorder_write_path
            self.close_results()
            self.record_group, self.record_group_ind = self.open_results(self.results_path)

        self.update_record_group(record)
        self.update_indices()
        self.update_results(record)

    def update_record_group(self, record):
        # - update record_group - #
        self.record_group_changed = False
        if self.procedure_start_time != record.procedure_start_time:
            self.record_group += 1
            self.record_group_changed = True

        # - update record_group_ind - #
        if self.record_group_changed:
            self.record_group_ind = 0
        else:
            self.record_group_ind += 1

    def update_indices(self):
        """ Update the pandas indices based on the current record_group and record_group_ind.
        """
        self.data_index = pd.MultiIndex.from_product([[self.record_group], [self.record_group_ind],
                                                      np.arange(self.record_row)], names=[self._rgroup_str,
                                                                                          self._rgroupind_str,
                                                                                          self._rrow_str])
        self.meta_index = pd.MultiIndex.from_tuples([(self.record_group, self.record_group_ind)],
                                                    names=[self._rgroup_str, self._rgroupind_str])

    def open_results(self, results_path):
        """ Open the results file and return the record_group and record_group_ind. This method must be implemented in
        subclasses and must return those values after opening (or creating) the results file.

        :param results_path: Path to the results.
        :return: Return the initial record_group and record_group_ind for a new file.
        """
        raise NotImplementedError("The open_results() method must be implemented in a subclass!")

    def update_results(self, record):
        """ Update the results file in the format determined by recorder subclasses.
        """
        raise NotImplementedError("The update_results() method must be implemented in a subclass!")

    def close_results(self):
        """ Close the currently opened results file. This method must be implemented in subclasses.
        """
        raise NotImplementedError("The close_results() method must be implemented in a subclass!")
