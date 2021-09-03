import asyncio
from time import sleep
import datetime
import numpy as np
from pymeasure.experiment import Procedure, Worker, Results
from pymeasure.experiment import FloatParameter
from pylabinst.SR830 import SR830


class Sr830Procedure(Procedure):

    sr830_instance = None
    sample_frequency = FloatParameter("Sample Frequency", units="Hz.", default=4,
                                      minimum=2**-4, maximum=2**9)
    sample_time = FloatParameter("Sample Time", units="s.", default=10)
    metadata = {}

    DATA_COLUMNS = ["Time Stamp", "X Channel Voltage (V.)", "Y Channel Voltage (V.)"]

    def execute(self):
        """ Description: main method for the procedure.
        :return: Outputs a .csv file with Sr830 data
        """
        if self.sr830_instance is not None:
            sample_period = 1/self.sample_frequency
            samples = int(np.ceil(self.sample_frequency * self.sample_time))
            for i in range(samples):
                time_stamp = datetime.datetime.now()
                voltage = self.sr830_instance.snap().split(",")
                x_voltage = voltage[0]
                y_voltage = voltage[1]
                out_dict = {"Time Stamp": time_stamp}
                for key in self.metadata:
                    out_dict[key] = self.metadata[key]
                out_dict["X Channel Voltage (V.)"] = x_voltage
                out_dict["Y Channel Voltage (V.)"] = y_voltage
                self.emit('results', out_dict)
                sleep(sample_period)
        else:
            raise RuntimeError("No valid SR830 class instance has been passed to the procedure.")

    def set_metadata(self, meta_dict):
        """Description: add metadata to include to the output .csv file

        :param meta_dict: (dict) Dictionary with keys corresponding to .csv column header and values corresponding to
                          the value to place under the header.
        :return: None
        """
        keys_list = list(meta_dict.keys())
        self.DATA_COLUMNS = [self.DATA_COLUMNS[0]] + keys_list + self.DATA_COLUMNS[-2:]
        for key in keys_list:
            self.metadata[key] = meta_dict[key]


async def run_sr830_procedure(sr830, fs, sample_time, storage_path, metadata=None):
    sr830_proc = Sr830Procedure()
    sr830_proc.sr830_instance = sr830
    sr830_proc.sample_frequency = fs
    sr830_proc.sample_time = sample_time
    if metadata is not None:
        sr830_proc.set_metadata(metadata)

    results = Results(sr830_proc, storage_path)
    worker = Worker(results)
    worker.start()
    worker.join(timeout=100)


async def main():
    fs = 4
    sample_time = 10
    storage_path = ".\\test.csv"
    metadata = {"grating": 2, "osf": "OSF1", "wavelength": 2.3}
    sr830 = SR830()
    await sr830.open()
    await asyncio.create_task(run_sr830_procedure(sr830, fs, sample_time, storage_path, metadata=metadata))


if __name__ == "__main__":
    asyncio.run(main())
