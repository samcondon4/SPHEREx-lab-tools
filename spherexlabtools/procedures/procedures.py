""" This module implements a set of ubiquitous procedure classes for measurement execution. These
    classes include:

        - :class:`.BasicProc`

Sam Condon, 01/31/2022
"""
import os
import time
import pickle
import logging
import threading
import numpy as np
import scipy.io as spio

from ..thread import StoppableReusableThread
from ..parameters import ParameterInspect, Parameter, FloatParameter, IntegerParameter, BooleanParameter


logger = logging.getLogger(__name__)


class Record:
    """ The fundamental class representing a data object in SPHERExLabTools. This class provides a thread safe
        object with the following attributes:

    **General**: Attributes used for general class behavior.
    :ivar lock: :class:`.threading.Lock` type used for thread safe access to instances.
    :ivar lock_initialized: Boolean to indicate if the lock has been initialized.
    :ivar proc: String representation of the procedure used to generate the record.
    :ivar data: Main data object of any type.
    :ivar ancillary: Secondary information to accompany the data object, such as a histogram of the data values.
    :ivar proc_params: Dictionary containing the parameters of the procedure that generated the record.
    :ivar inst_params: Dictionary containing the instrument parameters associated with the record.
    :ivar handle_kwargs: Key-word arguments used in the handle method of the appropriate viewer/recorder.
    :ivar to_date: Boolean to indicate if the data attribute is up-to-date. This is True immediately after the
                   :meth:`Record.update()` method is called, and gets set to False after the record is emitted.

    **Update**: Attributes that determine how the :meth:`Record.update()` method behaves.
    :ivar buffer: :class:`.IntegerParameter` which determines how large of a buffer to generate to hold data objects.
    :ivar avg: :class:`.IntegerParameter` which determines the number of data items in the buffer to average over
                to update the data attribute.
    :ivar histogram: Boolean to indicate if a histogram should be generated to accompany the data as ancillary
                     information.

    **Save**: Attributes that determine how the :meth:`Record.save()` method behaves.
    :ivar filepath: File path to where the record should get saved.
    :ivar save_type: Type of file to save record to. Currently, .mat and .pkl are supported.
    """

    lock = None
    lock_initialized = False

    def __init__(self, proc):
        """ Initialize a record by providing a string representation of the procedure object used.

        :param proc: String representing the procedure object that updates the record.
        """
        # general attributes #
        self.lock = threading.Lock()
        self.lock_initialized = True
        self.proc = proc
        self.data = None
        self.ancillary = {}
        self.proc_params = None
        self.inst_params = None
        self.emit_kwargs = {}
        self.buffer = []
        self.to_date = False

        # update attributes #
        self.avg = BooleanParameter("Average Buffer", default=False)
        self.buffer_size = IntegerParameter("Buffer Size", default=1)
        self.histogram = BooleanParameter("Generate Histogram", default=False)

        # save attributes #
        self.filepath = Parameter("Save Path", default=os.path.join(os.getcwd(), "Record"))
        self.save_type = Parameter("Save Type", default=".pkl")

    def update(self, data, proc_params=None, inst_params=None, **kwargs):
        """ Update the general attributes of the record.
        """
        self.proc_params = proc_params
        self.inst_params = inst_params
        self.emit_kwargs = kwargs
        # update the buffer attribute #
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(data)
        else:
            self.buffer[:-1] = self.buffer[1:]
            self.buffer[-1] = data

        # update the data attribute #
        if self.avg:
            self.data = sum(self.buffer) / len(self.buffer)
        else:
            self.data = self.buffer[-1]

        # generate ancillary data #
        if self.histogram:
            self.ancillary["histogram"] = np.histogram(self.data)

        # record is now up-to-date #
        self.to_date = True

    def save(self):
        """ Save the record to a .mat or .pkl file.
        """
        save_obj = {
            "data": self.data,
            "procedure": self.proc,
            "proc_params": self.proc_params,
            "inst_params": self.inst_params,
        }
        with open(self.filepath + self.save_type, "+") as file:
            if self.save_type == ".pkl":
                pickle.dump(save_obj, file)
            elif self.save_type == ".mat":
                spio.savemat(file, save_obj)

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


