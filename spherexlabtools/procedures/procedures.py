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
    :ivar sequence: Procedure sequence dictionary associated with the record.
    :ivar proc_params: Dictionary containing the parameters of the procedure that generated the record.
    :ivar inst_params: Dictionary containing the instrument parameters associated with the record.
    :ivar data: Main data object of any type.
    :ivar ancillary: Secondary information to accompany the data object, such as a histogram of the data values.
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

    lock = threading.Lock()
    lock_initialized = True
    proc = None
    sequence = None
    proc_params = None
    inst_params = None
    data = None
    ancillary = {}
    emit_kwargs = {}
    to_date = False

    # update attributes #
    avg = BooleanParameter("Average Buffer", default=False)
    buffer_size = IntegerParameter("Buffer Size", default=1)
    histogram = BooleanParameter("Generate Histogram", default=False)

    # save attributes #
    filepath = Parameter("Save Path", default=os.path.join(os.getcwd(), "Record"))
    save_type = Parameter("Save Type", default=".pkl")

    # for compatibility with the Parameter types #
    parameters = {}

    def __init__(self, name, proc):
        """ Initialize a record by providing a string representation of the procedure object used.

        :param proc: String representing the procedure object that updates the record.
        """
        self.name = name
        self.buffer = []
        self.proc = proc
        ParameterInspect.update_parameters(self)

    def update(self, data, proc_params=None, inst_params=None, sequence=None, **kwargs):
        """ Update the general attributes of the record.
        """
        self.proc_params = proc_params
        self.inst_params = inst_params
        self.sequence = sequence
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
            self.data = sum(self.buffer) / len(self.buffer)
        else:
            self.data = self.buffer[-1]

        # generate ancillary data #
        if self.histogram:
            self.ancillary["histogram"] = np.histogram(self.data)
        else:
            self.ancillary["histogram"] = None

        # record is now up-to-date #
        self.to_date = True

    def save(self):
        """ Save the record to a .mat or .pkl file. Note that the sequence is not saved out here, as it is of less
            concern what sequence a record was generated within when an individual record is saved out to a file.
        """
        save_obj = {
            "data": self.data,
            "buffer": self.buffer,
            "procedure": self.proc
        }
        if self.proc_params is not None:
            save_obj.update({"proc_params": self.proc_params})
        if self.inst_params is not None:
            save_obj.update({"inst_params": self.inst_params})
        fp = self.filepath + self.save_type
        if self.save_type == ".pkl":
            pickle.dump(save_obj, open(fp, "wb"))
        elif self.save_type == ".mat":
            spio.savemat(fp, save_obj)

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

    # this attribute gets replaced with a string representation of a procedure sequence if this procedure
    # is being run within a ProcedureSequence.
    sequence = None
    # parameters of the currently executing procedure #
    proc_params = None

    def __init__(self, cfg, exp, hw=None, viewers=None, recorders=None, update_params=True, **kwargs):
        """ Initialize a bare procedure instance.

        :param hw: :class:`..instruments.InstrumentSuite` object.
        :param exp: Experiment object. Used for compatibility with general class loader.
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
        self.hw = None
        self.records = {}
        self.record_queues = {}
        self.record_cfg = cfg["records"]
        self.status = BaseProcedure.QUEUED

        if type(cfg["hw"]) is list:
            self.hw = type("proc_hw", (object,), {})()
            for inst in cfg["hw"]:
                self.hw.__dict__[inst] = getattr(hw, inst)
        elif cfg["hw"] is not None:
            self.hw = getattr(hw, cfg["hw"])
        for key, val in cfg["records"].items():
            qdict_val = [{"viewer": self.exp.viewers, "recorder": self.exp.recorders}[k][v].queue for k, v in val.items()]
            self.record_queues[key] = qdict_val
            self.records[key] = Record(key, str(self))
        if update_params:
            ParameterInspect.update_parameters(self)
        for key in kwargs:
            if key in self.parameters.keys():
                setattr(self, key, kwargs[key])
        self.parameter_map = {pval.name: pkey for pkey, pval in self.parameters.items()}

    def startup(self):
        """ Check that all procedure parameters have been set.
        """
        self.status = BaseProcedure.RUNNING
        ParameterInspect.check_parameters(self)
        self.proc_params = ParameterInspect.parameter_values(self)

    def emit(self, record_name, record_data, inst_params=None, **kwargs):
        """ Post a record to the appropriate queues.

        :param record_name: String name of the record to post data to.
        :param record_data: Data to be posted to the record queue.
        :param inst_params: Optional set of instrument parameters to record.
        :param kwargs: Key-word arguments that are passed to the handle method of the corresponding
                       :class:`.QueueThread`.
        """
        record = self.records[record_name]
        record.update(record_data, inst_params=inst_params, proc_params=self.proc_params, sequence=self.sequence,
                      **kwargs)
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
                self.__dict__[rec] = BooleanParameter(rec, default=False)
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
            log_param = getattr(self, p)
            if log_param:
                logger.debug("LogProc getting %s" % p)
                data = getattr(self.hw, p)
                print(p, data)
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
        """ Set the sequence attribute of the procedure attribute.
        """
        BaseProcedure.startup(self)
        self.procedure.sequence = self.seq

    def execute(self):
        """ Execute the provided procedure in a loop from the constructed parameter list.
        """
        stopped = False
        for params in self.param_list[self.seq_ind:]:
            # set procedure parameters #
            for pkey, pval in params.items():
                setattr(self.procedure, self.procedure.parameter_map[pkey], pval)
            log_str = f"{self.name}: starting procedure {self.procedure.name} at index {self.seq_ind}"
            logger.info(log_str)
            self.exp.start_thread(log_str, self.procedure)
            # wait for the procedure to start running. #
            while not self.procedure.status == self.procedure.RUNNING:
                time.sleep(self.sleep)

            # wait until the procedure completes its execution. #
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

    def shutdown(self):
        """ Clear the sequence attribute of the procedure attribute.
        """
        self.procedure.sequence = None

