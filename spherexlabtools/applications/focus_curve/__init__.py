from .main import FocusCurveSession as _FCurveSession
from .main import MscopeCfg, FocuserCfg, GaugeCfg, CamCfg, ProcCfg


_sesh = _FCurveSession()

# expose _FCurveSession attributes #
MScope = _sesh.mscope
RUN_PROC = _sesh.run_proc
STOP_PROC = _sesh.stop_proc
RUN_GUI = _sesh.run_gui
STOP_GUI = _sesh.stop_gui
START_LIVE = _sesh.start_mscope_live
STOP_LIVE = _sesh.stop_mscope_live