class BaseProcedure(StoppableReusableThread):
    """ Thread to execute a measurement. Largely based on the pymeasure procedure class.
    """

    DATA_COLUMNS = []
    MEASURE = {}
    FINISHED, FAILED, ABORTED, QUEUED, RUNNING = 0, 1, 2, 3, 4
    STATUS_STRINGS = {
        FINISHED: 'Finished', FAILED: 'Failed',
        ABORTED: 'Aborted', QUEUED: 'Queued',
        RUNNING: 'Running'
    }
    parameters = {}

    def __init__(self, cfg, exp, hw=None, viewers=None, recorders=None, update_params=True, **kwargs):
        """ Initialize a bare procedure instance.

        :param hw: :class:`..instruments.InstrumentSuite` object.
        :param exp: Experiment object. Used for compatiblity with general class loader.
        :param records: Dictionary containing lists of queues to which data should be posted on
                         calls to emit().
        :param viewers: Dictionary of Viewer objects.
        :param recorders: Dictionary of recorder objects.
        :param update_params: Boolean to indicate if self._update_parameters() should run in this init.
        :param kwargs: Key-word arguments to set the procedure parameters.
        """
        super().__init__()
        self.exp = exp
        self.hw = None
        self.records = {}
        self.record_queues = {}
        self.status = BaseProcedure.QUEUED

        if type(cfg["hw"]) is list:
            self.hw = type("proc_hw", (object,), {})()
            for inst in cfg["hw"]:
                self.hw.__dict__[inst] = getattr(hw, inst)
        else:
            self.hw = getattr(hw, cfg["hw"])
        for key, val in cfg["records"].items():
            qdict_val = [{"viewer": viewers, "recorder": recorders}[k][v].queue for k, v in val.items()]
            self.record_queues[key] = qdict_val
            self.records[key] = Record(str(self))
        if update_params:
            ParameterInspect.update_parameters(self)
        for key in kwargs:
            if key in self.parameters.keys():
                setattr(self, key, kwargs[key])

    def startup(self):
        """ Check that all procedure parameters have been set.
        """
        self.status = BaseProcedure.RUNNING
        ParameterInspect.check_parameters(self)

    def emit(self, record_name, record_data, proc_params=None, inst_params=None, **kwargs):
        """ Post a record to the appropriate queues.

        :param record_name: String name of the record to post data to.
        :param record_data: Data to be posted to the record queue.
        :param proc_params: Optional set of procedure parameters to record.
        :param inst_params: Optional set of instrument parameters to record.
        :param kwargs: Key-word arguments that are passed to the handle method of the corresponding
                       :class:`.QueueThread`.
        """
        record = self.records[record_name]
        record.update(record_data, proc_params, inst_params, **kwargs)
        for q in self.record_queues[record_name]:
            q.put(record)

    def shutdown(self):
        """ Set the procedure finished value.
        """
        self.status = BaseProcedure.FINISHED

    def __str__(self):
        result = repr(self) + "\n"
        for parameter in self.parameters.items():
            result += str(parameter)
        return result

    def __repr__(self):
        return "<{}(status={},parameters_are_set={})>".format(
            self.__class__.__name__, self.STATUS_STRINGS[self.status],
            ParameterInspect.parameters_are_set(self)
        )


class LogProc(BaseProcedure):
    """ Basic procedure that continuously records a parameter at a defined refresh rate and
        sends it to a :class:`..recorders.Recorder`, a :class:`..viewers.Viewer`, or both
        with calls to :meth:`BaseProcedure.emit()`.
    """

    refresh_rate = FloatParameter("Log Rate", units="Hz.", default=1)

    def __init__(self, cfg, exp, **kwargs):
        """ Initialize a basic procedure that will record data from the prop argument.

        :param cfg: List of procedure configurations.
        :param kwargs: Key-word arguments for :class:`.BaseProcedure`
        """
        super().__init__(cfg, exp, update_params=False, **kwargs)
        self.DATA_COLUMNS = []
        records = list(self.record_queues.keys())
        for rec in records:
            if rec not in self.DATA_COLUMNS:
                self.DATA_COLUMNS.append(rec)
        ParameterInspect.update_parameters(self)

    def execute(self):
        """ Procedure execution method. Calls get_properties() to start recording props at a fixed interval.
        """
        while not self.thread.should_stop():
            self.get_properties()
            time.sleep(1/self.refresh_rate)

    def get_properties(self):
        """ Retrieve all properties given in the DATA_COLUMNS list and emit results.
        """
        for p in self.DATA_COLUMNS:
            logger.debug("LogProc getting %s" % p)
            data = getattr(self.hw, p)
            self.emit(p, data)

