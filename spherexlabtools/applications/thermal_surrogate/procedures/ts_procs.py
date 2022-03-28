""" ts_procs:

        Main module implementing custom procedures for the thermal surrogate measurements.
"""

import os
import time
import threading
from datetime import datetime
from spherexlabtools.thread import StoppableReusableThread
from spherexlabtools.procedures import BaseProcedure, LogProc
from spherexlabtools.parameters import ParameterInspect, Parameter, FloatParameter, IntegerParameter, BooleanParameter,\
                                       ListParameter


class Ls218TempProc(BaseProcedure):
    """ Basic procedure to log temperature data from the lakeshore 218.
    """

    # ancillary data written to by the Ls336AoutProc
    ancillary_lock = threading.Lock()
    ancillary_data = {}

    temperature_sample_rate = FloatParameter("Temperature Sample Rate", units="Hz.", default=1)
    filepath = Parameter("Output File Path", default=os.path.join(os.getcwd(), "test.csv"))

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)
        self.ls218 = self.hw

    def execute(self):
        """ Get temperature data and send to the appropriate viewers/recorders.
        """
        while not self.should_stop():
            t1 = self.ls218.temperature1
            self.emit("temperature1", t1)
            t2 = self.ls218.temperature2
            self.emit("temperature2", t2)
            """
            t3 = self.ls218.temperature3
            self.emit("temperature3", t3)
            t4 = self.ls218.temperature4
            self.emit("temperature4", t4)
            """
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            data_df = {"timestamp": [ts], "temperature1": [t1], "temperature2": [t2]}
            with Ls218TempProc.ancillary_lock:
                data_df.update(Ls218TempProc.ancillary_data)
            data_df.update({"filepath": self.filepath})
            self.emit("temp_to_csv", data_df)
            time.sleep(1/self.temperature_sample_rate)


class Ls336AoutProc(BaseProcedure):
    """ Basic procedure to pend for the specified amount of time then set the analog output on a lakeshore.
    """

    analog_out = Parameter("Mout3", default="[]")
    analog_out_pend = Parameter("Mout3 Set Pend Time", default="[]")
    temperature_sample_rate = FloatParameter("Temperature Sample Rate", units="Hz.", default=1)
    filepath = Parameter("Output File Path", default=os.path.join(os.getcwd(), "test.csv"))

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)
        self.ls336 = self.hw
        self.aout_floats = None
        self.aout_pend_floats = None
        self.temp_log_proc = None

    def startup(self):
        """ Initialize the thermal surrogate measurement.
        """
        BaseProcedure.startup(self)
        self.aout_floats = self.get_list_vals(self.analog_out)
        self.aout_pend_floats = self.get_list_vals(self.analog_out_pend)
        self.temp_log_proc = self.exp.procedures["Ls218TempProc"]
        self.temp_log_proc.temperature_sample_rate = self.temperature_sample_rate
        self.temp_log_proc.filepath = self.filepath

    def execute(self):
        """ Pend for the specified time.
        """
        i = 0
        for aout in self.aout_floats:
            time.sleep(self.aout_pend_floats[i])
            self.ls336.mout3 = aout
            aout = self.ls336.mout3
            self.emit("analog_out", aout)
            with Ls218TempProc.ancillary_lock:
                Ls218TempProc.ancillary_data.update({"Mout3": [aout]})
            if i == 0:
                self.exp.start_thread("Ls218TempProc", self.temp_log_proc)
            i += 1

    def shutdown(self):
        """ Shutdown the thermal surrogate measurement.
        """
        BaseProcedure.shutdown(self)
        self.aout_floats = None
        self.aout_pend_floats = None
        self.exp.stop_thread("Ls218TempProc")

    @staticmethod
    def get_list_vals(lst_str):
        """ Get a list of float values from a string formatted like a list.

        :param lst_str: String formatted like a list.
        """
        val_list = lst_str[1:-1].split(",")
        for i in range(len(val_list)):
            val_list[i] = float(val_list[i])
        return val_list
