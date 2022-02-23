""" spherexlabtools.controllers.controller

Sam Condon, 01/27/2022
"""
import time
import logging
import threading
import importlib

from PyQt5 import QtWidgets, QtCore
from pymeasure.experiment.parameters import *
from pyqtgraph.parametertree import Parameter, ParameterTree

from ..widgets import Sequencer


logger = logging.getLogger(__name__)


class Controller(QtWidgets.QWidget):
    """ Base-class for the controller objects.
    """

    def __init__(self, cfg, hw=None, procs=None):
        super().__init__()
        self.name = cfg["instance_name"]
        self.alive = False
        self.parameters = Parameter.create(name=self.name, type="group")
        self.tree = ParameterTree()
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

    def set_parameters(self, params, **kwargs):
        """ Set the children of the parameters attribute and update the tree and
            layout.

        :param: params: List of children to add to the parameter tree.
        :param: showTop: boolean to indicate if the top-level parameter should be shown.
        :param: **kwargs: Key-word arguments for tree.setParameters
        """
        self.parameters.addChildren(params)
        self.tree.setParameters(self.parameters, **kwargs)
        self.layout.addWidget(self.tree)

    def start(self):
        """ Start the controller.
        """
        self.alive = True
        self.show()

    def stop(self):
        """ Stop the controller.
        """
        self.alive = False
        self.close()


class InstrumentController(Controller):
    """ Controller class to implement manual control over an individual instrument within a GUI.
    """

    def __init__(self, cfg, hw, **kwargs):
        """ Initialize the InstrumentController Widget as a pyqtgraph parameter tree.

        :param: name: Name of the controller.
        :param: hw: Instrument driver.
        :param: control_params: list of parameter configuration dictionaries.
        :param: status_params: list of status configuration dictionaries.
        :param: status_refresh: seconds between updates to the status parameters.
        """
        super().__init__(cfg, **kwargs)
        self.hw = getattr(hw, cfg["hw"])
        params = []

        # configure control parameters if they are present. #
        control_params = cfg["control_parameters"]
        self.set_buttons = [Parameter.create(name="Set", type="action") for p in control_params]
        self.control_group = None
        if len(control_params) > 0:
            # create set buttons #
            for i in range(len(control_params)):
                control_params[i].update({"children": [self.set_buttons[i]], "expanded": False})
            self.set_params = Parameter.create(name="Set All Parameters", type="action")
            control_params.append(self.set_params)
            self.control_group = Parameter.create(name="Control", type="group", children=control_params)
            params.append(self.control_group)

        # configure status parameters if they are present #
        status_params = cfg["status_parameters"]
        self.status_group = None
        if len(status_params) > 0:
            for p in status_params:
                p["enabled"] = False
            self.status_group = Parameter.create(name="Status", type="group", children=status_params)
            self.status_values = {c.name(): c.value() for c in self.status_group.children()}
            params.append(self.status_group)

        # parameter tree #
        self.set_parameters(params, showTop=True)

        # Threading setup #
        self.get_timer = None
        self.status_refresh = 0 if "status_refresh" not in cfg.keys() else cfg["status_refresh"]

        # connect buttons to methods #
        self.set_params.sigActivated.connect(lambda _, children=self.control_group.children():
                                             self.set_inst_params([c.name() for c in children]))
        if self.control_group is not None:
            for c in self.control_group.children():
                if c is not self.set_params:
                    name = c.name()
                    logger.debug("Connecting set method for {}".format(name))
                    button = c.child("Set")
                    button.sigActivated.connect(lambda _, child=name: self.set_inst_params([child]))

    def set_inst_params(self, children):
        """ Write instrument control parameters to the hardware.

        :param children: List of gui children names to set instrument values from.
        """
        if self.alive:
            for c in children:
                child = self.control_group.child(c)
                if child is not self.set_params:
                    name = child.name()
                    value = child.value()
                    logger.debug("Setting instrument parameter {} with value {}".format(name, value))
                    setattr(self.hw, name, value)

    def get_inst_params(self):
        """ Get instrument parameters and write them to GUI elements. Start timer threads that periodically
            execute this method.
        """
        if self.alive:
            for c in self.status_group.children():
                param = c.name()
                val = getattr(self.hw, param)
                if val != self.status_values[param]:
                    self.status_values[param] = val
                    c.setValue(val)
            self.get_timer = threading.Timer(self.status_refresh, self.get_inst_params)
            self.get_timer.start()

    def start(self):
        """ Start the controller.
        """
        self.alive = True
        self.show()
        if self.status_refresh is not None:
            self.get_inst_params()

    def stop(self):
        """ Kill the controller.
        """
        self.alive = False
        self.get_timer.cancel()
        self.close()


