""" This module implements a set of ubiquitous procedure classes for measurement execution. These
    classes include:

        - :class:`.BasicProc`

Sam Condon, 01/31/2022
"""

import time
import inspect
from copy import deepcopy

from pymeasure.experiment import Procedure
from pymeasure.experiment import Parameter, FloatParameter
from pymeasure.thread import StoppableThread

from ..log import Logger


class BaseProcedure(Procedure):
    """ Thread to execute a measurement. Based on the pymeasure procedure.
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

    def __init__(self, hw, records=None, log=None, **kwargs):
        """ Initialize a bare procedure instance.

        :param: hw: Every procedure in the spherexlabtools framework needs an instrument object. This argument
                    is that object.
        :param: records: Dictionary containing lists of queues to which data should be posted on
                         calls to emit().
        :param: log: Logger object.
        """
        super().__init__(**kwargs)
        self.hw = hw
        self.records = records
        self.logger = Logger(log)
        self.running = False

    def emit(self, record_name, record_data):
        """ Post a record to the appropriate queues.
        """
        for q in self.records[record_name]:
            q.put(record_data)


class LogProc(BaseProcedure):
    """ Basic procedure that continuously records a parameter at a defined refresh rate and
        sends it to a :class:`..recorders.Recorder`, a :class:`..viewers.Viewer`, or both
        with calls to :meth:`..workers.FlexibleWorker.emit` which is monkey patched into
        all procedure classes upon execution.
    """

    refresh_rate = FloatParameter("Log Rate", units="Hz.", default=1)

    def __init__(self, hw, **kwargs):
        """ Initialize a basic procedure that will record data from the prop argument.

        :param: hw: Instrument object
        :param: props String or list of strings of instrument property or properties to get data from.
        """
        super().__init__(hw, **kwargs)
        self.DATA_COLUMNS = list(self.records.keys())

    def execute(self):
        """ Procedure execution method. Calls get_properties() to start recording props at a fixed interval.
        """
        print(self.refresh_rate)
        while self.running:
            self.get_properties()
            time.sleep(1/self.refresh_rate)

    def get_properties(self):
        """ Retrieve all properties given in the DATA_COLUMNS list and emit results.
        """
        for p in self.DATA_COLUMNS:
            data = getattr(self.hw, p)
            self.emit(p, data)


def create_procedures(cfgs, hw, viewers=None, recorders=None, log=None):
    """ Create a set of procedures.

    :param: cfgs: List of procedure configuration dictionaries.
    :param: hw: InstrumentSuite object.
    :param: viewers: Dictionary of instantiated viewers.
    :param: recorders: Dictionary of instantiated recorders.
    """
    procedures = {}
    for cfg in cfgs:
        # get hardware object #
        hw_obj = getattr(hw, cfg["hw"])

        # get recorder and viewer queues to pass to the procedure base #
        records = cfg["records"]
        qdict = {}
        for key, val in records.items():
            qdict_val = [{"viewer": viewers, "recorder": recorders}[k][v].queue for k, v in val.items()]
            qdict[key] = qdict_val

        # instantiate the procedure, placing it in the returned dictionary #
        if cfg["type"] == "LogProc":
            procedures[cfg["instance_name"]] = LogProc(hw_obj, records=qdict, log=log)

    return procedures
