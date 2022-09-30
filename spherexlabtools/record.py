import datetime
import os
import logging
import threading
from spherexlabtools.parameters import ParameterInspect, Parameter, BooleanParameter, IntegerParameter

import spherexlabtools.log as slt_log

log_name = f"{slt_log.LOGGER_NAME}.{__name__.split('.')[-1]}"
logger = logging.getLogger(log_name)


class Record:

    lock = threading.Lock()
    lock_initialized = True

    # update attributes #
    avg = BooleanParameter("Average Buffer", default=False)
    buffer_size = IntegerParameter("Buffer Size", default=1)
    generate_ancillary = BooleanParameter("Generate Ancillary", default=False)

    # save attributes #
    filepath = Parameter("Save Path", default=os.path.join(os.getcwd(), "Record"))
    save_type = Parameter("Save Type", default=".pkl")

    # for compatibility with the Parameter types #
    parameters = {}

    def __init__(self, name, viewer=None, recorder=None, **kwargs):
        """ Initialize a record.

        :param name: String identifying the record.
        :param viewer: String identifying the viewer associated with this record.
        :param recorder: String identifying the recorder associated with this record.
        """
        self.name = name
        self.viewer = viewer
        self.recorder = recorder
        self.recorder_write_path = os.path.join(os.getcwd(), self.name)
        self.data = None
        self.timestamp = None
        self.proc_params = None
        self.meta = None
        self.procedure_start_time = None
        self.emit_kwargs = None
        self.to_date = False

        # - parameters - #
        self.parameters = {}
        ParameterInspect.update_parameters(self)

        # - TODO: this is for backwards compatibility and should be deprecated - #
        self.ancillary = {}
        self.buffer = []

    def update(self, data, proc_params=None, meta=None, proc_start_time=None, **kwargs):
        self.data = data
        try:
            if "timestamp" in self.data.columns:
                self.timestamp = self.data["timestamp"].values[0]
            else:
                self.timestamp = datetime.datetime.now()
        except (KeyError, AttributeError):
            self.timestamp = datetime.datetime.now()
        self.proc_params = proc_params
        self.meta = meta
        self.procedure_start_time = proc_start_time
        self.emit_kwargs = kwargs

        # update the buffer attribute #
        dbuf_size = self.buffer_size - len(self.buffer)
        if dbuf_size > 0:
            self.buffer.append(data)
        elif dbuf_size < 0:
            self.buffer = self.buffer[:dbuf_size]
            self.buffer[-1] = data
        else:
            self.buffer[:-1] = self.buffer[1:]
            self.buffer[-1] = data

        # update the data attribute #
        if self.avg:
            self.data = np.mean(self.buffer, axis=0)
        else:
            self.data = self.buffer[-1]

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
