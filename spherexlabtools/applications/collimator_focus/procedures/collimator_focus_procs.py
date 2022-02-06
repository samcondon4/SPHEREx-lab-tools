""" collimator_focus:

    Module implementing the procedures used in the collimator focus measurement.

Sam Condon, 02/05/2022
"""

from spherexlabtools.procedures import LogProc
from pymeasure.experiment import FloatParameter


class CamViewProc(LogProc):
    """ Subclass of the logging procedure defining startup to initialize the camera in stream mode for
        a faster frame rate.
    """

    refresh_rate = FloatParameter("Frame Rate", units="Hz.", default=8, minimum=1, maximum=8)

    def __init__(self, hw, **kwargs):
        super().__init__(hw, **kwargs)

    def startup(self):
        """ Set the camera frame rate, and start streaming.
        """
        self.hw.cam_acquisition_frame_rate_auto = "Off"
        self.hw.cam_acquisition_frame_rate_en = True
        self.hw.cam_acquisition_frame_rate = self.refresh_rate
        self.hw.cam_start_stream()

    def shutdown(self):
        """ Stop camera streaming.
        """
        self.hw.cam_stop_stream()
