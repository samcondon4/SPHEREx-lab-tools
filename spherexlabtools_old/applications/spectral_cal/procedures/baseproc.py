"""pylabsm_baseproc:

    This provides a base procedure
"""
import os
import asyncio
import datetime
#from pymeasure.display.plotter import Plotter
from pymeasure.experiment import Procedure, Worker, Results


class SmBaseProc(Procedure):

    def __init__(self):

        self._timestamp_method = lambda: str(datetime.datetime.now().timestamp())
        self._metadata = {}
        self.running = False
        self.worker = None
        self.storage_path = None
        self.hold = False
        super().__init__()

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

    async def run(self, measurement_parameters=None, plot=False, append_to_existing=False, hold=False):
        """Description: Run a measurement for any device.

        :param measure_parameters: (dict) dictionary containing parameters of the measurement.
        :param plot:               (bool) boolean to visualize measurement in popup plot.
        :param append_to_existing: (bool) boolean to indicate if data should be saved to an existing file or to create
                                   a new file.
        :param hold: (bool) boolean to indicate if the coroutine should wait to return until the measurement is complete.
        :return: None, but outputs a .csv file
        """
        self.hold = hold

        if measurement_parameters is not None:
            print("Base procedure received parameters = {}".format(measurement_parameters))
            for mkey, mval in measurement_parameters.items():
                setattr(self, mkey, mval)

        file_name = self.storage_path
        if not append_to_existing:
            while os.path.exists(file_name):
                file_name_split = file_name.split(".")
                file_name = file_name_split[0] + "_." + file_name_split[1]

        results = Results(self, file_name)

        """
        if plot:
            plotter = Plotter(results)
            plotter.start()
        """

        self.worker = Worker(results)
        self.worker.start()

        self.running = True
        if hold:
            while self.running:
                await asyncio.sleep(0)
