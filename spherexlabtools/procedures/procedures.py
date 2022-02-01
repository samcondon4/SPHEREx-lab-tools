""" This module implements a set of ubiquitous procedure classes for measurement execution. These
    classes include:

        - :class:`.BasicProc`

Sam Condon, 01/31/2022
"""

import threading
from pymeasure.experiment import Procedure
from pymeasure.experiment import FloatParameter
from ..log import Logger


class BaseProcedure(Procedure):
    """ Subclass of the pymeasure procedure.
    """

    def __init__(self, hw, viewer=None, recorder=None, log=None):
        """ Initialize a bare procedure instance.

        :param: hw: Every procedure in the spherexlabtools framework needs an instrument object. This argument
                    is that object.
        :param: viewer: Viewer object for procedure data to be sent to.
        :param: recorder: Recorder object for procedure data to be sent to.
        :param: log: Logger object.
        """
        super().__init__()
        self.hw = hw
        self.topics = []
        if viewer is not None:
            self.topics.append("view")
        if recorder is not None:
            self.topics.append("record")
        self.viewer = viewer
        self.recorder = recorder
        self.logger = Logger(log)


class LogProc(BaseProcedure):
    """ Basic procedure that continuously records a parameter at a defined refresh rate and
        sends it to a :class:`..recorders.Recorder`, a :class:`..viewers.Viewer`, or both
        with calls to :meth:`..workers.FlexibleWorker.emit` which is monkey patched into
        all procedure classes upon execution.
    """

    refresh_rate = FloatParameter("Refresh Rate", units="Hz.")
    DATA_COLUMNS = []

    def __init__(self, hw, props, **kwargs):
        """ Initialize a basic procedure that will record data from the prop argument.

        :param: hw: Instrument object
        :param: props String or list of strings of instrument property or properties to get data from.
        """
        super().__init__(hw, **kwargs)
        self.DATA_COLUMNS = props if len(props) > 1 else [props]

    def execute(self):
        """ Procedure execution method. Calls get_properties() at a fixed interval.
        """
        while not self.should_stop():
            threading.Timer(1/self.refresh_rate, self.get_properties).start()

    def get_properties(self):
        """ Retrieve all properties given in the DATA_COLUMNS list and emit results.
        """
        data = {}
        for p in self.DATA_COLUMNS:
            data[p] = getattr(self.hw, p)
        self.logger.log("Emitting values from: {}".format(self.DATA_COLUMNS))
        self.emit(self.topics, data)


def create_procedures(cfgs, hw, viewers=None, recorders=None, log=None):
    """ Create a set of procedures.

    :param: cfgs: List of procedure configuration dictionaries.
    :param: hw: InstrumentSuite object.
    :param: viewers: Dictionary of instantiated viewers.
    :param: recorders: Dictionary of instantiated recorders.
    """
    procedures = {}
    for cfg in cfgs:
        hw_obj = getattr(hw, cfg["hw"])
        viewer = None if "viewer" not in cfg.keys() else viewers[cfg["viewer"]]
        recorder = None if "recorder" not in cfg.keys() else recorders[cfg["recorder"]]
        if cfg["type"] == "LogProc":
            procedures["instance_name"] = LogProc(hw_obj, cfg["props"], viewer=viewer, recorder=recorder, log=log)

    return procedures
