""" spherexlabtools.controllers.controller

Sam Condon, 01/27/2022
"""
import time
import logging
import threading

from PyQt5 import QtWidgets, QtCore
from pymeasure.experiment.parameters import *
from pyqtgraph.parametertree import Parameter, ParameterTree

from ..widgets import Sequencer
from ..procedures import BaseProcedure
from ..parameters import ParameterInspect
from ..thread import StoppableReusableThread

logger = logging.getLogger(__name__)


class Controller(QtWidgets.QWidget):
    """ Base-class for the controller objects.
    """

    def __init__(self, cfg, exp, hw=None, procs=None):
        super().__init__()
        self.name = cfg["instance_name"]
        self.exp = exp
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

    refresh_timer = QtCore.QTimer()
    params_set = QtCore.pyqtSignal()

    def __init__(self, cfg, exp, hw, **kwargs):
        """ Initialize the InstrumentController Widget as a pyqtgraph parameter tree.

        :param: name: Name of the controller.
        :param: hw: Instrument driver.
        :param: control_params: list of parameter configuration dictionaries.
        :param: status_params: list of status configuration dictionaries.
        :param: status_refresh: seconds between updates to the status parameters, or can be the string "after_set",
                                so that parameters are only ever updated after they are set to new values.
        """
        super().__init__(cfg, exp, **kwargs)
        self.hw = getattr(hw, cfg["hw"])
        params = []

        # configure control parameters if they are present. #
        self.set_buttons = None
        self.control_group = None
        self.set_params = None
        self.set_processes = {}
        self._configure_control_parameters(cfg.get("control_parameters", []))
        if self.control_group is not None:
            params.append(self.control_group)

        # configure status parameters if they are present #
        self.status_refresh_button = None
        self.status_group = None
        self.status_names = None
        self.status_refresh = None
        self.get_processes = {}
        if "status_parameters" in cfg.keys():
            status_dict = {key: cfg[key] for key in ["status_parameters", "status_refresh"]}
            self._configure_status_parameters(status_dict)
            params.append(self.status_group)

        # create action buttons if present in the configuration ###############
        self.actions_group = None
        actions = cfg.get("actions", [])
        if len(actions) > 0:
            self.actions_group = Parameter.create(name="Actions", type="group",
                                                  children=[Parameter.create(type="action", name=a) for a in actions])
            params.append(self.actions_group)

        # complete the final configurations #
        self.set_parameters(params, showTop=True)
        self._configure_buttons()

    def set_inst_params(self, children):
        """ Write instrument control parameters to the hardware.

        :param children: List of gui children names to set instrument values from.
        """
        if self.alive:
            for c in children:
                child = self.control_group.child(c)
                if child is not self.set_params:
                    name = child.name()
                    value = self.set_processes[name](child)
                    logger.debug("Setting instrument parameter {} with value {}".format(name, value))
                    setattr(self.hw, name, value)
            self.params_set.emit()

    def get_inst_params(self):
        """ Get instrument parameters and write them to GUI elements.
        """
        if self.alive:
            for c in self.status_group.children():
                param = c.name()
                logger.debug("Getting instrument parameter %s" % param)
                if param in self.status_names:
                    val = self.get_processes[param](getattr(self.hw, param))
                    logger.debug(f"Got {val}")
                    if val != self.status_values[param]:
                        self.status_values[param] = val
                        c.setValue(val)

    def run_instrument_action(self, action):
        """ Run an instrument method from a new thread.

        :param action: String name of the method to run.
        """
        logger.debug("Running action %s on instrument %s" % (action, str(self.hw)))
        act = getattr(self.hw, action)
        act()

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
        self.refresh_timer.stop()
        self.close()

    def _configure_control_parameters(self, control_params):
        """ Configure the set of instrument control parameters.

        :param control_params: List of configurations for the instrument control parameters.
        """
        self.set_buttons = [Parameter.create(name="Set", type="action") for p in control_params]
        if len(self.set_buttons) > 0:
            i = 0
            for param_cfg in control_params:
                set_proc = param_cfg.get("set_process", lambda child: child.value())
                self.set_processes[param_cfg["name"]] = set_proc
                if "children" in param_cfg.keys():
                    param_cfg["children"] = [Parameter.create(**child_dict) for child_dict in param_cfg["children"]]
                    param_cfg["children"].append(self.set_buttons[i])
                    param_cfg.update({"expanded": False})
                else:
                    param_cfg.update({"children": [self.set_buttons[i]], "expanded": False})
                i += 1
            self.set_params = Parameter.create(name="Set All Parameters", type="action")
            control_params.append(self.set_params)
            self.control_group = Parameter.create(name="Control", type="group", children=control_params)

    def _configure_status_parameters(self, status_dict):
        """ Configure the status parameter ui features.

        :param status_dict: Dictionary of the form {"status_parameters": list, "status_refresh": str}
        """
        status_params = status_dict["status_parameters"]
        self.status_refresh = status_dict["status_refresh"]
        sref_typ = type(self.status_refresh)
        self.status_names = [p["name"] for p in status_params]
        for param in status_params:
            get_proc = param.get("get_process", lambda v: v)
            self.get_processes[param["name"]] = get_proc
            param["enabled"] = False

        if sref_typ is float or sref_typ is int:
            logger.debug("Starting refresh timer for %f seconds" % self.status_refresh)
            thread = StoppableReusableThread()
            self.refresh_timer.timeout.connect(self.get_inst_params)
            self.refresh_timer.start(self.status_refresh)

        elif self.status_refresh == "after_set":
            logger.debug("Connecting params_set signal to get_inst_params")
            self.params_set.connect(self.get_inst_params)

        elif self.status_refresh == "manual":
            logger.debug("Connecting status_refresh_button to get_inst_params")
            self.status_refresh_button = Parameter.create(name="Refresh", type="action")
            self.status_refresh_button.sigActivated.connect(self.get_inst_params)
            status_params.append(self.status_refresh_button)

        self.status_group = Parameter.create(name="Status", type="group", children=status_params)
        self.status_values = {c.name(): c.value() for c in self.status_group.children()}

    def _configure_buttons(self):
        """ Connect buttons to the appropriate methods.
        """
        if self.control_group is not None:
            thread = StoppableReusableThread()
            thread.execute = lambda: self.set_inst_params([c.name() for c in self.control_group.children()])
            self.set_params.sigActivated.connect(
                self.exp.get_start_thread_lambda("%s: Set All Params" % self.name, thread))

            for c in self.control_group.children():
                if c is not self.set_params:
                    child_name = c.name()
                    logger.debug("Connecting set method for {}".format(child_name))
                    button = c.child("Set")
                    thread = StoppableReusableThread()
                    thread.execute = lambda child=child_name: self.set_inst_params([child])
                    button.sigActivated.connect(self.exp.get_start_thread_lambda(
                        "%s: Set %s" % (self.name, child_name), thread))

        if self.actions_group is not None:
            for c in self.actions_group.children():
                act_name = c.name()
                logger.debug("Connecting action method for {}".format(act_name))
                thread = StoppableReusableThread()
                thread.execute = lambda act=act_name: self.run_instrument_action(act)
                c.sigActivated.connect(self.exp.get_start_thread_lambda(
                    "%s: Action %s" % (self.name, act_name), thread
                ))


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

    def __init__(self, cfg, exp, procs, place_params=True, sequencer=True, records=True, connect=True, **kwargs):
        """ Initialize the procedure controller gui interface.

        :param name: String name of the controller.
        :param exp: Experiment object.
        :param procs: Procedure object to control.
        :param place_params: Boolean to indicate if the default parameter layout should be set.
        :param connect: Boolean to indicate if the start and stop procedure buttons should be connected to methods.
        :param sequencer: Boolean indicating if a sequencer interface should be generated.
        :param records: Boolean indicating if a record viewer/manipulating interface should be generated.
        """
        super().__init__(cfg, exp, **kwargs)
        if "place_params" in cfg.keys():
            place_params = cfg["place_params"]
        if "sequencer" in cfg.keys():
            sequencer = cfg["sequencer"]
        self.procedure = procs[cfg["procedure"]]
        self.proc_param_objs = ParameterInspect.parameter_objects(self)

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
        self.proc_seq_ind = 0
        self.procedure_sequence_thread = StoppableReusableThread()
        if sequencer:
            self.sequencer = Sequencer(self.proc_params_tree)

        # place parameters if flag is set #
        if place_params:
            self.proc_params.addChildren(self.proc_actions)
            params = [self.proc_params, self.sequencer] if self.sequencer is not None else [self.proc_params]
            self.set_parameters(params)

        # connect buttons to methods #
        if connect:
            self._connect_buttons()

    def start_procedure(self, params=None, log_msg=None):
        """ Start the procedure thread.

        :param params: Optional dictionary of parameter to run the procedure with. If not provided,
                       parameters from the single procedure execution tree will be used.
        :param log_msg: String specifying a log message to write at the INFO level.
        """
        if params is None:
            for c in self.proc_params.children():
                name = c.name()
                if name in self.param_name_map.keys():
                    setattr(self.procedure, self.param_name_map[c.name()], c.value())
        else:
            for key, value in params.items():
                setattr(self.procedure, self.param_name_map[key], value)

        # start the procedure #
        if log_msg is not None:
            logger.info(log_msg)
        self.procedure.start()

    def stop_procedure(self, timeout=1):
        """ Stop the running procedure thread.
        """
        logger.info("%s stopping procedure" % self.name)
        self.procedure.stop()

    def start_procedure_sequence(self, seq, sleep=2):
        """ Start a sequence of procedures with parameters built by the sequencer widget.

        :param seq: List of procedure parameters.
        :param sleep: Time in seconds to sleep between checking if the procedure sequence is complete.
        """
        logger.info("%s: Starting procedure sequence of length %i" % (self.name, len(seq)))
        if self.proc_seq_ind != 0:
            seq = None
        self.procedure_sequence_thread.execute = lambda s=seq, sl=sleep: self._proc_seq_thread_target(seq=seq,
                                                                                                      sleep=sl)
        self.procedure_sequence_thread.start()

    def stop_procedure_sequence(self):
        """ Stop a currently running procedure sequence.
        """
        if self.procedure.status == BaseProcedure.RUNNING:
            self.procedure.stop()
        self.proc_seq_ind = 0

    def pause_procedure_sequence(self):
        """ Stop a currently running procedure sequence without resetting the sequence index.
        """
        if self.procedure.status == BaseProcedure.RUNNING:
            self.procedure.stop()

    def _proc_seq_thread_target(self, seq=None, sleep=2):
        """ Method that is the target of the procedure_sequence_thread.

        :param seq: List of procedure parameters.
        :param ind: Index into a procedure sequence for when a sequence has been paused.
        :param sleep: Time in seconds to sleep between checking if an individual procedure is complete.
        """
        if seq is not None:
            self.proc_seq = seq
            self.proc_seq_ind = 0
        while self.proc_seq_ind < len(self.proc_seq):
            proc = self.proc_seq[self.proc_seq_ind]
            log_msg = "%s: Starting procedure at sequence index %s" % (self.name, str(self.proc_seq_ind))
            self.proc_seq_ind += 1
            self.start_procedure(proc, log_msg=log_msg)
            while not self.procedure.status == self.procedure.FINISHED:
                time.sleep(sleep)
                if self.procedure_sequence_thread.should_stop():
                    self.stop_procedure()
                    break
        if self.proc_seq_ind >= len(self.proc_seq):
            self.proc_seq_ind = 0

    def _connect_buttons(self):
        """ Connect the start/stop buttons to the appropriate methods.
        """
        self.start_proc.sigActivated.connect(lambda a: self.start_procedure(params=None, log_msg="%s: Starting single"
                                                                                                 "procedure" %
                                                                                                 self.name))
        self.stop_proc.sigStateChanged.connect(lambda a: self.stop_procedure())

        if self.sequencer is not None:
            self.sequencer.new_sequence.connect(lambda seq: self.start_procedure_sequence(seq))
            self.sequencer.abort_proc_sequence.connect(self.stop_procedure_sequence)


class LogProcController(ProcedureController):
    """ Controller class to implement control over a procedure through a GUI.
    """

    def __init__(self, cfg, exp, procs, **kwargs):
        super().__init__(cfg, exp, procs, place_params=False, sequencer=False, connect=False,
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
