""" spherexlabtools.experiment

Sam Condon, 01/27/2022
"""

import queue
import logging
import pyqtgraph as pg

from spherexlabtools.workers import FlexibleWorker
from spherexlabtools.viewers import create_viewers
from spherexlabtools.recorders import create_recorders
from spherexlabtools.procedures import create_procedures
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
        log = {
            "level": exp_pkg.LOG_LEVEL,
            "handler": exp_pkg.FILE_HANDLER
        }
        self.exp_pkg = exp_pkg
        self.exp_pkg.LOGGER.info("Experiment initialization started.")
        self.viewers = create_viewers(exp_pkg)
        self.recorders = create_recorders(exp_pkg)
        self.hw = create_instrument_suite(exp_pkg)
        self.procedures = create_procedures(exp_pkg, self.hw, viewers=self.viewers, recorders=self.recorders)
        self.controllers = create_controllers(exp_pkg, hw=self.hw, procedures=self.procedures, log=log)
        self.exp_pkg.LOGGER.info("Experiment initialization complete.")

    def start_viewer(self, viewer_key):
        """ Start a viewer thread.
        """
        self.exp_pkg.LOGGER.info("Starting viewer: %s" % viewer_key)
        self.viewers[viewer_key].start()

    def stop_viewer(self, viewer_key):
        """ Stop a viewer thread.
        """
        self.exp_pkg.LOGGER.info("Killing viewer: %s" % viewer_key)
        self.viewers[viewer_key].stop()

    def start_recorder(self, rec_key):
        """ Start a recorder thread.
        """
        pass

    def stop_recorder(self, rec_key):
        """ Kill a recorder thread.
        """
        pass

    def start_procedure(self, proc_key, **kwargs):
        """ Start a procedure thread.
        """
        pass

    def stop_procedure(self, proc_key):
        """ Kill a procedure thread.
        """
        pass

    def start_controller(self, cntrl_key):
        """ Start a controller thread.
        """
        self.exp_pkg.LOGGER.info("Starting controller: %s" % cntrl_key)
        self.controllers[cntrl_key].start()

    def stop_controller(self, cntrl_key):
        """ Kill a controller thread.
        """
        self.exp_pkg.LOGGER.info("Killing controller: %s" % cntrl_key)
        self.controllers[cntrl_key].stop()


def create_experiment(exp_pkg):
    """ Instantiate and return an Experiment object.
    :param: exp_pkg: Python package containing the experiment configuration files.
    """
    return Experiment(exp_pkg)

