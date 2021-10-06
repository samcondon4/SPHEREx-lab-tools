import pdb

import numpy as np
from time import sleep

from pymeasure.instruments.thorlabs.thorlabspm100usb import ThorlabsPM100USB
from pymeasure.experiment import FloatParameter
from pylabsm_baseproc import SmBaseProc

class PhotoDiodeMeasurement(SmBaseProc):

    sample_frequency = FloatParameter("Sample Frequency", units="Hz.", default=4,
                                      minimum=2 ** -4, maximum=2 ** 9)
    sample_time = FloatParameter("Sample time", units="s.", default=10)

    wavelength = FloatParameter("Wavelength", units="um.", default=1000)

    DATA_COLUMNS = ["Time Stamp", "Power"]

    visa_resource_name = "USB0::0x1313::0x8072::1912814 ::INSTR"

    def __init__(self, pm_instance=None, visa_resource_name=None):

        if visa_resource_name is not None:
            self.visa_resource_name = visa_resource_name

        if pm_instance is None:
            self.powermeter_instance = ThorlabsPM100USB(self.visa_resource_name)
        else:
            self.powermeter_instance = pm_instance

        self.powermeter_type = type(self.powermeter_instance)

        super().__init__()

    def startup(self):
        pass

    def execute(self):
        """ Description: main method to execute the measurement procedure.
        :return: Outputs a .csv file with photodiode power data and external metadata
        """
        if self.powermeter_instance is not None:
            pm = self.powermeter_instance
            self.running = True
            sample_period = 1 / self.sample_frequency
            samples = int(np.ceil(self.sample_frequency * self.sample_time))
            wavelength = self.wavelength

            # out_dict = {"Power": pm.power}
            out_dict = {}

            for i in range(samples):
                try:
                    data = {
                        'Time Stamp': self.timestamp,
                        'Power': pm.measure_power(wavelength)
                    }
                    self.emit("results", data)

                except Exception as e:
                    print(e)

                # add external metadata #######################################
                for key in self._metadata:
                    out_dict[key] = self._metadata[key]
                ###############################################################

                # write results #
                sleep(sample_period)

        self.running = False
