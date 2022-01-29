""" This module provides a class, :class:`.Microscope` through which the collimator calibration microscope can
    be controlled.

Sam Condon, 01/09/2022
"""
import time
import logging
import threading
import pyqtgraph as pg
from pymeasure.instruments import CompoundInstrument


pg.setConfigOption("imageAxisOrder", "row-major")


class LockedData:

    initialized = False

    def __init__(self, data=None):
        self.lock = threading.Lock()
        self.data = data
        self.initialized = True

    def __getattribute__(self, item):
        """ Override to use the thread lock.
        """
        inititalized = object.__getattribute__(self, "initialized")
        if inititalized:
            lock = object.__getattribute__(self, "lock")
            lock.acquire()
            val = object.__getattribute__(self, item)
            lock.release()
            return val
        else:
            return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        """ Override to use the thread lock.
        """
        inititalized = object.__getattribute__(self, "initialized")
        if inititalized:
            lock = object.__getattribute__(self, "lock")
            lock.acquire()
            object.__setattr__(self, key, value)
            lock.release()
        else:
            object.__setattr__(self, key, value)


class Microscope(CompoundInstrument):

    # camera data, display, and stream threads #
    cam_data = LockedData()
    cam_stream_thread = None
    cam_show_stream_thread = None
    _display_event = None

    def __init__(self, cfg, img_display_event=None):
        """ Initialize a Microscope instance.

        :param: cfg: :class:`.CompoundInstrument` configuration dictionary.
        :param: img_display_event: optional threading.Event object to set after displaying an image.
        """
        self._display_event = img_display_event
        super().__init__(cfg)
        self.cam_acquisition_mode = "Continuous"

    @property
    def stream_frame_rate(self):
        """ Integer property representing the camera stream frame rate.
        """
        return self.cam_acquisition_frame_rate

    @stream_frame_rate.setter
    def stream_frame_rate(self, rate):
        self.cam_acquisition_frame_rate = rate
        self._cam_view.sleep = 1/rate

