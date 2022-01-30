""" spherexlabtools.experiment

Sam Condon, 01/27/2022
"""

import logging
import queue
import threading
import importlib
import pyqtgraph as pg
from spherexlabtools.viewers import create_viewers
from spherexlabtools.recorders import create_recorders
from spherexlabtools.controllers import create_controllers
from spherexlabtools.instruments import create_instrument_suite

app = pg.mkQApp("Experiment")


class Experiment:
    """ The core class of the spherexlabtools package. The basic operating principle of spherexlabtools
        is implemented by this class. Namely, that every action that is performed in an experiment, be
        that the recording of data, or setting instrument parameters via a gui, is executed in its own thread.
        This class handles the scheduling of all threads and ensures that each thread has the resources that
        it needs to operate.
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
        self.controllers = create_controllers(exp_pkg.CONTROLLERS, self.hw)

    def start_controller(self, cntrl_key):
        """ Start a controller.
        """
        self.controllers[cntrl_key].start()

    def kill_controller(self, cntrl_key):
        """ Kill a controller.
        """
        self.controllers[cntrl_key].kill()


def create_experiment(exp_pkg):
    """ Instantiate and return an Experiment object.
    :param: exp_pkg: Python package containing the experiment configuration files.
    """
    return Experiment(exp_pkg)

