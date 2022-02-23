""" spherexlabtools.experiment

Sam Condon, 01/27/2022
"""
import logging
import pyqtgraph as pg
from PyQt5 import QtWidgets
from .loader import load_objects_from_cfg_list
import spherexlabtools.viewers as slt_view
import spherexlabtools.procedures as slt_proc
import spherexlabtools.instruments as slt_inst
import spherexlabtools.recorders as slt_record
import spherexlabtools.controllers as slt_control
from spherexlabtools.instruments import InstrumentSuite


app = None
logger = logging.getLogger(__name__)


class Experiment:
    """ The core class of the spherexlabtools package. The basic operating principle of spherexlabtools
        is implemented by this class. Namely, that every action that is performed in an experiment, be
        that the recording of data, or setting instrument parameters via a gui, is executed in its own thread.
        This class handles the scheduling of all threads and ensures that each thread has the resources that
        it needs to operate. All gui windows are run in the main thread.
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
        global app
        app = pg.mkQApp(exp_pkg.__name__)
        self.exp_pkg = exp_pkg
        logger.info("Initializing experiment: %s" % exp_pkg.__name__)

        self.layout = QtWidgets.QGridLayout()

        # initialize instrument-suite #############################################
        self.hw = InstrumentSuite(exp_pkg.INSTRUMENT_SUITE)

        # initialize viewers ######################################################
        viewer_cfgs = exp_pkg.VIEWERS
        try:
            search_order = [exp_pkg.viewers, slt_view]
        except AttributeError:
            search_order = [slt_view]
        self.viewers = load_objects_from_cfg_list(search_order, viewer_cfgs)

        # initialize recorders ####################################################
        rec_cfgs = exp_pkg.RECORDERS
        try:
            search_order = [exp_pkg.recorders, slt_record]
        except AttributeError:
            search_order = [slt_record]
        self.recorders = load_objects_from_cfg_list(search_order, rec_cfgs)

        # initialize procedures ###################################################
        proc_cfgs = exp_pkg.PROCEDURES
        try:
            search_order = [exp_pkg.procedures, slt_proc]
        except AttributeError:
            search_order = [slt_proc]
        self.procedures = load_objects_from_cfg_list(search_order, proc_cfgs, hw=self.hw,
                                                     viewers=self.viewers, recorders=self.recorders)

        # initialize controllers ##################################################
        control_cfgs = exp_pkg.CONTROLLERS
        try:
            search_order = [exp_pkg.controllers, slt_control]
        except AttributeError:
            search_order = [slt_control]
        self.controllers = load_objects_from_cfg_list(search_order, control_cfgs, hw=self.hw,
                                                      procs=self.procedures)

        logger.info("Experiment initialization complete.")

    def start_viewer(self, viewer_key):
        """ Start a viewer thread.
        """
        logger.info("Starting viewer: %s" % viewer_key)
        viewer = self.viewers[viewer_key]
        viewer.start()

    def stop_viewer(self, viewer_key):
        """ Stop a viewer thread.
        """
        logger.info("Killing viewer: %s" % viewer_key)
        self.viewers[viewer_key].stop()

    def start_recorder(self, rec_key):
        """ Start a recorder thread.
        """
        logger.info("Starting recorder: %s" % rec_key)
        self.recorders[rec_key].start()

    def stop_recorder(self, rec_key):
        """ Kill a recorder thread.
        """
        logger.info("Killing recorder: %s" % rec_key)
        self.recorders[rec_key].stop()

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
        logger.info("Starting controller: %s" % cntrl_key)
        self.controllers[cntrl_key].start()

    def stop_controller(self, cntrl_key):
        """ Kill a controller thread.
        """
        logger.info("Killing controller: %s" % cntrl_key)
        self.controllers[cntrl_key].stop()


def create_experiment(exp_pkg):
    """ Instantiate and return an Experiment object.
    :param: exp_pkg: Python package containing the experiment configuration files.
    """
    return Experiment(exp_pkg)

