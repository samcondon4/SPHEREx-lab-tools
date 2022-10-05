""" This module implements Recorder sub-classes that write to binary output files.
"""

import os
import logging
import pandas as pd

import spherexlabtools.log as slt_log
from spherexlabtools.recorders import Recorder


class HDFRecorder(Recorder):
    """ Write the data, procedure parameters, and metadata into separate groups of an HDF5 file.
    """

    _data_group_str = "data"
    _pp_group_str = "proc_params"
    _meta_group_str = "meta"

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, extension=".h5", merge=False, **kwargs)

    def open_results(self, exists):
        """ Open existing or create a new .h5 file.

        :param results_path:
        :return: The appropriate RecordGroup and RecordGroupInd values.
        """
        self.opened_results = pd.HDFStore(self.results_path)
        if exists:
            rec_group, rec_group_ind = self.opened_results[self._pp_group_str].index[-1]
        else:
            rec_group = -1
            rec_group_ind = -1

        return rec_group, rec_group_ind

    def close_results(self):
        """ Close the .h5 results file.
        """
        if self.opened_results is not None:
            self.opened_results.close()
            self.opened_results = None

    def update_results(self):
        """ update the .h5 results with information from the new dataframes.
        """
        self.opened_results.append(self._data_group_str, self.data_df)
        self.opened_results.append(self._pp_group_str, self.pp_df)
        self.opened_results.append(self._meta_group_str, self.meta_df)
