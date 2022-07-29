import time
import numpy as np
from spherexlabtools.parameters import *
from spherexlabtools.procedures import BaseProcedure


class TestProc(BaseProcedure):

    frame_width = IntegerParameter("Frame Width", units="pixels", default=2448)
    frame_height = IntegerParameter("Frame Height", units="pixels", default=2048)
    heater_output = FloatParameter("Heater Output Voltage", units="V.", default=0)
    light_frame = IntegerParameter("Light Frame", default=0)
    wait_time = FloatParameter("Wait Time", units="s.", default=0)

    images = IntegerParameter("Images", default=1)

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)
        self.lockin = self.hw.LockinAmp
        self.heater = self.hw.Heater
        self.cam = self.hw.Camera

    def startup(self):
        super().startup()
        self.cam.frame_width = self.frame_width
        self.cam.frame_height = self.frame_height
        self.heater.output_voltage = self.heater_output
        time.sleep(self.wait_time)

    def execute(self):
        for i in range(self.images):
            # - get an image and write out to the HDF5 recorder - #
            im = self.cam.frame
            if self.light_frame == 0:
                im = np.zeros_like(im)
            inst_params_dict = {"frame_width": self.frame_width,
                                "frame_height": self.frame_height,
                                "heater_output": self.heater_output,
                                "light_frame": self.light_frame}
            self.emit("image", im, inst_params=inst_params_dict)

            # - get a sample lockin output - #
            lockin_out = self.lockin.sr830_wave
            self.emit("lockin_output", np.array([lockin_out]), inst_params=inst_params_dict)
