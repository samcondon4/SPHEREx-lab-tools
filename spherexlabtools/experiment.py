""" spherexlabtools.experiment

Sam Condon, 01/27/2022
"""
import logging
import pyqtgraph as pg
from PyQt5 import QtWidgets
from .loader import load_objects_from_cfg_list
import spherexlabtools.viewers as slt_view
import spherexlabtools.procedures as slt_proc
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

                - imports the measure.py module and creates a set of recorders using the
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
        self.active_threads = {}

        # initialize instrument-suite #############################################
        self.hw = InstrumentSuite(exp_pkg.INSTRUMENT_SUITE)

        # initialize viewers ######################################################
        viewer_cfgs = exp_pkg.VIEWERS
        try:
            search_order = [exp_pkg.viewers, slt_view]
        except AttributeError:
            search_order = [slt_view]
        self.viewers = load_objects_from_cfg_list(search_order, self, viewer_cfgs)

        # initialize recorders ####################################################
        rec_cfgs = exp_pkg.RECORDERS
        try:
            search_order = [exp_pkg.recorders, slt_record]
        except AttributeError:
            search_order = [slt_record]
        self.recorders = load_objects_from_cfg_list(search_order, self, rec_cfgs)

        # initialize procedures ###################################################
        proc_cfgs = exp_pkg.PROCEDURES
        # get all compound procedure configurations #
        compound_proc_cfgs = []
        for proc in proc_cfgs:
            if "subprocedures" in proc.keys():
                compound_proc_cfgs.append(proc)
                proc_cfgs.remove(proc)
        try:
            search_order = [exp_pkg.procedures, slt_proc]
        except AttributeError:
            search_order = [slt_proc]
        self.procedures = load_objects_from_cfg_list(search_order, self, proc_cfgs, hw=self.hw,
                                                     viewers=self.viewers, recorders=self.recorders)
        # instantiate compound procedures #
        self.procedures.update(load_objects_from_cfg_list([slt_proc], self, compound_proc_cfgs))

        # initialize controllers ##################################################
        control_cfgs = exp_pkg.CONTROLLERS
        try:
            search_order = [exp_pkg.controllers, slt_control]
        except AttributeError:
            search_order = [slt_control]
        self.controllers = load_objects_from_cfg_list(search_order, self, control_cfgs, hw=self.hw,
                                                      procs=self.procedures)

        logger.info("Experiment initialization complete.")

    def start_viewer(self, viewer_key):
        """ Start a viewer thread.
        """
        logger.info("Starting viewer: %s" % viewer_key)
        viewer = self.viewers[viewer_key]
        self.start_thread(viewer_key, viewer)

    def stop_viewer(self, viewer_key):
        """ Stop a viewer thread.
        """
        logger.info("Killing viewer: %s" % viewer_key)
        self.stop_thread(viewer_key)

    def start_recorder(self, rec_key):
        """ Start a recorder thread.
        """
        logger.info("Starting recorder: %s" % rec_key)
        recorder = self.recorders[rec_key]
        self.start_thread(rec_key, recorder)

    def stop_recorder(self, rec_key):
        """ Kill a recorder thread.
        """
        logger.info("Killing recorder: %s" % rec_key)
        self.stop_thread(rec_key)

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
        controller = self.controllers[cntrl_key]
        # controller guis run in the main thread. #
        controller.start()

    def stop_controller(self, cntrl_key):
        """ Kill a controller thread.
        """
        logger.info("Killing controller: %s" % cntrl_key)
        controller = self.controllers[cntrl_key]
        controller.stop()

    def start_thread(self, thread_key, thread):
        """ Start a thread and update the active_threads dictionary. This should only be called internally.

        :param thread_key: String key name to use in the active_threads dictionary.
        :param thread: Thread object to start.
        """
        if thread_key not in self.active_threads.keys() or not self.active_threads[thread_key].running:
            thread.start()
            self.active_threads[thread_key] = thread
        else:
            raise RuntimeError("Thread %s is already active!" % thread_key)

    def get_start_thread_lambda(self, thread_key, thread):
        """ Return a lambda function to call the start_thread method. This is useful to generate lambda functions
            to connect to pyqt signals.

        :param thread_key: Same as for :meth:`Experiment.start_thread`
        :param thread: Same as for :meth:`Experiment.start_thread`
        """
        return lambda key=thread_key, t=thread: self.start_thread(key, t)

    def stop_thread(self, thread_key):
        """ Stop a thread and update the active_threads dictionary. This should only be called internally.

        :param thread_key: String key name for the active_threads dictionary.
        """
        if thread_key in self.active_threads.keys():
            thread = self.active_threads.pop(thread_key)
            thread.stop()

    def get_stop_thread_lambda(self, thread_key, thread):
        """ Return a lambda function to call the :meth:`Experiment.start_thread` method. This is useful to generate
            lambda functions to connect to pyqt signals.

        :param thread_key: Same as for :meth:`Experiment.start_thread`
        :param thread: Same as for :meth:`Experiment.start_thread`
        """
        return lambda key=thread_key, t=thread: self.start_thread(key, t)


def create_experiment(exp_pkg):
    """ Instantiate and return an Experiment object.
    :param: exp_pkg: Python package containing the experiment configuration files.
    """
    return Experiment(exp_pkg)

