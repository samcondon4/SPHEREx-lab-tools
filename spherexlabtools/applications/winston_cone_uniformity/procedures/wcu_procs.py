""" wcu_procs:

    Module implementing the procedures used in the winston cone uniformity measurement.

Sam Condon, 02/24/2022
"""
import time
import logging
import numpy as np
from spherexlabtools.thread import StoppableThread
from spherexlabtools.procedures import BaseProcedure
from spherexlabtools.parameters import FloatParameter, IntegerParameter, BooleanParameter


logger = logging.getLogger(__name__)


class WcuProc(BaseProcedure):
    """ Winston cone uniformity full measurement procedure.
    """

    x_position = FloatParameter("X-Position", units="mm.", default=0)
    y_position = FloatParameter("Y-Position", units="mm.", default=0)
    power_samples = IntegerParameter("Samples", default=10)
    power_sample_rate = FloatParameter("Sample Rate", units="Hz.", default=1)
    home_init = BooleanParameter("Home", default=False)

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
        BaseProcedure.startup(self)
        if self.home_init:
            self.home_stage()

    def execute(self):
        self.stage.x_absolute_position = self.x_position
        self.stage.y_absolute_position = self.y_position
        self.stage.x_wait_for_completion()
        self.stage.y_wait_for_completion()
        samples = np.zeros(int(self.power_samples))
        for i in range(int(self.power_samples)):
            power = self.detector.power
            samples[i] = self.detector.power
            self.emit("power", power)
            time.sleep(1/self.power_sample_rate)
        mean = samples.mean()
        std = samples.std()
        median = np.median(samples)
        x_pos = self.stage.x_absolute_position
        y_pos = self.stage.y_absolute_position
        df = {"Mean Power (W.)": mean, "Power 1-Sigma (W.)": std, "X-Position (mm.)": x_pos,
              "Median Power (W.)": median, "Y-Position (mm.)": y_pos}
        self.emit("power_mean_std", df, group="Data")
        BaseProcedure.shutdown(self)
