""" This module implements Recorder sub-classes that write to plain-text output files.
"""

import os
import logging
import pandas as pd

import spherexlabtools.log as slt_log
from spherexlabtools.recorders import Recorder


class CsvRecorder(Recorder):
    """ Joins the data, procedure parameters, and metadata into a single csv table.
    """

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)

    def open_results(self, results_path):
        """ Open the results csv file and return the record_group and record_group_ind.

        :param results_path: Path to the results.
        :return: Return the initial record_group and record_group_ind for a new file.
        """
        try:
            results_df = pd.read_csv(results_path)
        except FileNotFoundError:
            rec_group = -1
            rec_group_ind = 0
            self.opened_results = False
        else:
            rec_group = results_df[self._rgroup_str].values[-1]
            rec_group_ind = results_df[self._rgroupind_str].values[-1]
            self.opened_results = True

        return rec_group, rec_group_ind

    def close_results(self):
        """ Don't need this for the csv recorder.
        """
        pass

    def update_results(self, record):
        """ Join the data, procedure parameters, and metadata into a single dataframe and write
        to the output file.
        """
        pass
