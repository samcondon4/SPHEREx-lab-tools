""" spherexlabtools.controllers.controller

Sam Condon, 01/27/2022
"""
import queue
import threading
from PyQt5 import QtWidgets
import pyqtgraph as pg
import pyqtgraph.parametertree.parameterTypes as PTypes
from pyqtgraph.parametertree import Parameter, ParameterTree


class InstrumentController(QtWidgets.QWidget):
    """ Controller class to implement manual control over an individual instrument within a GUI.
    """

    def __init__(self, hw, cfg, name):
        """ Initialize the InstrumentController Widget as a pyqtgraph parameter tree.

        :param: hw: Instrument driver.
        :param: cfg: Controller configuration dictionary.
        :param: name: Name of the controller.
        """
        super().__init__()
        self.hw = hw
        self.set_params = Parameter.create(name="Set Parameters", type="action")
        cfg["control_parameters"].append(self.set_params)
        self.control_group = Parameter.create(name="Control", type="group", children=cfg["control_parameters"])
        # disable status parameters so that the user cannot edit them.
        for p in cfg["status_parameters"]:
            p["enabled"] = False
        self.status_group = Parameter.create(name="Status", type="group", children=cfg["status_parameters"])
        self.parameters = Parameter.create(name=name, type="group", children=[self.control_group, self.status_group])
        self.tree = ParameterTree()
        self.tree.setParameters(self.parameters, showTop=True)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.tree)

        self.alive = False
        self.get_timer = None

        # Threading setup #
        self.status_refresh = cfg["status_refresh"]
        self.set_params.sigStateChanged.connect(self.set_inst_params)

    def set_inst_params(self):
        """ Write instrument control parameters to the hardware.
        """
        if self.alive:
            for c in self.control_group.children():
                if c.name() != "Set Parameters":
                    setattr(self.hw, c.name(), c.value())

    def get_inst_params(self):
        """ Get instrument parameters and write them to GUI elements.
        """
        if self.alive:
            for c in self.status_group.children():
                attr = getattr(self.hw, c.name())
                c.setValue(attr)
            self.get_timer = threading.Timer(self.status_refresh, self.get_inst_params)
            self.get_timer.start()

    def start(self):
        """ Start the controller.
        """
        self.alive = True
        self.show()
        self.get_inst_params()

    def kill(self):
        """ Kill the controller.
        """
        self.alive = False
        self.get_timer.cancel()
        self.close()


def create_controllers(cntrl_cfg, hw):
    """ Create a set of controller objects from a list of configuration dictionaries, an InstrumentSuite object,
        and a set of procedures.

    :param: cntrl_cfg: List of controller configuration dictionaries.
    :param: hw: InstrumentSuite object.
    """
    controllers = {}
    for cntrl in cntrl_cfg:
        typ_split = cntrl.pop("type").split("::")
        if typ_split[0] == "instrument":
            name = typ_split[1]
            controllers[name] = InstrumentController(getattr(hw, name), cntrl, name)

    return controllers
