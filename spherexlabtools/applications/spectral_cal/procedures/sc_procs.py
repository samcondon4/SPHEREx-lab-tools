""" sc_procs:

    This module implements the procedures used in the spectral cal measurement.

"""
import time
import numpy as np
import pandas as pd

from spherexlabtools.procedures import BaseProcedure
from pymeasure.experiment import IntegerParameter, FloatParameter, Parameter


class SpecCalProc(BaseProcedure):
    ndf_position = IntegerParameter("NDF Position", default=1, minimum=1, maximum=8)

    mono_shutter = IntegerParameter("Monochromator Shutter", default=1)
    mono_osf = Parameter("Monochromator OSF", default="Auto")
    mono_grating = Parameter("Monochromator Grating", default="Auto")
    mono_wavelength = FloatParameter("Monochomator Wavelength", default=0.5, units="um.")

    lockin_sr510_sensitivity = FloatParameter("Sr510 Sensitivity", default=0.5, units="V. rms")
    lockin_sr510_time_constant = FloatParameter("Sr510 Time-Constant", default=1, units="S.")
    lockin_sr830_sensitivity = FloatParameter("Sr830 Sensitivity", default=0.5, units="V. rms")
    lockin_sr830_time_constant = FloatParameter("Sr830 Time-Constant", default=1, units="S.")
    lockin_sample_rate = FloatParameter("Lockin Sample-Rate", default=1, units="Hz.")

    sample_time = FloatParameter("Sample Time", default=10, units="S.")

    inst_params = ["ndf_position", "mono_shutter", "mono_osf", "mono_grating", "mono_wavelength",
                   "lockin_sr510_time_constant", "lockin_sr830_time_constant", "lockin_sr510_sensitivity",
                   "lockin_sr830_sensitivity"]

    PARAM_DELIMITER = "_"

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)
        self.ndf = self.hw.ndf
        self.mono = self.hw.mono
        self.lockin = self.hw.lockin

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

    def execute(self):
        """ Execute the spectral-cal measurement.
        """
        samples = int(self.lockin_sample_rate * self.sample_time)
        record_data_df = pd.DataFrame({"sr830_x_voltage": np.zeros(samples), "sr830_y_voltage": np.zeros(samples),
                                       "sr510_voltage": np.zeros(samples)})
        for i in range(samples):
            sr830_voltages = self.lockin.sr830_xy
            sr510_voltage = self.lockin.sr510_output
            sample = {"sr830_x_voltage": sr830_voltages[0], "sr830_y_voltage": sr830_voltages[1],
                      "sr510_voltage": sr510_voltage}
            record_data_df.loc[i] = sample
            time.sleep(1 / self.lockin_sample_rate)
