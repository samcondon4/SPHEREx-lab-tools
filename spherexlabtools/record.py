import os
import logging
import threading
from spherexlabtools.parameters import ParameterInspect

import spherexlabtools.log as slt_log

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
        self.data = None
        self.proc_params = None
        self.meta = None
        self.procedure_start_time = None
        self.emit_kwargs = None
        self.to_date = False
        ParameterInspect.update_parameters(self)

    def update(self, data, proc_params=None, meta=None, proc_start_time=None, **kwargs):
        self.data = data
        self.proc_params = proc_params
        self.meta = meta
        self.procedure_start_time = proc_start_time
        self.emit_kwargs = kwargs
        self.to_date = True

    def save(self, file_arg=None):
        pass

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
