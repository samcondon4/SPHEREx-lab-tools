import os
import logging
import threading
import numpy as np
import pandas as pd
from pyqtgraph.parametertree import Parameter

import spherexlabtools.log as slt_log
from spherexlabtools.ui import get_object_parameters

log_name = f"{slt_log.LOGGER_NAME}.{__name__.split('.')[-1]}"
logger = logging.getLogger(log_name)


class Record:

    lock = threading.Lock()
    lock_initialized = True

    def __init__(self, name, viewer=None, recorder=None, **kwargs):
        """ Initialize a record.

        :param name: String identifying the record.
        :param viewer: String identifying the viewer associated with this record.
        :param recorder: String identifying the recorder associated with this record.
        """
        self.name = name
        self.recorder_write_path = os.path.join(os.getcwd(), self.name)
        self.data = None
        self.timestamp = None
        self.proc_params = None
        self.meta = None
        self.procedure_start_time = None
        self.emit_kwargs = None
        self.to_date = False

        # - set the viewer and recorder parameter names - #
        viewer_name = 'None' if viewer is None else viewer.name
        rec_name = 'None' if recorder is None else recorder.name
        self.viewer = Parameter.create(name='Viewer', type='str', value=viewer_name, enabled=False,
                                       children=get_object_parameters(viewer))
        self.recorder = Parameter.create(name='Recorder', type='str', value=rec_name, enabled=False,
                                         children=get_object_parameters(recorder))

    def update(self, data, proc_params=None, meta=None, proc_start_time=None, **kwargs):
        # - update the data dataframe - #
        dtype = type(data)
        if dtype is np.ndarray:
            data_dict = {
                "_".join([self.name, str(i)]): data[:, i] for i in range(data.shape[1])
            }
            self.data = pd.DataFrame(data_dict)
        elif dtype is not pd.DataFrame:
            self.data = pd.DataFrame({self.name: data}, index=[0])
        else:
            self.data = data

        # - update the procedure parameters and metadata dataframes - #
        self.proc_params = pd.DataFrame(proc_params, index=[0])
        self.meta = pd.DataFrame(meta, index=[0])
        self.procedure_start_time = proc_start_time
        self.emit_kwargs = kwargs

        self.to_date = True

    def __getattribute__(self, name):
        """ Attribute access override for thread safety.
        """
        if not name == "lock" and object.__getattribute__(self, "lock_initialized"):
            with object.__getattribute__(self, "lock"):
                ret = object.__getattribute__(self, name)
        else:
            ret = object.__getattribute__(self, name)

        return ret

    def __setattr__(self, name, value):
        """ Override attribute access for thread safety.
        """
        if not name == "lock" and object.__getattribute__(self, "lock_initialized"):
            with object.__getattribute__(self, "lock"):
                object.__setattr__(self, name, value)

        elif name == "lock" and object.__getattribute__(self, "lock_initialized"):
            raise ValueError("Record lock cannot be modified!")

        else:
            object.__setattr__(self, name, value)
