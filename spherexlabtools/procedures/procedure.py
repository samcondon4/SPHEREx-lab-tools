""" This module implements a set of basic procedure classes for measurement execution.
"""
import os
import time
import logging
import datetime
import threading

import numpy as np
import pandas as pd
from pyqtgraph.parametertree import Parameter, ParameterTree

import spherexlabtools.log as slt_log
from spherexlabtools.record import Record
from spherexlabtools.ui.record import RecordUI
from spherexlabtools.thread import StoppableReusableThread
from spherexlabtools.parameters import ParameterInspect, Parameter, FloatParameter, IntegerParameter, BooleanParameter


log_name = f"{slt_log.LOGGER_NAME}.{__name__.split('.')[-1]}"
logger = logging.getLogger(log_name)


class Procedure(StoppableReusableThread):
    """ Thread to execute a measurement. Largely based on the pymeasure procedure class.
    """

    FINISHED, FAILED, ABORTED, QUEUED, RUNNING = 0, 1, 2, 3, 4
    STATUS_STRINGS = {
        FINISHED: 'Finished', FAILED: 'Failed',
        ABORTED: 'Aborted', QUEUED: 'Queued',
        RUNNING: 'Running'
    }
    parameters = {}

    def __init__(self, cfg, exp, hw=None, update_params=True, viewers=None, recorders=None, **kwargs):
        """ Initialize a bare procedure instance.

        :param hw: :class:`..instruments.InstrumentSuite` object.
        :param exp: Experiment object. Used for compatibility with general class loader.
        :param update_params: Boolean to indicate if self._update_parameters() should run in this init.
        :param viewers: Dictionary of Viewer objects.
        :param recorders: Dictionary of recorder objects.
        :param kwargs: Key-word arguments to set the procedure parameters.
        """
        logger.info(slt_log.INIT_MSG % cfg["instance_name"])

        # - initialize the procedure object - #
        super().__init__()
        self.name = cfg["instance_name"]
        self.exp = exp
        self.hw = cfg.get("hw", None)
        self.records = {}
        self.record_queues = {}
        self.status = Procedure.QUEUED
        self.proc_params = {}
        self.start_time = None
        self.sequence = None

        # - configure the hardware attribute - #
        if type(self.hw) is list:
            hw_obj = type("hw", (object,), {})
            for inst in self.hw:
                setattr(hw_obj, inst, getattr(hw, inst))
            self.hw = hw_obj
        elif self.hw is not None:
            self.hw = getattr(hw, self.hw)

        # - configure the records and record queues - #
        for key, val in cfg["records"].items():
            val_dict = {vkey: vval for vkey, vval in val.items()}
            kwargs_dict = {}
            for vkey in list(val_dict.keys()):
                if vkey not in ["viewer", "recorder"]:
                    kwargs_dict[vkey] = val_dict.pop(vkey)
            view_rec_val = {k: {"viewer": self.exp.viewers, "recorder": self.exp.recorders}[k][v] for k, v in
                            val_dict.items()}
            qdict_val = [comp.queue for comp in view_rec_val.values()]
            kwargs_dict.update({k: v for k, v in view_rec_val.items()})
            self.record_queues[key] = qdict_val
            self.records[key] = Record(key, **kwargs_dict)
        if update_params:
            ParameterInspect.update_parameters(self)
        for key in kwargs:
            if key in self.parameters.keys():
                setattr(self, key, kwargs[key])
        self.parameter_map = {pval.name: pkey for pkey, pval in self.parameters.items()}

        # - configure the records user-interface - #
        self.records_interface = RecordUI(self.records)
        self.records_interface_tree = ParameterTree()
        setattr(self.records_interface_tree, "name", self.name)
        self.records_interface_tree.setParameters(self.records_interface)
        logger.info(slt_log.CMPLT_MSG % f"{self.name} initialization")

    def startup(self):
        """ Check that all procedure parameters have been set, and set the start_time object.
        """
        self.status = Procedure.RUNNING
        ParameterInspect.check_parameters(self)
        self.proc_params = ParameterInspect.parameter_values(self)
        self.start_time = datetime.datetime.now()

    def emit(self, record_name, record_data, meta=None, filepath=None, **kwargs):
        """ Post a record to the appropriate queues.

        :param record_name: String name of the record.
        :param record_data: Data values to write to the record.
        :param meta: Metadata values to write to the record.
        :param filepath: String filepath to where the record should be saved if connected to a recorder.
        :param kwargs: Key-word arguments for record updating.
        """
        # - get the record and attributes to be updated - #
        record = self.records[record_name]
        if filepath is not None:
            record.filepath = filepath
        if self.sequence is None:
            proc_start_time = self.start_time
        else:
            proc_start_time = self.sequence.start_time

        # - update the record and place it on all associated queues - #
        record.update(record_data, proc_params=self.proc_params, meta=meta, proc_start_time=proc_start_time, **kwargs)
        for q in self.record_queues[record_name]:
            q.put(record)

    def shutdown(self):
        """ Set the procedure finished value.
        """
        self.status = Procedure.FINISHED

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


