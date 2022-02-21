""" collimator_focus:

    Module implementing the procedures used in the collimator focus measurement.

Sam Condon, 02/05/2022
"""
import logging
import numpy as np
from spherexlabtools.procedures import BaseProcedure, LogProc
from pymeasure.experiment import FloatParameter, IntegerParameter


logger = logging.getLogger(__name__)


class CamProc(BaseProcedure):
    """ Base class defining microscope camera startup and shutdown methods.
    """

    refresh_rate = FloatParameter("Frame Rate", units="Hz.", default=8, minimum=1, maximum=8)

    def __init__(self, cfg, **kwargs):
        super().__init__(cfg, **kwargs)

    def startup(self):
        BaseProcedure.startup(self)
        self.hw.cam_acquisition_frame_rate_auto = "Off"
        self.hw.cam_acquisition_frame_rate_en = True
        self.hw.cam_acquisition_frame_rate = self.refresh_rate
        self.hw.cam_start_stream()

    def shutdown(self):
        self.hw.cam_stop_stream()
        BaseProcedure.shutdown(self)


class CamViewProc(CamProc, LogProc):
    """ Subclass of the logging procedure defining the startup method to initialize the camera in stream mode for
        a faster frame rate.
    """

    average_num = IntegerParameter("Images Averaged", default=1)

    def __init__(self, cfg, **kwargs):
        LogProc.__init__(self, cfg, **kwargs)
        CamProc.__init__(self, cfg, **kwargs)


class CollimatorFocusProc(CamProc):
    """ Main collimator focus measurement procedure.
    """

    focus_position = IntegerParameter("Focus Position", units="step position", default=0)
    frames_per_image = IntegerParameter("Frames Per Image", default=10)
    images = IntegerParameter("Images", default=1)

    def __init__(self, cfg, **kwargs):
        """
        """
        super().__init__(cfg, **kwargs)

    def execute(self):
        # move the focuser and wait for its motion to complete #
        self.hw.focuser_step_position = self.focus_position
        self.hw.focuser_wait_for_completion()

        frame_width = self.hw.cam_exposure_width
        frame_height = self.hw.cam_exposure_height

        # take a set of images averaged over several frames #
        for i in range(int(self.images)):
            image = np.zeros([frame_height, frame_width], dtype=np.uint64)
            for e in range(int(self.frames_per_image)):
                exp = self.hw.cam_latest_frame
                image = image + (exp / self.frames_per_image)
                # write out to viewers #
                logger.debug("CollimatorFocusProc emitting data")
                self.emit("frame", exp)
                self.emit("frame_avg", image)

            # pass data_columns and group as argument to HDF5Recorder handle() method #
            self.emit("image", image, group="Data", group_records=self.images)

