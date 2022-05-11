""" collimator_focus:

    Module implementing the procedures used in the collimator focus measurement.

Sam Condon, 02/05/2022
"""
import logging
import numpy as np
from spherexlabtools.procedures import BaseProcedure, LogProc
from spherexlabtools.parameters import FloatParameter, IntegerParameter, Parameter

logger = logging.getLogger(__name__)


class CamProc(BaseProcedure):
    """ Base class defining microscope camera startup and shutdown methods.
    """
    
    refresh_rate = FloatParameter("Exposure Time us.", default=100000, minimum=30, maximum=5929218.769073486)

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)

    def startup(self):
        BaseProcedure.startup(self)
        try:
            self.hw.acquisition_frame_rate_en = False
            self.hw.exposure_time = self.refresh_rate
            self.hw.start_stream()
        except AttributeError:
            self.hw.Camera.acquisition_frame_rate_en = False
            self.hw.Camera.exposure_time = self.refresh_rate
            self.hw.Camera.start_stream()

    def shutdown(self):
        try:
            self.hw.stop_stream()
        except AttributeError:
            self.hw.Camera.stop_stream()
        BaseProcedure.shutdown(self)


class CamViewProc(CamProc, LogProc):
    """ Subclass of the logging procedure defining the startup method to initialize the camera in stream mode for
        a faster frame rate.
    """

    def __init__(self, cfg, exp, **kwargs):
        LogProc.__init__(self, cfg, exp, **kwargs)
        CamProc.__init__(self, cfg, exp, **kwargs)


class CollimatorFocusProc(CamProc):
    """ Main collimator focus measurement procedure.
    """

    focus_position = Parameter("Absolute Focus Position mm.", default=0)
    frames_per_image = IntegerParameter("Frames Per Image", default=10)
    images = IntegerParameter("Images", default=1)

    def __init__(self, cfg, exp, **kwargs):
        """
        """
        super().__init__(cfg, exp, **kwargs)
        self.cam = self.hw.Camera
        self.mscope = self.hw.MscopeMotors
        self.inst_params = {}

    def startup(self):
        """ Override startup to get instrument parameters
        """
        super().startup()
        self.inst_params.update({"focus_position": self.mscope.focuser_absolute_position,
                                 "camera_gain": self.cam.gain,
                                 "camera_exposure_time": self.cam.exposure_time})

    def execute(self):
        # move the focuser and wait for its motion to complete #
        self.mscope.focuser_absolute_position = self.focus_position
        self.mscope.focuser_wait_for_completion()

        frame_width = self.cam.exposure_width
        frame_height = self.cam.exposure_height

        # take a set of images averaged over several frames #
        for _ in range(int(self.images)):
            image = np.zeros([frame_height, frame_width], dtype=np.float64)
            for __ in range(self.frames_per_image):
                exp = self.cam.latest_frame
                image = image + (exp / self.frames_per_image)
                # write out to viewers #
                logger.debug("CollimatorFocusProc emitting data")
                self.emit("frame", exp)
                self.emit("frame_avg", image)

            self.emit("image", image, inst_params=self.inst_params)