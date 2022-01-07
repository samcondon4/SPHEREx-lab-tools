import numpy as np
from time import sleep
from pymeasure.experiment import FloatParameter
from pymeasure.instruments.srs.sr510 import SR510
from pymeasure.instruments.srs.sr830 import SR830
from .baseproc import SmBaseProc


class LockinMeasurement(SmBaseProc):
    sample_frequency = FloatParameter("Sample Frequency", units="Hz.", default=1,
                                      minimum=2 ** -4, maximum=2 ** 9)
    sample_time = FloatParameter("Sample time", units="s.", default=10)
    DATA_COLUMNS = []

    def __init__(self, lockin_instance):
        self.lockin_instance = lockin_instance
        self.lockin_type = type(lockin_instance)
        self.DATA_COLUMNS = ["Time Stamp", "phase", "frequency", "sensitivity", "time constant"]
        if self.lockin_type is SR510:
            self.DATA_COLUMNS.extend(["Status Byte", "Output Voltage (V.)"])
        else:
            self.DATA_COLUMNS.extend(
                ["LIA Status Byte", "ERR Status Byte", "X-Channel Voltage (V.)", "Y-Channel Voltage (V.)"])
        super().__init__()

    def startup(self):
        """ Method that executes just before execute() to initialize the measurement procedure. In this case, if the
            hold attribute is true, then wait for 6 time constants. Further, if the lockin_instance is an SR830, then
            call the auto_phase() function.
        """
        if self.hold:
            sleep(6*self.lockin_instance.time_constant)

    def execute(self):
        """ Description: main method to execute the measurement procedure.
        :return: Outputs a .csv file with lockin data and external metadata
        """
        if self.lockin_instance is not None:
            li = self.lockin_instance
            self.running = True
            sample_period = 1 / self.sample_frequency
            samples = int(np.ceil(self.sample_frequency * self.sample_time))
            out_dict = {"phase": li.phase, "frequency": li.frequency,
                        "sensitivity": li.sensitivity, "time constant": li.time_constant}

            for i in range(samples):
                # break out of the measurement loop if should_stop is set, i.e. the measurement was paused or aborted.
                if self.should_stop():
                    break

                try:
                    out_dict["Time Stamp"] = self.timestamp
                except Exception as e:
                    print(e)
                # record lockin data and status ###############################
                if self.lockin_type is SR510:
                    out_dict["Status Byte"] = li.status
                    out_dict["Output Voltage (V.)"] = li.output
                elif self.lockin_type is SR830:
                    out_dict["LIA Status Byte"] = li.lia_status
                    out_dict["ERR Status Byte"] = li.err_status
                    voltage = li.xy
                    out_dict["X-Channel Voltage (V.)"] = voltage[0]
                    out_dict["Y-Channel Voltage (V.)"] = voltage[1]
                ###############################################################

                # add external metadata #######################################
                for key in self._metadata:
                    out_dict[key] = self._metadata[key]
                ###############################################################

                # write results #
                self.emit("results", out_dict)
                sleep(sample_period)

        self.running = False