class ProcedureController(Controller):
    """ Base class for a procedure controller object.
    """

    # map from pymeasure parameter type to pyqtgraph parameter tree type #
    parameter_map = {
        FloatParameter: "float",
        IntegerParameter: "int",
        BooleanParameter: "bool",
    }

    proc_complete = QtCore.pyqtSignal()

    def __init__(self, cfg, procs, place_params=True, sequencer=True, connect=True, **kwargs):
        """ Initialize the procedure controller gui interface.

        :param name: String name of the controller.
        :param procs: Procedure object to control.
        :param place_params: Boolean to indicate if the default parameter layout should be set.
        :param connect: Boolean to indicate if the start and stop procedure buttons should be connected to methods.
        :param sequencer: Boolean indicating if a sequencer interface should be generated.
        """
        super().__init__(cfg, **kwargs)
        if "place_params" in cfg.keys():
            place_params = cfg["place_params"]
        if "sequencer" in cfg.keys():
            sequencer = cfg["sequencer"]
        self.procedure = procs[cfg["procedure"]]
        self.proc_param_objs = self.procedure.parameter_objects()

        # create parameter dictionaries for the procedure parameters #
        j = 0
        self.proc_params_tree = [{} for _ in range(len(self.proc_param_objs.keys()))]
        self.param_name_map = {}
        for key, val in self.proc_param_objs.items():
            self.param_name_map[val.name] = key
            self.proc_params_tree[j] = {"name": val.name, "type": self.parameter_map[type(val)], "value": val.value}
            j += 1
        self.proc_params = Parameter.create(name="Procedure Params", type="group", children=self.proc_params_tree)

        # create start and stop procedure buttons #
        self.start_proc = Parameter.create(name="Start Procedure", type="action")
        self.stop_proc = Parameter.create(name="Stop Procedure", type="action")
        self.proc_actions = [self.start_proc, self.stop_proc]

        # create the sequencer parameter group if the sequencer boolean is true #
        self.sequencer = None
        self.proc_seq = None
        self.proc_seq_ind = None
        if sequencer:
            self.sequencer = Sequencer(self.proc_params_tree)
            self.sequencer.new_sequence.connect(lambda seq: self.run_procedure_sequence(seq))

        # place parameters if flag is set #
        if place_params:
            self.proc_params.addChildren(self.proc_actions)
            params = [self.proc_params, self.sequencer] if self.sequencer is not None else [self.proc_params]
            self.set_parameters(params)

        # connect buttons to methods #
        if connect:
            self._connect_buttons()

    def start_procedure(self, params=None, monitor=False):
        """ Start the procedure thread.

        :param params: Optional dictionary of parameter to run the procedure with. If not provided,
                       parameters from the single procedure execution tree will be used.
        :param monitor: Optional boolean to indicate a monitor thread should be run to emit a QSignal
                        when the procedure completes execution.
        """
        if params is None:
            log_msg = "%s starting single procedure: %s" % (self.name, self.procedure)
            for c in self.proc_params.children():
                name = c.name()
                if name in self.param_name_map.keys():
                    setattr(self.procedure, self.param_name_map[c.name()], c.value())
        else:
            log_msg = "%s starting sequence index %s procedure: %s" % \
                      (self.name, self.proc_seq_ind, self.procedure)
            for key, value in params.items():
                setattr(self.procedure, self.param_name_map[key], value)

        # start the procedure #
        logger.info(log_msg)
        self.procedure.start()
        if monitor:
            threading.Thread(target=self.proc_monitor).start()

    def proc_monitor(self, sleep=0.5):
        """ Monitor a running procedure and emit the complete signal when it is finished.

        :param sleep: Interval between checks on if procedure is complete.
        """
        logger.debug("proc_monitor started!")
        while not self.procedure.status == self.procedure.FINISHED:
            time.sleep(sleep)
        logger.debug("proc_monitor emitting procedure complete!")
        self.proc_complete.emit()

    def stop_procedure(self, timeout=1):
        """ Stop the running procedure thread.
        """
        logger.info("%s stopping procedure: %s" % (self.name, self.procedure))
        self.procedure.stop()

    def run_procedure_sequence(self, seq=None):
        """ Start a sequence of procedures with parameters built by the sequencer widget.

        :param seq: List of procedure parameters.
        """
        # set up execution of a procedure sequence #
        if seq is not None and self.proc_seq is None:
            logger.info("%s: Starting procedure sequence of length %i" % (self.name, len(seq)))
            self.proc_seq = seq
            self.proc_seq_ind = 0
            self.proc_complete.connect(lambda: self.run_procedure_sequence(seq=None))
        else:
            logger.debug("Incrementing procedure sequence index.")
            self.proc_seq_ind += 1

        # start the next procedure in the sequence if the sequence is not yet complete #
        if self.proc_seq_ind < len(self.proc_seq):
            params = self.proc_seq[self.proc_seq_ind]
            self.start_procedure(params=params, monitor=True)
        else:
            logger.info("%s: Starting procedure sequence of length %i" % (self.name, len(seq)))
            self.proc_complete.disconnect()

    def stop_procedure_sequence(self):
        """ Stop a currently running procedure sequence.
        """
        pass

    def _connect_buttons(self):
        """ Connect the start/stop buttons to the appropriate methods.
        """
        self.start_proc.sigStateChanged.connect(lambda a: self.start_procedure(params=None, monitor=False))
        self.stop_proc.sigStateChanged.connect(lambda a: self.stop_procedure())


class LogProcController(ProcedureController):
    """ Controller class to implement control over a procedure through a GUI.
    """

    def __init__(self, cfg, procs, **kwargs):
        super().__init__(cfg, procs, place_params=False, sequencer=False, connect=False,
                         **kwargs)

        # configure parameter tree #
        proc_dcols = self.procedure.DATA_COLUMNS
        self.log_params = [{"name": col, "type": "bool", "value": False} for col in proc_dcols]
        self.dcol_param_group = Parameter.create(name="Log Parameters", type="group", children=self.log_params)

        self.proc_params.addChild(self.dcol_param_group)

        params = [self.proc_params]
        params.extend(self.proc_actions)
        # build widget #
        self.set_parameters(params, showTop=True)

        # connect buttons to methods #
        self._connect_buttons()
