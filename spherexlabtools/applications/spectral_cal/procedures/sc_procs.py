""" sc_procs:

    This module implements the procedures used in the spectral cal measurement.

"""
import time
import numpy as np
import pandas as pd

from spherexlabtools.procedures import BaseProcedure
from spherexlabtools.parameters import IntegerParameter, FloatParameter, Parameter, BooleanParameter


class SpecCalProc(BaseProcedure):
    # neutral density filter #
    ndf_position = IntegerParameter("NDF Position", default=1, minimum=1, maximum=8)

    # monochromator #
    mono_shutter = IntegerParameter("Monochromator Shutter", default=1)
    mono_osf = Parameter("Monochromator OSF", default="Auto")
    mono_grating = Parameter("Monochromator Grating", default="Auto")
    mono_wavelength = FloatParameter("Monochomator Wavelength", default=0.5, units="um.")

    # lockins for reference detectors #
    lockin_sr510_sensitivity = FloatParameter("Sr510 Sensitivity", default=0.5, units="V. rms")
    lockin_sr510_time_constant = FloatParameter("Sr510 Time-Constant", default=1, units="S.")
    lockin_sr830_sensitivity = FloatParameter("Sr830 Sensitivity", default=0.5, units="V. rms")
    lockin_sr830_time_constant = FloatParameter("Sr830 Time-Constant", default=1, units="S.")
    lockin_sample_rate = FloatParameter("Lockin Sample-Rate", default=1, units="Hz.")

    # exposure time and comment for detector readout #
    exposure_time = FloatParameter("Exposure Time", default=10, units="S.")
    exposure_comment = Parameter("Exposure Comment", default="")

    # parameters for the readout #
    generate_fits = IntegerParameter("Generate Fits", default=1)

    inst_params = ["ndf_position", "mono_shutter", "mono_osf", "mono_grating", "mono_wavelength",
                   "lockin_sr510_time_constant", "lockin_sr830_time_constant", "lockin_sr510_sensitivity",
                   "lockin_sr830_sensitivity"]

    PARAM_DELIMITER = "_"

    SR830_X_STR = "sr830_x_voltage"
    SR830_Y_STR = "sr830_y_voltage"
    SR510_STR = "sr510_output_voltage"

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)
        self.ndf = self.hw.ndf
        self.mono = self.hw.mono
        self.lockin = self.hw.lockin
        self.readout = self.hw.readout
        self.inst_params_emit = {}

    def startup(self):
        """ Initialize the spectral-cal measurement by moving all hardware into the proper state.
        """
        BaseProcedure.startup(self)
        # set the instrument parameters #
        for param in self.inst_params:
            param_split = param.split(SpecCalProc.PARAM_DELIMITER)
            inst = getattr(self, param_split[0])
            val = getattr(self, param)
            setattr(inst, SpecCalProc.PARAM_DELIMITER.join(param_split[1:]), val)

        # read the resulting instrument parameters #
        self.inst_params_emit = {}
        for param in self.inst_params:
            param_split = param.split(SpecCalProc.PARAM_DELIMITER)
            inst = getattr(self, param_split[0])
            val = getattr(inst, SpecCalProc.PARAM_DELIMITER.join(param_split[1:]))
            self.inst_params_emit[param] = [val]

        # TODO: This is a point that could potentially add a lot of time over long scans. Maybe this can be modified?
        time.sleep(6*self.lockin_sr830_time_constant)

    def execute(self):
        """ Execute the spectral-cal measurement.
        """
        readout_response = self.readout.start_exposure(self.exposure_time, self.exposure_comment,
                                                       nofits=int(not self.generate_fits))
        readout_keep_dict = readout_response["testcom"]
        readout_keep_dict.update({"dio": readout_response["dio"], "fits": readout_response["fits"]})
        self.inst_params_emit.update(readout_keep_dict)
        data = self.inst_params_emit["filename"]
        data_df = pd.DataFrame({"exposure_filename": [data]})
        self.emit("spec_cal_csv", data_df, inst_params=self.inst_params_emit)
        """ 
        #samples = int(self.lockin_sample_rate * self.sample_time)
        for i in range(samples):
            sr830_voltages = self.lockin.sr830_xy
            sr510_voltage = self.lockin.sr510_output
            sample = {self.SR830_X_STR: [sr830_voltages[0]], self.SR830_Y_STR: [sr830_voltages[1]],
                      self.SR510_STR: [sr510_voltage]}
            sample.update(self.inst_params_emit)
            # emit viewer records for live plots ########
            self.emit("sr830_x", sr830_voltages[0])
            self.emit("sr830_y", sr830_voltages[1])
            self.emit("sr510_output", sr510_voltage)
            time.sleep(1 / self.lockin_sample_rate)
            self.emit("lockin_output", sample)
        """
