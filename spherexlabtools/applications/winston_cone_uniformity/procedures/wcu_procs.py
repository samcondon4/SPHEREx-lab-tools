""" wcu_procs:

    Module implementing the procedures used in the winston cone uniformity measurement.

Sam Condon, 02/24/2022
"""
import time
import logging
import numpy as np
from spherexlabtools.thread import StoppableThread
from spherexlabtools.procedures import BaseProcedure, LogProc
from pymeasure.experiment import FloatParameter, IntegerParameter, BooleanParameter


logger = logging.getLogger(__name__)


class WcuProc(BaseProcedure):
    """ Winston cone uniformity full measurement procedure.
    """

    x_position = FloatParameter("X-Position", units="mm.", default=0)
    y_position = FloatParameter("Y-Position", units="mm.", default=0)
    power_samples = IntegerParameter("Samples", default=10)
    power_sample_rate = FloatParameter("Sample Rate", units="Hz.", default=1)
    home_init = BooleanParameter("Home", default=True)

    # flag to indicate if stage has been homed #
    homed = False

    def __init__(self, cfg, **kwargs):
        super().__init__(cfg, **kwargs)
        self.stage = self.hw.stage
        self.detector = self.hw.detector

    def home_stage(self):
        """ Method to start threads to home the x and y stages.
        """
        xthread = StoppableThread(target=self.stage.x_home)
        ythread = StoppableThread(target=self.stage.y_home)
        xthread.start()
        ythread.start()
        while xthread.is_alive() or ythread.is_alive():
            time.sleep(1)
            if self.should_stop():
                xthread.join()
                ythread.join()

    def startup(self):
        """ Home the stage if this has not been done yet.
        """
        if self.home_init:
            self.home_stage()

    def execute(self):
        pass
