import os
import logging
import threading

import numpy as np
from .fcurve import FocusCurveProc
from .microscope import Microscope
from pymeasure.experiment import Worker, ImgResults

from .config.proc_cfg import ProcCfg
from .config.mscope_cfg import MscopeCfg, FocuserCfg, GaugeCfg, CamCfg


log = logging.getLogger()
log.addHandler(logging.NullHandler())


class FocusCurveSession:
    """ This class provides the top level focus curve generation interface.
    """

    def __init__(self):
        """ Create a new collimator control and focus curve generation session.
        """
        log.warning("Initializing focus curve generation session.")
        # event used to synchronize procedure and live display threads #
        self.img_display_event = threading.Event()
        self.mscope = Microscope(MscopeCfg, img_display_event=self.img_display_event)
        self.live_active = False
        ProcCfg["frame_rate"] = self.mscope.stream_frame_rate

    def cfg_mscope(self):
        """ Shutdown the microscope and reinitialize with (presumably) new configuration settings.
        """
        raise NotImplementedError("Reconfiguration of microscope not yet implemented!")

    def start_mscope_live(self):
        """ Start microscope live streaming.
        """
        log.warning("Starting microscope camera live stream.")
        self.mscope.CAM_START_STREAM()
        self.mscope.CAM_START_SHOW_STREAM()
        self.live_active = True

    def stop_mscope_live(self):
        """ Stop microscope live streaming.
        """
        log.warning("ending microscope camera live stream.")
        self.mscope.CAM_STOP_STREAM()
        self.mscope.CAM_STOP_SHOW_STREAM()
        self.live_active = False

    def set_frame_rate(self, rate):
        """ Change the camera streaming frame rate. Update the display refresh and procedure sleep times accordingly.

        :param: rate: Float frame rate value.
        """
        self.mscope.stream_frame_rate = rate
        ProcCfg["frame_rate"] = rate

    def run_proc(self, foc_pos=None):
        """ Run the focus curve measurement automation procedure.

        :param: foc_pos: Optional focuser step position to run procedure at. This will override the current value set
                         in the procedure configuration dictionary. Can be a list or a single integer value. If not set,
                         then the value from ProcCfg is used.
        """
        # if camera streaming has not been activated, activate it #
        if not self.live_active:
            self.start_mscope_live()

        # generate list of focus positions to iterate through #
        if foc_pos is None:
            foc_pos = ProcCfg["focus_position"]
            foc_pos_from_cfg = None
        else:
            foc_pos_from_cfg = ProcCfg.pop("focus_position")
        foc_pos_typ = type(foc_pos)
        if foc_pos_typ is list or foc_pos_typ is np.ndarray:
            foc_pos_list = foc_pos
        else:
            foc_pos_list = [foc_pos]

        # create the procedure instance #
        proc = FocusCurveProc(mscope=self.mscope, exp_source=self.mscope.cam_data, cfg=ProcCfg,
                              wait_event=self.img_display_event)

        # run a focus curve procedure at each focus position #
        for pos in foc_pos_list:
            proc.focus_position = pos
            proc.running = True
            results = ImgResults(proc, os.path.join(ProcCfg["output_directory"], ProcCfg["filename"]))
            worker = Worker(results)
            worker.start()
            # TODO: FIGURE OUT WHY THIS IS BLOCKING THE OTHER THREADS #
            worker.join(1000)

        # repopulate the config dict with initial position value #
        if foc_pos_from_cfg is not None:
            ProcCfg["focus_position"] = foc_pos_from_cfg

    def stop_proc(self):
        pass

    def run_gui(self):
        pass

    def stop_gui(self):
        pass
