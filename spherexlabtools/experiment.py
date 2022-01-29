""" spherexlabtools.experiment

Sam Condon, 01/27/2022
"""

import logging
import threading
import importlib
import pyqtgraph as pg
from spherexlabtools.viewers import create_viewers
from spherexlabtools.recorders import create_recorders
from spherexlabtools.controllers import create_controllers
from spherexlabtools.instruments import create_instrument_suite

app = pg.mkQApp("Experiment")


class InstrumentControlThread(threading.Thread):

    def __init__(self, hw, controller, wait_timeout, **kwargs):
        """ Constructor for a new instrument control thread.

        :param: hw: Instrument object.
        :param: controller: InstrumentController object.
        :param: wait_timeout: Timeout between set_event pends.
        """
        super().__init__(**kwargs)
        self.hw = hw
        self.controller = controller
        self.wait_timeout = wait_timeout
        self.should_stop = False
        self.set_event = threading.Event()

        # configure thread synchronization #
        self.controller.set_event = self.set_event

    def run(self):
        """
        """
        while not self.should_stop:
            self.set_event.wait(self.wait_timeout)
            if self.controller.set_data != {}:
                for p in self.controller.set_data:
                    setattr(self.hw, p, self.controller.set_data[p])
            self.controller.clear_set_data()


class Experiment:
    """ This class defines the top-level experiment control object.
    """

    thread = None

    def __init__(self, exp_pkg):
        """ Initialize an experiment. This init function performs the following tasks:
                - imports the hw.py module and instantiates an :class:`.InstrumentSuite`
                  instance using the INSTRUMENT_SUITE name found within.

                - imports the record.py module and creates a set of recorders using the
                  RECORDERS name found within.

                - imports the view.py module and creates a set of viewers using the VIEWERS
                  name found within.

        :param: exp_pkg: Python package containing the experiment configuration modules.
        """
        # self.recorders = create_recorders(recorders)
        # self.viewers = create_viewers(viewers)
        self.hw = create_instrument_suite(exp_pkg.INSTRUMENT_SUITE)
        self.controllers = create_controllers(exp_pkg.CONTROLLERS)
        for c in self.controllers.keys():
            self.start_controller(c)

    def start_controller(self, cntrl_key):
        """ Start a controller thread and interface.
        """
        hw = getattr(self.hw, cntrl_key)
        controller = self.controllers[cntrl_key]
        controller.show()
        if "InstrumentController" in str(type(controller)):
            self.thread = InstrumentControlThread(hw, controller, 0.5)
            self.thread.setDaemon(True)
            self.thread.start()


def create_experiment(exp_pkg):
    """ Instantiate and return an Experiment object.
    :param: exp_pkg: Python package containing the experiment configuration files.
    """
    return Experiment(exp_pkg)

