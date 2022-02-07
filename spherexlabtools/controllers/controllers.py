""" spherexlabtools.controllers.controller

Sam Condon, 01/27/2022
"""
import threading
import importlib
from PyQt5 import QtWidgets
from pymeasure.experiment.parameters import *
from pyqtgraph.parametertree import Parameter, ParameterTree

from ..log import Logger
from ..widgets import Sequencer


class Controller(QtWidgets.QWidget):
    """ Base-class for the controller objects.
    """

    def __init__(self, name, hw=None, proc=None, log=None):
        super().__init__()
        # logging setup #
        self.name = name
        self.alive = False
        self.logger = Logger(__name__ + ": %s" % name, log)
        self.parameters = Parameter.create(name=name, type="group")
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

    def __init__(self, name, cfg, hw, **kwargs):
        """ Initialize the InstrumentController Widget as a pyqtgraph parameter tree.

        :param: name: Name of the controller.
        :param: hw: Instrument driver.
        :param: control_params: list of parameter configuration dictionaries.
        :param: status_params: list of status configuration dictionaries.
        :param: status_refresh: seconds between updates to the status parameters.
        :param: log: Dictionary of the form {"level": log level,
                                             "handler": logging file handler}
        """
        super().__init__(name, **kwargs)
        self.hw = hw
        params = []

        # configure control parameters if they are present. #
        control_params = cfg["control_parameters"]
        self.control_group = None
        if len(control_params) > 0:
            self.set_params = Parameter.create(name="Set Parameters", type="action")
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
        self.set_params.sigStateChanged.connect(self.set_inst_params)

    def set_inst_params(self):
        """ Write instrument control parameters to the hardware.
        """
        if self.alive:
            for c in self.control_group.children():
                param = c.name()
                val = c.value()
                if param != "Set Parameters":
                    self.logger.log("Setting control parameter %s to %s" % (param, str(val)))
                    setattr(self.hw, param, val)

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
                    self.logger.log("Updating status parameter %s to %s" % (param, val))
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
        self.logger.log("started")

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

    def __init__(self, name, cfg, proc, place_params=True, sequencer=True, **kwargs):
        """ Initialize the procedure controller gui interface.

        :param: name: String name of the controller.
        :param: proc: Procedure object to control.
        :param: place_params: Boolean to indicate if the default parameter layout should be set.
        :param: sequencer: Boolean indicating if a sequencer interface should be generated.
        :param: log: Logging config dictionary.
        """
        super().__init__(name, **kwargs)
        if "place_params" in cfg.keys():
            place_params = cfg["place_params"]
        if "sequencer" in cfg.keys():
            sequencer = cfg["sequencer"]
        self.procedure = proc
        self.proc_param_objs = proc.parameter_objects()

        # create parameter dictionaries for the procedure parameters #
        j = 0
        self.proc_params_tree = [{} for _ in range(len(self.proc_param_objs.keys()))]
        self.param_name_map = {}
        for key, val in self.proc_param_objs.items():
            self.param_name_map[val.name] = key
            self.proc_params_tree[j] = {"name": val.name, "type": self.parameter_map[type(val)], "value": val.value}
            j += 1
        self.proc_params = Parameter.create(name="Single Procedure", type="group", children=self.proc_params_tree)

        # create start and stop procedure buttons #
        self.start_proc = Parameter.create(name="Start Procedure", type="action")
        self.stop_proc = Parameter.create(name="Abort Procedure", type="action")
        self.proc_actions = [self.start_proc, self.stop_proc]

        # create the sequencer parameter group if the sequencer boolean is true #
        self.sequencer = None
        if sequencer:
            self.sequencer = Sequencer(self.proc_params_tree)

        # place parameters if flag is set #
        if place_params:
            self.proc_params.addChildren(self.proc_actions)
            params = [self.proc_params, self.sequencer] if self.sequencer is not None else [self.proc_params]
            self.set_parameters(params)

        # connect buttons to methods #
        self.start_proc.sigStateChanged.connect(self.start_procedure)
        self.stop_proc.sigStateChanged.connect(self.stop_procedure)

    def start_procedure(self):
        """ Start the procedure thread.
        """
        # set the procedure parameters #
        for c in self.proc_params.children():
            if c not in self.proc_actions:
                setattr(self.procedure, self.param_name_map[c.name()], c.value())
        # start the procedure #
        self.procedure.start()

    def stop_procedure(self, timeout=1):
        """ Stop the running procedure thread.
        """
        self.procedure.stop()


class LogProcController(ProcedureController):
    """ Controller class to implement control over a procedure through a GUI.
    """

    def __init__(self, name, cfg, proc, **kwargs):
        super().__init__(name, cfg, proc, place_params=False, sequencer=False, **kwargs)

        # configure parameter tree #
        proc_dcols = self.procedure.DATA_COLUMNS
        log_params = [{} for _ in range(len(proc_dcols))]
        for i in range(len(log_params)):
            log_params[i] = {"name": proc_dcols[i], "type": "bool", "value": False}
        self.dcol_param_group = {"name": "Log Parameters:", "type": "group", "children": log_params}
        self.start_proc = Parameter.create(name="Start Logging", type="action")
        self.stop_proc = Parameter.create(name="Stop Logging", type="action")
        self.sub_params_tree = [self.dcol_param_group, self.start_proc, self.stop_proc]

        # build widget #
        params = []
        params.extend(self.sub_params_tree)
        params.append(self.proc_params)
        self.set_parameters(params, showTop=True)

        # connect buttons to methods #
        self.stop_proc.sigStateChanged.connect(self.stop_procedure)
        self.start_proc.sigStateChanged.connect(self.start_procedure)


def create_controllers(exp_pkg, hw=None, procedures=None, log=None):
    """ Create a set of controller objects from a list of configuration dictionaries, an InstrumentSuite object,
        a set of procedures, viewers, and recorders.

    :param: exp_pkg: User experiment configuration package.
    :param: hw: InstrumentSuite object.
    :param: procedures: Dictionary of instantiated procedures.
    """
    cntrl_cfg = exp_pkg.CONTROLLERS
    controllers = {}
    for cfg in cntrl_cfg:
        name = cfg["instance_name"]

        # instantiate the controller object. Search order for a controller class is:
        # 1) User defined controllers in the provided experiment package.
        # 2) spherexlabtools core controllers
        try:
            cntrl_class = getattr(exp_pkg.controllers, cfg["type"])
        except (AttributeError, ModuleNotFoundError):
            cntrl_mod = importlib.import_module(__name__)
            cntrl_class = getattr(cntrl_mod, cfg["type"])

        # get hardware #
        try:
            hw = getattr(hw, cfg["hw"])
        except (AttributeError, KeyError):
            hw = None

        # get procedure #
        try:
            proc = procedures[cfg["procedure"]]
        except KeyError:
            proc = None

        # instantiate controller and place it in the returned dictionary #
        controllers[name] = cntrl_class(name, cfg, hw=hw, proc=proc, log=log)

    return controllers
