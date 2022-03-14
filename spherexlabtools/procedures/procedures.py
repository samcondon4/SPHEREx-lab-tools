""" This module implements a set of ubiquitous procedure classes for measurement execution. These
    classes include:

        - :class:`.BasicProc`

Sam Condon, 01/31/2022
"""
import time
import logging
import inspect
import threading
import importlib
from PyQt5 import QtCore
from copy import deepcopy
from pymeasure.experiment import Parameter, FloatParameter, IntegerParameter

from ..thread import StoppableReusableThread, QueueThread


logger = logging.getLogger(__name__)


class Record:
    """ Basic class implementing thread-safe attribute access. This allows a procedure to write the same data
        out to multiple queues on separate threads without worrying about race-conditions.
    """

    lock = None
    lock_initialized = False

    def __init__(self, data, params=None, handle=None):
        """ Initialize a record with specified data, parameters, and handle key-words.

        :params data: Data of any type.
        :param params: Parameters specifying the conditions under which the data was taken.
        :param handle: Dictionary of key-words specifying data handling arguments.
        """
        self.lock = threading.Lock()
        self.lock_initialized = True
        self.data = data
        self.params = params
        self.handle = handle

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
    _parameters = {}

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
        self.name = cfg["instance_name"]
        self.exp = exp
        if hw is not None:
            if type(cfg["hw"]) is list:
                self.hw = type("proc_hw", (object,), {})()
                for inst in cfg["hw"]:
                    self.hw.__dict__[inst] = getattr(hw, inst)
            else:
                self.hw = getattr(hw, cfg["hw"])
        qdict = {}
        for key, val in cfg["records"].items():
            # check if a list of queues has already been provided #
            if type(val) is not list:
                qdict_val = [{"viewer": viewers, "recorder": recorders}[k][v].queue for k, v in val.items()]
            else:
                qdict_val = val
            qdict[key] = qdict_val
        self.records = qdict
        self.status = BaseProcedure.QUEUED
        if update_params:
            self._update_parameters()
        for key in kwargs:
            if key in self._parameters.keys():
                setattr(self, key, kwargs[key])
        self.parameter_map = {pval.name: pkey for pkey, pval in self.parameter_objects().items()}

    def startup(self):
        """ Check that all procedure parameters have been set.
        """
        self.status = BaseProcedure.RUNNING
        self.check_parameters()

    def emit(self, record_name, record_data, record_params=True, **kwargs):
        """ Post a record to the appropriate queues.

        :param record_name: String name of the record to post data to.
        :param record_data: Data to be posted to the record queue.
        :param record_params: Boolean to indicate if the procedure parameters should be included in the
                              dictionary placed on the recorder queue. Optional argument with default
                              value of True.
        :param kwargs: Key-word arguments that are passed to the handle method of the corresponding
                       :class:`.QueueThread`.
        """
        params = None
        if record_params:
            params = self.parameter_values()
        record = Record(record_data, params=params, handle=kwargs)
        for q in self.records[record_name]:
            q.put(record)

    def shutdown(self):
        """ Set the procedure finished value.
        """
        self.status = BaseProcedure.FINISHED

    def _update_parameters(self):
        """ Collects all the Parameter objects for the procedure and stores
        them in a meta dictionary so that the actual values can be set in
        their stead
        """
        if not self._parameters:
            self._parameters = {}
        for item, parameter in self.__dict__.items():
            self._update_p(item, parameter, check=lambda p, cls: issubclass(type(p), cls))
        for item, parameter in inspect.getmembers(self.__class__):
            self._update_p(item, parameter, check=isinstance)

    def _update_p(self, i, p, check):
        """ Update a single parameter. Used by the above method.
        """
        if check(p, Parameter):
            self._parameters[i] = deepcopy(p)
            if p.is_set():
                setattr(self, i, p.value)
            else:
                setattr(self, i, None)

    def parameters_are_set(self):
        """ Returns True if all parameters are set """
        for name, parameter in self._parameters.items():
            if getattr(self, name) is None:
                return False
        return True

    def check_parameters(self):
        """ Raises an exception if any parameter is missing before calling
        the associated function. Ensures that each value can be set and
        got, which should cast it into the right format. Used as a decorator
        @check_parameters on the startup method
        """
        for name, parameter in self._parameters.items():
            value = getattr(self, name)
            if value is None:
                raise NameError("Missing {} '{}' in {}".format(
                    parameter.__class__, name, self.__class__))

    def parameter_values(self):
        """ Returns a dictionary of all the Parameter values and grabs any
        current values that are not in the default definitions
        """
        result = {}
        for name, parameter in self._parameters.items():
            value = getattr(self, name)
            if value is not None:
                parameter.value = value
                setattr(self, name, parameter.value)
                result[name] = parameter.value
            else:
                result[name] = None
        return result

    def parameter_objects(self):
        """ Returns a dictionary of all the Parameter objects and grabs any
        current values that are not in the default definitions
        """
        result = {}
        for name, parameter in self._parameters.items():
            value = getattr(self, name)
            if value is not None:
                parameter.value = value
                setattr(self, name, parameter.value)
            result[name] = parameter
        return result

    def refresh_parameters(self):
        """ Enforces that all the parameters are re-cast and updated in the meta
        dictionary
        """
        for name, parameter in self._parameters.items():
            value = getattr(self, name)
            parameter.value = value
            setattr(self, name, parameter.value)

    def set_parameters(self, parameters, except_missing=True):
        """ Sets a dictionary of parameters and raises an exception if additional
        parameters are present if except_missing is True
        """
        for name, value in parameters.items():
            if name in self._parameters:
                self._parameters[name].value = value
                setattr(self, name, self._parameters[name].value)
            else:
                if except_missing:
                    raise NameError("Parameter '{}' does not belong to '{}'".format(
                        name, repr(self)))


