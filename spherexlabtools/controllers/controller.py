""" spherexlabtools.controllers.controller

Sam Condon, 01/27/2022
"""
from PyQt5 import QtWidgets
import pyqtgraph as pg
import pyqtgraph.parametertree.parameterTypes as PTypes
from pyqtgraph.parametertree import Parameter, ParameterTree


class Controller:
    """ Base class for all controllers. This class implements data flow to/from external classes.
    """
    def __init__(self, set_event=None):
        """ Constructor for controller base class.

        :param: set_event: threading.Event object that is set when the set_params button is pressed.
        """
        self.set_data = {}
        self.set_event = set_event

    def clear_set_data(self):
        self.set_data = {}


class InstrumentController(QtWidgets.QWidget, Controller):
    """ Controller class to implement manual control over an individual instrument within a GUI.
    """

    def __init__(self, cfg, name, set_event=None):
        """ Initialize the InstrumentController Widget as a pyqtgraph parameter tree.

        :param: cfg: Controller configuration dictionary.
        :param: name: Name of the controller.
        """
        super().__init__(set_event)
        self.set_params = Parameter.create(name="Set Parameters", type="action")
        cfg["control_parameters"].append(self.set_params)
        self.control_group = Parameter.create(name="Control", type="group", children=cfg["control_parameters"])
        self.status_group = Parameter.create(name="Status", type="group", children=cfg["status_parameters"])
        self.parameters = Parameter.create(name=name, type="group", children=[self.control_group, self.status_group])
        self.tree = ParameterTree()
        self.tree.setParameters(self.parameters, showTop=True)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.tree)

        # Threading setup #
        self.set_params.sigStateChanged.connect(self.set_control_params)

    def set_control_params(self):
        """
        """
        self.set_data = {}
        for c in self.control_group.children():
            if c.name() != "Set Parameters":
                self.set_data[c.name()] = c.value()
        if self.set_event is not None:
            self.set_event.set()


def create_controllers(cntrl_cfg):
    """ Create a set of controller objects.
    """
    controllers = {}
    for cntrl in cntrl_cfg:
        typ_split = cntrl.pop("type").split("::")
        if typ_split[0] == "instrument":
            name = typ_split[1]
            controllers[name] = InstrumentController(cntrl, name)

    return controllers
