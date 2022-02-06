""" collimator_focus:

    Module implementing the procedures used in the collimator focus measurement.

Sam Condon, 02/05/2022
"""

from spherexlabtools.procedures import BaseProcedure, LogProc
from pymeasure.experiment import FloatParameter, IntegerParameter


class CamProc(BaseProcedure):
    """ Base class defining microscope camera startup and shutdown methods.
    """

    refresh_rate = FloatParameter("Frame Rate", units="Hz.", default=8, minimum=1, maximum=8)

    def __init__(self, hw, **kwargs):
        super().__init__(hw, **kwargs)

    def startup(self):
        self.hw.cam_acquisition_frame_rate_auto = "Off"
        self.hw.cam_acquisition_frame_rate_en = True
        self.hw.cam_acquisition_frame_rate = self.refresh_rate
        self.hw.cam_start_stream()

    def shutdown(self):
        self.hw.cam_stop_stream()


class CamViewProc(CamProc, LogProc):
    """ Subclass of the logging procedure defining the startup method to initialize the camera in stream mode for
        a faster frame rate.
    """

    def __init__(self, hw, **kwargs):
        CamProc.__init__(self, hw, **kwargs)
        LogProc.__init__(self, hw, **kwargs)


class CollimatorFocusProc(CamProc):
    """ Main collimator focus measurement procedure.
    """

    focus_position = IntegerParameter("Focus Position", units="step position", default=0)
    frames_per_image = IntegerParameter("Frames Per Image", default=10)
    images = IntegerParameter("Images", default=1)

    def __init__(self, hw, **kwargs):
        """
        """
        super().__init__(hw, **kwargs)




