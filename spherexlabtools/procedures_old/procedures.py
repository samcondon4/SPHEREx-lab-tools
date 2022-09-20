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
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from pyqtgraph.parametertree import Parameter, ParameterTree

from ..thread import StoppableReusableThread
from ..parameters import ParameterInspect, Parameter, FloatParameter, IntegerParameter, BooleanParameter
import spherexlabtools.log as slt_log
from spherexlabtools.ui.widgets import Records


log_name = f"{slt_log.LOGGER_NAME}.{__name__.split('.')[-1]}"
logger = logging.getLogger(log_name)


class Record:
    """ The fundamental class representing a data object in SPHERExLabTools. This class provides a thread safe
        object with the following attributes:

    **General**: Attributes used for general class behavior.
    :ivar lock: :class:`.threading.Lock` type used for thread safe access to instances.
    :ivar lock_initialized: Boolean to indicate if the lock has been initialized.
    :ivar proc: String representation of the procedure used to generate the record.
    :ivar data: Main data object of any type.
    :ivar proc_params: Dictionary containing the parameters of the procedure that generated the record.
    :ivar inst_params: Dictionary containing the instrument parameters associated with the record.
    :ivar sequence: Procedure sequence dictionary associated with the record.
    :ivar sequence_timestamp: Timestamp indicating when the procedure sequence that generated the record started.
    :ivar procedure_timestamp: Timestamp indicating when the procedure that generated the record started.
    :ivar data_timestamp: Timestamp of when the individual data point was generated.
    :ivar ancillary: Secondary information to accompany the data object, such as a histogram of the data values.
    :ivar emit_kwargs: Key-word arguments used in the handle method of the appropriate viewer/recorder.
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
    data = None
    proc_params = None
    inst_params = None
    sequence = None
    sequence_timestamp = None
    procedure_timestamp = None
    data_timestamp = None
    ancillary = {}
    emit_kwargs = {}
    to_date = False

    # update attributes #
    avg = BooleanParameter("Average Buffer", default=False)
    buffer_size = IntegerParameter("Buffer Size", default=1)
    generate_ancillary = BooleanParameter("Generate Ancillary", default=False)

    # save attributes #
    filepath = Parameter("Save Path", default=os.path.join(os.getcwd(), "Record"))
    save_type = Parameter("Save Type", default=".pkl")

    # for compatibility with the Parameter types #
    parameters = {}

    def __init__(self, name, proc, alias=None, typ=None, viewer=None, recorder=None, subrecords=None,
                 ancillary_generator=None):
        """ Initialize a record by providing a string representation of the procedure object used.

        :param name: String identifying the record.
        :param proc: String representing the procedure object that updates the record.
        :param alias: String representing an alias name for the record.
        :param typ: String identifying the type of the record.
        :param viewer: String identifying the viewer associated with this record.
        :param recorder: String identifying the recorder associated with this record.
        :param subrecords: None, or list of records whose data this record encapsulates.
        :param ancillary_generator: Optional callable that will be passed the record instance and shall return
                              an object that will be set as the ancillary attribute of the record on each call
                              to update().
        """
        self.name = name
        self.buffer = []
        self.proc = proc
        self.alias = alias
        self.type = typ
        self.viewer = viewer
        self.recorder = recorder
        self.recorder_write_path = os.path.join(os.getcwd(), self.name)
        self.subrecords = subrecords
        self.sequence_timestamp = None
        self.procedure_timestamp = None
        self.data_timestamp = None
        self.ancillary_gen = ancillary_generator
        ParameterInspect.update_parameters(self)

    def update(self, data, proc_params=None, inst_params=None, sequence=None, **kwargs):
        """ Update the general attributes of the record.

        :param data: Data point of any type associated with the record.
        :param proc_params: Dictionary of parameters from the procedure that generated the record.
        :param inst_params: Dictionary of instrument parameters from the procedure that generated the record.
        :param sequence: String representation of the procedure sequence that generated the record.
        """
        self.proc_params = proc_params
        self.inst_params = inst_params
        self.sequence = {"sequence": [str(sequence)]}
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

        # generate ancillary data #
        if self.ancillary_gen is not None and self.generate_ancillary:
            self.ancillary = self.ancillary_gen(self)

        # record is now up-to-date #
        self.to_date = True

    def save(self, file_arg=None):
        """ Save the record to a .mat or .pkl file. Note that the sequence is not saved out here, as it is of less
            concern what sequence a record was generated within when an individual record is saved out to a file.

        :param file_arg: String or file-like object to use for the save routines.
        """
        save_obj = {
            "data": self.data,
            "procedure": self.proc
        }
        if self.proc_params is not None:
            save_obj.update({"proc_params": self.proc_params})
        if self.inst_params is not None:
            save_obj.update({"inst_params": self.inst_params})

        f = file_arg if file_arg is not None else self.filepath + self.save_type
        if type(f) is str:
            f = open(f, "wb")

        if self.save_type == ".pkl":
            pickle.dump(save_obj, f)
        elif self.save_type == ".mat":
            spio.savemat(f, save_obj, appendmat=True)

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
    # sequence_start_ts is a posix time timestamp for when the procedure sequence started execution #
    sequence_start_ts = None
    start_ts = None
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
        logger.info(slt_log.INIT_MSG % self.name)
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
            val_dict = {vkey: vval for vkey, vval in val.items()}
            kwargs_dict = {}
            for vkey in list(val_dict.keys()):
                if vkey not in ["viewer", "recorder"]:
                    kwargs_dict[vkey] = val_dict.pop(vkey)
            view_rec_val = {k: {"viewer": self.exp.viewers, "recorder": self.exp.recorders}[k][v] for k, v in
                            val_dict.items()}
            qdict_val = [comp.queue for comp in view_rec_val.values()]
            kwargs_dict.update({k: v.name for k, v in view_rec_val.items()})
            self.record_queues[key] = qdict_val
            self.records[key] = Record(key, str(self), **kwargs_dict)
        if update_params:
            ParameterInspect.update_parameters(self)
        for key in kwargs:
            if key in self.parameters.keys():
                setattr(self, key, kwargs[key])
        self.parameter_map = {pval.name: pkey for pkey, pval in self.parameters.items()}

        # - records ui - #
        self.records_interface = Records(self.records)
        self.records_interface_tree = ParameterTree()
        setattr(self.records_interface_tree, "name", self.name)
        #self.records_interface_tree_layout = QtWidgets.QGridLayout()
        self.records_interface.new_record_params_sig.connect(self.update_record_attrs)
        self.records_interface.save_record_sig.connect(self.save_record)
        self.records_interface_tree.setParameters(self.records_interface)
        #self.records_interface_tree_layout.addWidget(self.records_interface_tree)
        logger.info(slt_log.CMPLT_MSG % f"{self.name} initialization")

    def startup(self):
        """ Check that all procedure parameters have been set.
        """
        self.status = BaseProcedure.RUNNING
        ParameterInspect.check_parameters(self)
        self.proc_params = ParameterInspect.parameter_values(self)
        self.start_ts = datetime.now().timestamp()

    def emit(self, record_name, record_data, inst_params=None, data_ts=None, filepath=None, **kwargs):
        """ Post a record to the appropriate queues.

        :param record_name: String name of the record to post data to.
        :param record_data: Data to be posted to the record queue.
        :param inst_params: Optional set of instrument parameters to record.
        :param data_ts: Timestamp of when the individual data point was generated.
        :param filepath: String filepath to where the record should be saved if it is connected to a recorder.
                         If set to None, the record.filepath is not modified as it may have been set by a controller.
        :param kwargs: Key-word arguments that are passed to the handle method of the corresponding
                       :class:`.QueueThread`.
        """
        record = self.records[record_name]
        record.sequence_timestamp = self.sequence_start_ts
        record.procedure_timestamp = self.start_ts
        record.data_timestamp = data_ts
        if filepath is not None:
            record.filepath = filepath
        record.update(record_data, inst_params=inst_params, proc_params=self.proc_params, sequence=self.sequence,
                      **kwargs)
        for q in self.record_queues[record_name]:
            q.put(record)

    def shutdown(self):
        """ Set the procedure finished value.
        """
        self.status = BaseProcedure.FINISHED

    def update_record_attrs(self, record_param, record_name):
        """ Update a record with the provided attributes.
        """
        rec_name_param_set_map = {
            "Integrate Buffer": "avg",
            "Buffer Size": "buffer_size",
            "Run Ancillary Generator": "generate_ancillary",
            "Recorder Write Path": "recorder_write_path"
        }
        record = self.records[record_name]
        setattr(record, rec_name_param_set_map[record_param.name()], record_param.value())

    def save_record(self, save_record_params, record_name):
        """ Save the record in the format specified.
        """
        record = self.records[record_name]
        save_vals = save_record_params.getValues()
        record.filepath = save_vals["File-path"][0]
        record.save_type = save_vals["Type"][0]
        record.save()

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
        self.DATA_RECORDS = []
        self.COMPOUND_RECORDS = []
        for rec in self.records.values():
            if rec.subrecords is not None:
                self.COMPOUND_RECORDS.append(rec)
            if rec not in self.DATA_RECORDS and rec not in self.COMPOUND_RECORDS:
                self.DATA_RECORDS.append(rec)
                self.__dict__[rec.name] = BooleanParameter(rec.name, default=True)
        ParameterInspect.update_parameters(self)

    def execute(self):
        """ Procedure execution method. Calls get_properties() to start recording props at a fixed interval.
        """
        while not self.thread.should_stop():
            self.get_properties()
            time.sleep(1 / self.refresh_rate)

    def get_properties(self):
        """ Retrieve all properties given in the DATA_RECORDS list and emit results.
            Generate data for all records in the COMPOUND_RECORDS list and emit results.
        """
        # get record timestamp #
        ts = datetime.timestamp(datetime.now())
        data_vals = {rec.name: None for rec in self.DATA_RECORDS}
        # retrieve data for all data records #
        for rec in self.DATA_RECORDS:
            log_param = getattr(self, rec.name)
            if log_param:
                #logger.debug("LogProc getting %s" % rec.name)
                data = getattr(self.hw, rec.name)
                data_vals[rec.name] = data
                self.emit(rec.name, data, timestamp=ts)

        # collect and emit data for all compound records #
        for rec in self.COMPOUND_RECORDS:
            subrecords = rec.subrecords
            sr_dict = {subrec_name: [data_vals[subrec_name]] for subrec_name in subrecords}
            self.emit(rec.name, sr_dict, timestamp=ts)


class CompoundProcedure(BaseProcedure):
    """ Procedure class that merges multiple procedures so that they can be executed at the same time.
    """

    def __init__(self, cfg, exp, pend=1, **kwargs):
        """
        """
        cfg["hw"] = None
        cfg["records"] = {}
        self.subprocedures = {c["instance_name"]: exp.procedures[c["instance_name"]] for c in cfg["subprocedures"]}
        self.param_to_proc_map = {}
        self.pend = pend
        for proc in self.subprocedures.values():
            cfg["records"].update(proc.record_cfg)
            for key, val in ParameterInspect.parameter_objects(proc).items():
                self.__dict__[key] = val
                self.param_to_proc_map[key] = proc
        super().__init__(cfg, exp, **kwargs)

    def startup(self):
        BaseProcedure.startup(self)
        for pkey, param in ParameterInspect.parameter_objects(self).items():
            setattr(self.param_to_proc_map[pkey], pkey, param.value)

    def execute(self):
        # start all procedures #
        for proc in self.subprocedures.values():
            self.exp.start_thread(proc.name, proc)

        while self.procs_running():
            if self.should_stop():
                for proc in self.subprocedures.values():
                    proc.stop()
            time.sleep(self.pend)

    def procs_running(self):
        """ Check if there are any procedures running.
        """
        ret = False
        for proc in self.subprocedures.values():
            if proc.status == BaseProcedure.RUNNING and type(proc) is not LogProc:
                ret = True
                break

        return ret


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
        self.procedure.sequence_start_ts = self.start_ts

    def execute(self):
        """ Execute the provided procedure in a loop from the constructed parameter list.
        """
        stopped = False
        for params in self.param_list[self.seq_ind:]:
            # set procedure parameters #
            for pkey, pval in params.items():
                setattr(self.procedure, self.procedure.parameter_map[pkey], pval)
            log_str = f"{self.name}: starting procedure {self.procedure.name} at index {self.seq_ind}"
            #logger.info(log_str)
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
