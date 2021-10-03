import os
import asyncio
import datetime
import numpy as np
from time import sleep
from pymeasure.instruments.srs.sr510 import SR510
from pymeasure.instruments.srs.sr830 import SR830
from pymeasure.experiment import Procedure, Worker, Results, FloatParameter


class LockinMeasurement(Procedure):
    sample_frequency = FloatParameter("Sample Frequency", units="Hz.", default=4,
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
        self._timestamp_method = lambda: str(datetime.datetime.now())
        self._metadata = {}
        self.running = False
        self.worker = None
        self.tc_hold = True
        super().__init__()

    def startup(self):
        pass

    def execute(self):
        """ Description: main method to execute the measurement procedure.
        :return: Outputs a .sv file with lockin data and external metadata
        """
        if self.lockin_instance is not None:
            li = self.lockin_instance
            self.running = True
            sample_period = 1 / self.sample_frequency
            samples = int(np.ceil(self.sample_frequency * self.sample_time))
            out_dict = {"phase": li.phase, "frequency": li.frequency,
                        "sensitivity": li.sensitivity, "time constant": li.time_constant}

            # sleep for 6 time constants to allow lockin to settle before starting measurement #
            if self.tc_hold:
                sleep(6*out_dict["time constant"])

            for i in range(samples):
                # break out of the measurement loop if should_stop is set
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

    @property
    def metadata(self):
        """Property to hold external metadata to include in the output csv
        """
        return self._metadata

    @metadata.setter
    def metadata(self, meta_dict):
        """Description: add external metadata to include to the output .csv file

        :param meta_dict: (dict) Dictionary with keys corresponding to .csv column header and values corresponding to
                          the value to place under the header.
        :return: None
        """
        if meta_dict == {}:
            self._metadata = {}
        else:
            keys_list = list(meta_dict.keys())
            for key in meta_dict:
                if key not in self._metadata:
                    self.DATA_COLUMNS.append(key)
                self._metadata[key] = meta_dict[key]

    @property
    def timestamp(self):
        """Property to return a time stamp from the user set timestamp method
        """
        return self._timestamp_method()

    @timestamp.setter
    def timestamp(self, method):
        """Set the time stamp method.
        """
        self._timestamp_method = method

    async def run(self, measure_parameters, append_to_existing=False, hold=False):
        """Description: Run a measurement on the sr510/830 lockin.

        :param measure_parameters: (dict) dictionary containing parameters of the measurement. Should be of the form:
                                          {"sample_rate": <(float) sampling frequency in Hz.>,
                                           "sample_time": <(float) sample time in s.>,
                                          "storage_path": <(str) .csv file path>}
        :param append_to_existing: (bool) boolean to indicate if data should be saved to an existing file or to create
                                   a new file.
        :param hold: (bool) boolean to indicate if the coroutine should wait to return until the measurement is complete.
                            Procedure will also sleep for 6 time constants if this kwarg is set to allow the lockin to
                            settle.
        :return: None, but outputs a .csv file
        """
        self.sample_frequency = measure_parameters["sample_rate"]
        self.sample_time = measure_parameters["sample_time"]
        self.tc_hold = hold
        file_name = measure_parameters["storage_path"]
        if not append_to_existing:
            while os.path.exists(file_name):
                file_name_split = file_name.split(".")
                file_name = file_name_split[0] + "_." + file_name_split[1]

        # set phase of sr830 using the auto-phase function
        if self.lockin_type is SR830:
            self.lockin_instance.auto_phase()

        results = Results(self, file_name)
        self.worker = Worker(results)
        self.worker.start()
        self.running = True
        if hold:
            while self.running:
                await asyncio.sleep(0)
