""" ts_procs:

        Main module implementing custom procedures for the thermal surrogate measurements.
"""

import time
import threading
from spherexlabtools.procedures import BaseProcedure, LogProc
from spherexlabtools.parameters import ParameterInspect, Parameter, FloatParameter, IntegerParameter, BooleanParameter,\
                                       ListParameter


rec_lock = threading.Lock()


class DataLogProc(LogProc):
    """ Logging procedure utilizing the global lock defined above.
    """

    def execute(self):
        """ Override execute to use the lock defined above.
        """
        while not self.thread.should_stop():
            with rec_lock:
                self.get_properties()
            time.sleep(1/self.refresh_rate)


class Ls336AoutProc(BaseProcedure):
    """ Basic procedure to pend for the specified amount of time then set the analog output on a lakeshore.
    """

    analog_out = Parameter("Ls336 Mout3", default="[]")
    analog_out_times = Parameter("Ls336 Mout3 Set Time", default="[]")

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)
        self.ls336 = self.hw
        self.aout_floats = None
        self.aout_time_floats = None
        self.aout_pend_floats = None

    def startup(self):
        """ Initialize the thermal surrogate measurement.
        """
        BaseProcedure.startup(self)
        self.aout_floats = self.get_list_vals(self.analog_out)
        self.aout_time_floats = self.get_list_vals(self.analog_out_times)
        self.aout_pend_floats = [self.aout_time_floats[0]] + [self.aout_time_floats[i] - self.aout_time_floats[i-1]
                                                              for i in range(1, len(self.aout_time_floats))]

    def execute(self):
        """ Pend for the specified time.
        """
        i = 0
        for aout in self.aout_floats:
            time.sleep(self.aout_pend_floats[i])
            with rec_lock:
                self.ls336.mout3 = aout
            i += 1

    def shutdown(self):
        """ Shutdown the thermal surrogate measurement.
        """
        BaseProcedure.shutdown(self)
        self.aout_floats = None
        self.aout_pend_floats = None

    @staticmethod
    def get_list_vals(lst_str):
        """ Get a list of float values from a string formatted like a list.

        :param lst_str: String formatted like a list.
        """
        val_list = lst_str[1:-1].split(",")
        for i in range(len(val_list)):
            val_list[i] = float(val_list[i])
        return val_list
