import asyncio
import os
from time import sleep
import datetime
import numpy as np
from pymeasure.experiment import Procedure, Worker, Results
from pymeasure.experiment import FloatParameter


class Sr510Measurement(Procedure):

    sr510_instance = None
    running = False
    sample_frequency = FloatParameter("Sample Frequency", units="Hz.", default=4,
                                      minimum=2**-4, maximum=2**9)
    sample_time = FloatParameter("Sample Time", units="s.", default=10)
    metadata = {}

    DATA_COLUMNS = ["Time Stamp", "Output Voltage (V.)", "Status Register"]

    def execute(self):
        """ Description: main method for the procedure.
        :return: Outputs a .csv file with Sr830 data
        """
        print("good")
        if self.sr510_instance is not None:
            print("good")
            self.running = True
            sample_period = 1/self.sample_frequency
            samples = int(np.ceil(self.sample_frequency * self.sample_time))
            for i in range(samples):
                print("good")
                time_stamp = datetime.datetime.now()
                voltage = self.sr510_instance.output
                status = self.sr510_instance.status
                out_dict = {"Time Stamp": time_stamp}
                for key in self.metadata:
                    out_dict[key] = self.metadata[key]
                out_dict["Output Voltage (V.)"] = voltage
                out_dict["Status Register"] = status
                self.emit('results', out_dict)
                sleep(sample_period)
            self.running = False
        else:
            self.running = False
            raise RuntimeError("No valid SR830 class instance has been passed to the procedure.")

    def set_metadata(self, meta_dict):
        """Description: add metadata to include to the output .csv file

        :param meta_dict: (dict) Dictionary with keys corresponding to .csv column header and values corresponding to
                          the value to place under the header.
        :return: None
        """
        keys_list = list(meta_dict.keys())
        self.DATA_COLUMNS.extend(keys_list)
        for key in meta_dict:
            if key not in self.metadata:
                self.metadata[key] = meta_dict[key]

    def clear_metadata(self):
        """Description: clear the metadata dictionary

        :return:
        """
        self.metadata = {}

    async def run(self, measure_parameters, metadata=None, append_to_existing=False, hold=False):
        """Description: Run a measurement on the sr830 lockin.

        :param measure_parameters: (dict) dictionary containing parameters of the measurement. Should be of the form:
                                          {"sample_rate": <(float) sampling frequency in Hz.>,
                                           "sample_time": <(float) sample time in s.>,
                                          "storage_path": <(str) .csv file path>}
        :param metadata: (dict) dictionary containing additional metadata to include
        :param append_to_existing: (bool) boolean to indicate if data should be saved to an existing file or to create
                                   a new file.
        :param hold: (bool) boolean to indicate if the coroutine should wait to return until the measurement is complete.
        :return: None, but outputs a .csv file
        """
        try:
            self.sr510_instance = measure_parameters["SR510"]
            self.sample_frequency = measure_parameters["sample_rate"]
            self.sample_time = measure_parameters["sample_time"]
            if metadata is not None:
                self.set_metadata(metadata)

            file_name = measure_parameters["storage_path"]
            if not append_to_existing:
                while os.path.exists(file_name):
                    file_name_split = file_name.split(".")
                    file_name = file_name_split[0] + "_." + file_name_split[1]

            # get instrument parameters #
            self.set_metadata(self.sr510_instance.quick_properties)
            results = Results(self, file_name)
            worker = Worker(results)
            worker.start()
            self.running = True
            if hold:
                while self.running:
                    await asyncio.sleep(0)

        except Exception as e:
            print(e)

