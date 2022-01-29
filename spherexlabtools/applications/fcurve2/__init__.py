from .session import FocusCurveSession


_sesh = FocusCurveSession()

# expose session attributes #
START_IMG_WRITE = _sesh.start_image_write
STOP_IMG_WRITE = _sesh.stop_image_write
START_IMG_DISPLAY = _sesh.start_image_display
STOP_IMG_DISPLAY = _sesh.stop_image_display
START_PROC = _sesh.start_procedure
STOP_PROC = _sesh.stop_procedure