class LogProc(BaseProcedure):
    """ Basic procedure that continuously records a parameter at a defined refresh rate and
        sends it to a :class:`..recorders.Recorder`, a :class:`..viewers.Viewer`, or both
        with calls to :meth:`BaseProcedure.emit()`.
    """

    refresh_rate = FloatParameter("Log Rate", units="Hz.", default=1)

    _buf_id = "_buf"
    _avg_id = "_average"

    def __init__(self, cfg, exp, **kwargs):
        """ Initialize a basic procedure that will record data from the prop argument.

        :param cfg: List of procedure configurations.
        :param kwargs: Key-word arguments for :class:`.BaseProcedure`
        """
        super().__init__(cfg, exp, update_params=False, **kwargs)
        self.DATA_COLUMNS = list(self.records.keys())
        for rec in self.DATA_COLUMNS:
            setattr(self, rec+self._avg_id, IntegerParameter(rec+self._avg_id, units="records", default=1))
            setattr(self, rec+self._buf_id, [0])
        self._update_parameters()

    def execute(self):
        """ Procedure execution method. Calls get_properties() to start recording props at a fixed interval.
        """
        while not self.thread.should_stop():
            self.get_properties()
            time.sleep(1/self.refresh_rate)

    def update_buf(self, p, data, return_avg=False):
        """ Update a buffer for the record, p.
        """
        buf = getattr(self, p+self._buf_id)
        avg_len = getattr(self, p+self._avg_id)
        if len(buf) != avg_len:
            setattr(self, p+self._buf_id, [0 for _ in range(avg_len)])
            buf = getattr(self, p+self._buf_id)
        buf.pop(-1)
        buf.insert(0, data)
        if return_avg:
            return sum(buf) / len(buf)

    def get_properties(self):
        """ Retrieve all properties given in the DATA_COLUMNS list and emit results.
        """
        for p in self.DATA_COLUMNS:
            logger.debug("LogProc getting %s" % p)
            data = getattr(self.hw, p)
            data = self.update_buf(p, data, return_avg=True)
            self.emit(p, data)


class ProcedureSequence(BaseProcedure):
    """ Procedure class that wraps and executes a standalone procedure in a loop.
    """

    seq = Parameter("Procedure Sequence", default="")
    param_list = Parameter("Parameter List")
    sleep = FloatParameter("Sleep Interval", default=1, units="s.")
    seq_ind = 0

    def __init__(self, cfg, exp, proc, **kwargs):
        """
        """
        super().__init__(cfg, exp, **kwargs)
        self.procedure = proc

    def startup(self):
        """ Emit the provided sequence, and build the list of sequence parameters.
        """
        BaseProcedure.startup(self)
        if self.seq_ind == 0:
            self.emit("sequence", self.seq)

    def execute(self):
        """ Execute the provided procedure in a loop from the constructed parameter list.
        """
        stopped = False
        for params in self.param_list[self.seq_ind:]:
            # set procedure parameters #
            for pkey, pval in params.items():
                setattr(self.procedure, self.procedure.parameter_map[pkey], pval)
            self.exp.start_thread(f"{self.name}: starting procedure {self.procedure.name} at index {self.seq_ind}",
                                  self.procedure)
            while not self.procedure.status == self.procedure.FINISHED:
                time.sleep(self.sleep)
                if self.should_stop():
                    self.procedure.stop()
                    stopped = True
                    break
            if stopped:
                break
            else:
                self.seq_ind += 1

        if not stopped:
            self.seq_ind = 0