class LoggingProcedure(Procedure):
    """ This class provides basic logging of instrument parameters. It contains the following Procedure Parameters:

    - sample_rate: The rate in hz to query instruments for new data.
    - record_rows: How many rows of instrument data should be recorded before a call to emit()?
    - iterations: How many times to run the log. Set to 0 for continuous logging.

    Currently, logging to just a single record is supported.
    """

    sample_rate = FloatParameter('Sample Rate', units='hz', default=1)
    record_rows = IntegerParameter('Record Rows', default=1)
    iterations = IntegerParameter('Iterations', default=0)

    def __init__(self, cfg, exp, data, meta, **kwargs):
        """ Initialize a basic logging procedure.

        :param cfg: Configuration dictionary.
        :param exp: Experiment control package.
        :param data: Dictionary of the form: {'instrument-name': [list of parameters to record from the instrument in the data table]}
        :param meta: Dictionary of the form: {'instrument-name': [list of parameters to record from the instrument in the meta-data table]}
        :param kwargs:
        """
        assert len(cfg['records'].keys()) == 1, 'One and only one record is currently supported by the base LoggingProcedure.'
        super().__init__(cfg, exp, **kwargs)
        self.record = list(cfg['records'].keys())[0]
        self.data_params = [(key, val[i]) for key, val in data.items() for i in range(len(val))]
        self.meta_params = [(key, val[i]) for key, val in meta.items() for i in range(len(val))]
        self.data_df = None
        self.meta_df = None
        self.continuous = False

    def startup(self):
        """ Populate the metadata dictionary.
        """
        super().startup()
        # - populate the metadata dataframe for the procedure execution - #
        self.meta_df = pd.DataFrame({
            param: [0] for inst, param in self.meta_params
        })
        self.populate_log_row(self.hw, self.meta_df, self.meta_params, 0)

        # - check if we should run in continuous mode - #
        self.continuous = True if self.iterations == 0 else False
        if self.continuous:
            self.iterations += 1

        # - initialize a new data dataframe - #
        self.data_df = pd.DataFrame({
            param: np.arange(self.record_rows) for inst, param in self.data_params
        })

    def execute(self):
        """ Run the log.
        """
        i = 0
        while i < self.iterations:
            if self.should_stop():
                break

            # - populate the data dataframe - #
            for j in range(self.record_rows):
                self.populate_log_row(self.hw, self.data_df, self.data_params, j)
                time.sleep(1 / self.sample_rate)
            self.emit(self.record, self.data_df, meta=self.meta_df)

            # - if we aren't in continuous mode, then add to the iterator - #
            if not self.continuous:
                i += 1

    @staticmethod
    def populate_log_row(hw, log_dict, param_list, index):
        """ Populate the data or metadata dictionary row with parameter values.

        :param hw: Hardware object.
        :param log_dict: The dictionary to populate.
        :param param_list: List of tuples with the instrument name and parameter to query.
        :param index: Index of the dictionary row to populate.
        :return:
        """
        for inst, param in param_list:
            inst_obj = getattr(hw, inst)
            param_val = getattr(inst_obj, param)
            log_dict[param][index] = param_val


class ProcedureSequence(Procedure):
    """ Procedure class that wraps and executes a standalone procedure in a loop.
    """

    param_list = Parameter("Parameter List")
    sleep = FloatParameter("Sleep Interval", default=1, units="s.")
    seq_ind = 0

    def __init__(self, cfg, exp, proc, **kwargs):
        super().__init__(cfg, exp, **kwargs)
        self.procedure = proc

    def startup(self):
        """ Set the sequence attribute of the procedure attribute.
        """
        super().startup()
        self.procedure.sequence = self

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
