""" spherexlabtools.controllers.controller

Sam Condon, 01/27/2022
"""
import threading
from PyQt5 import QtWidgets
from pymeasure.experiment.parameters import *
from pyqtgraph.parametertree import Parameter, ParameterTree

from ..log import Logger


class Controller(QtWidgets.QWidget):
    """ Base-class for the controller objects.
    """

    def __init__(self, name, log=None):
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

    def __init__(self, name, hw, control_params=None, status_params=None, status_refresh=None, **kwargs):
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
        self.control_group = None
        if control_params is not None:
            self.set_params = Parameter.create(name="Set Parameters", type="action")
            control_params.append(self.set_params)
            self.control_group = Parameter.create(name="Control", type="group", children=control_params)
            params.append(self.control_group)
        # configure status parameters if they are present #
        self.status_group = None
        if status_params is not None:
            for p in status_params:
                p["enabled"] = False
            self.status_group = Parameter.create(name="Status", type="group", children=status_params)
            self.status_values = {c.name(): c.value() for c in self.status_group.children()}
            params.append(self.status_group)

        # parameter tree #
        self.set_parameters(params, showTop=True)

        # Threading setup #
        self.get_timer = None
        self.status_refresh = status_refresh
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

    def __init__(self, name, proc, log=None, **kwargs):
        super().__init__(name, log=log)
        self.procedure = proc
        self.proc_param_objs = proc.parameter_objects()
        self.proc_params_tree = [{} for _ in range(len(self.proc_param_objs.keys()))]
        j = 0
        # create parameter dictionaries for the procedure parameters #
        self.param_name_map = {}
        for key, val in self.proc_param_objs.items():
            self.param_name_map[val.name] = key
            self.proc_params_tree[j] = {"name": val.name, "type": self.parameter_map[type(val)], "value": val.value}
        self.proc_params = Parameter.create(name="Procedure Parameters", type="group", children=self.proc_params_tree)

        self.log_config = log

        # list of parameters implemented in subclasses #
        self.sub_params_tree = None

    def start_procedure(self):
        """ Start the procedure thread.
        """
        # set the procedure parameters #
        for c in self.proc_params.children():
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

    def __init__(self, name, proc, **kwargs):
        super().__init__(name, proc, **kwargs)

        # configure parameter tree #
        proc_dcols = self.procedure.DATA_COLUMNS
        log_params = [{} for _ in range(len(proc_dcols))]
        for i in range(len(log_params)):
            log_params[i] = {"name": proc_dcols[i], "type": "bool", "value": False}
        self.dcol_param_group = {"name": "Log Parameters:", "type": "group", "children": log_params}
        self.start_log = Parameter.create(name="Start Logging", type="action")
        self.stop_log = Parameter.create(name="Stop Logging", type="action")
        self.sub_params_tree = [self.dcol_param_group, self.start_log, self.stop_log]

        # build widget #
        params = []
        params.extend(self.sub_params_tree)
        params.append(self.proc_params)
        self.set_parameters(params, showTop=True)

        # connect buttons to methods #
        self.stop_log.sigStateChanged.connect(self.stop_procedure)
        self.start_log.sigStateChanged.connect(self.start_procedure)


def create_controllers(exp_pkg, hw=None, procedures=None, log=None):
    """ Create a set of controller objects from a list of configuration dictionaries, an InstrumentSuite object,
        a set of procedures, viewers, and recorders.

    :param: exp_pkg: User experiment configuration package.
    :param: hw: InstrumentSuite object.
    :param: procedures: Dictionary of instantiated procedures.
    """
    cntrl_cfg = exp_pkg.CONTROLLERS
    controllers = {}
    for cntrl in cntrl_cfg:
        name = cntrl["instance_name"]
        typ = cntrl["type"]
        if typ == "InstrumentController":
            hw = getattr(hw, cntrl["hw"])
            control_params = None if "control_parameters" not in cntrl.keys() else cntrl["control_parameters"]
            status_params = None if "status_parameters" not in cntrl.keys() else cntrl["status_parameters"]
            refresh = None if "status_refresh" not in cntrl.keys() else cntrl["status_refresh"]
            controllers[name] = InstrumentController(name, hw, control_params=control_params,
                                                     status_params=status_params, status_refresh=refresh, log=log)
        elif typ == "LogProcController":
            proc = procedures[cntrl["procedure"]]
            controllers[name] = LogProcController(name, proc, log=log)

    return controllers
