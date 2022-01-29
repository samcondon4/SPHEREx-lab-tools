""" Configuration file for the microscope instrument.
"""

import time
import threading
import pyqtgraph as pg
from pymeasure.instruments.flir import Flea3 as _Fl3


class StreamView(pg.GraphicsLayoutWidget):

    def __init__(self):
        """ Initialize the stream view.
        """
        super().__init__()
        self.app = pg.mkQApp("Flea3 Live View")
        self.view = self.addViewBox()
        self.view.setAspectLocked(True)
        self.img = pg.ImageItem(border="w")
        self.view.addItem(self.img)
        self.update_active = False

    def update_from_object(self, obj, wait_event=None, set_event=None):
        """ Continuously update the displayed image from an object with a data attribute.

        :param: obj: Any object containing a "data" attribute containing image data to display.
        :param: wait_event: optional threading.Event object to pend on before reading image data.
        :param: set_event: optional threading.Event object to set after reading image data.
        """
        self.update_active = True
        while self.update_active:
            if wait_event is not None:
                wait_event.wait()
            data = obj.data
            self.img.setImage(data)
            if wait_event is not None:
                wait_event.clear()
            if set_event is not None:
                set_event.set()
        self.update_active = False


def _cam_start_stream(self):
    self.cam_stream_thread = threading.Thread(target=lambda: self.cam_stream_to_object(self.cam_data,
                                                                                       event=self._new_image_event))
    self.cam_stream_thread.start()


def _cam_stop_stream(self):
    self.cam_stream_active = False
    self.cam_stream_thread.join(1000)


def _cam_start_show_stream(self):
    self._cam_view = StreamView()
    self._cam_view.sleep = 1 / self.cam_acquisition_frame_rate
    self.cam_show_stream_thread = threading.Thread(target=lambda: self._cam_view.update_from_object(
        self.cam_data, wait_event=self._new_image_event, set_event=self._display_event))
    self.cam_show_stream_thread.start()
    self._cam_view.show()


def _cam_stop_show_stream(self):
    self._cam_view.update_active = False
    self.cam_show_stream_thread.join(1000)
    self._cam_view.close()


# params can be configured to set initial settings of the camera. Note that params that should not be altered are
# set in Microscope.__init__()
CamCfg = {
    "instance_name": "cam",
    "resource_name": _Fl3.cam_list[0],
    "manufacturer": "flir",
    "instrument": "Flea3",
    "params": {
        "gain_auto": "Off",
        "gain": 0,
        "blacklevel_en": False,
        "gamma_en": False,
        "sharpess_en": False,
        "acquisition_frame_rate_auto": "Off",
        "acquisition_frame_rate_en": True,
        "acquisition_frame_rate": 8,
        "exposure_width": 2448,
        "exposure_height": 2048,
    }
}

GaugeCfg = {
    "instance_name": "gauge",
    "resource_name": "ASRL/dev/ttyUSB0::INSTR",
    "manufacturer": "heidenhain",
    "instrument": "ND287",
    "params": {
        "units": "mm",
    },
    "kwargs": {
        "baud_rate": 115200
    }
}

FocuserCfg = {
    "instance_name": "focuser",
    "resource_name": "ASRL/dev/ttyUSB1::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "LinearStageController",
    "kwargs": {
        "log_id": "mscope_focus",
        "homedir": "CCW",
        "address": 3,
    }
}

MscopeCfg = {
    "subinstruments": [CamCfg, GaugeCfg, FocuserCfg],
    "property_config": [
        ("absolute_position", "gauge_position", "focuser_absolute_position")
    ],
    "attr_config": [
        ("_cam_view", None),
        ("_new_image_event", threading.Event()),
        ("CAM_START_STREAM", _cam_start_stream),
        ("CAM_STOP_STREAM", _cam_stop_stream),
        ("CAM_START_SHOW_STREAM", _cam_start_show_stream),
        ("CAM_STOP_SHOW_STREAM", _cam_stop_show_stream)
    ]
}
