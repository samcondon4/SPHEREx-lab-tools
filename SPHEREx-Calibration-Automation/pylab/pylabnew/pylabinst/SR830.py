"""SRS830m: This module implements a getter/setter based control wrapper for the SRS830m Lock-in amplifier

Sam Condon, 07/01/2021
"""

import pyvisa
import numpy as np
import asyncio
import struct
from time import sleep
import datetime
from pymeasure.experiment import Procedure, Worker, Results
from pymeasure.experiment import FloatParameter
from pylabinst.pylabinst_instrument_base import Instrument


class Sr830Measurement(Procedure):

    sr830_instance = None
    sample_frequency = FloatParameter("Sample Frequency", units="Hz.", default=4,
                                      minimum=2**-4, maximum=2**9)
    sample_time = FloatParameter("Sample Time", units="s.", default=10)
    metadata = {}

    DATA_COLUMNS = ["Time Stamp", "X Channel Voltage (V.)", "Y Channel Voltage (V.)", "Lia Status Register",
                    "Error Status Register"]

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
                lia_status = self.sr830_instance.get_lia_status()
                err_status = self.sr830_instance.get_error_status()
                out_dict = {"Time Stamp": time_stamp}
                for key in self.metadata:
                    out_dict[key] = self.metadata[key]
                out_dict["X Channel Voltage (V.)"] = x_voltage
                out_dict["Y Channel Voltage (V.)"] = y_voltage
                out_dict["Lia Status Register"] = lia_status
                out_dict["Error Status Register"] = err_status
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
        self.DATA_COLUMNS = [self.DATA_COLUMNS[0]] + keys_list + self.DATA_COLUMNS[-4:]
        self.metadata = meta_dict


class SR830(Instrument):

    SNAP_ENUMERATION = {"x": 1, "y": 2, "r": 3, "theta": 4,
                        "aux in 1": 5, "aux in 2": 6, "aux in 3": 7, "aux in 4": 8,
                        "frequency": 9, "ch1": 10, "ch2": 11}

    def __init__(self, gpib_id="GPIB0::8::INSTR", log_path=".\\housekeeping\\Lockin.csv"):
        Instrument.__init__(self)

        # Configure open method and pyvisa resources #################################
        self.set_open_method(self.open_com)
        self.gpib_id = gpib_id
        self.pyvisa_rm = None
        self.inst = None
        #############################################################################

        # Measurement class ###########################
        self.measure_procedure = Sr830Measurement()
        ###############################################

        # Add getter and setter methods to Instrument base class ###############################
        self.add_get_parameter("current phase", self.get_phase)
        self.add_set_parameter("current phase", self.set_phase)
        self.add_get_parameter("reference frequency", self.get_reference_frequency)
        self.add_set_parameter("reference frequency", self.set_reference_frequency)
        self.add_get_parameter("current sensitivity", self.get_sensitivity)
        self.add_set_parameter("current sensitivity", self.set_sensitivity)
        self.add_get_parameter("current time constant", self.get_time_constant)
        self.add_set_parameter("current time constant", self.set_time_constant)
        self.add_get_parameter("current sample rate", self.get_sample_rate)
        self.add_set_parameter("current sample rate", self.set_sample_rate)

        # Status registers ###############
        self.add_get_parameter("sr830 lia status", self.get_lia_status)
        self.add_get_parameter("sr830 error status", self.get_error_status)
        #########################################################################################

        # SR830 specific attributes ###############################
        self.sensitivity = None
        self.time_constant = None
        self.sample_rate = None
        self.is_settled = False
        ###########################################################

    def open_com(self):
        """open_com: Open a communication channel with the SR830 lock-in amplifier
        """
        self.pyvisa_rm = pyvisa.ResourceManager()
        self.inst = self.pyvisa_rm.open_resource(self.gpib_id)
        self.write("REST")
        asyncio.create_task(self.get_parameters("All"))

    # PARAMETER GETTER/SETTERS ##############################################################
    def get_phase(self):
        return str(self.query("PHAS"))

    def set_phase(self, phase):
        """set_phase:

            Set lockin phase shift. Either float, int or string "auto" are valid
            inputs. Passing "auto" will execute the auto phase function.

        """
        t = type(phase)
        if t is float or t is int:
            self.write("PHAS{}".format(phase))
        elif t is str:
            if phase == "auto":
                self.write("APHS")
        else:
            raise TypeError("set_phase() expects input of type float or string 'auto' "
                            "but {} was given".format(type(phase)))

    def get_reference_frequency(self):
        return str(self.query("FREQ"))

    def set_reference_frequency(self, rfreq):
        arg_type = type(rfreq)
        if arg_type is float:
            self.write("FREQ{}".format(rfreq))
        else:
            raise TypeError("set_reference_frequency() expects input of type float but {} was given".format(arg_type))

    def get_sensitivity(self):
        sens_ind = float(self.query("SENS"))
        if sens_ind == 0:
            sens = 2e-9
        elif sens_ind == 1:
            sens = 5e-9
        else:
            sens_ind -= 2
            sens_ind_mod = sens_ind % 3
            val = 1
            if sens_ind_mod == 0:
                val = 1
            elif sens_ind_mod == 1:
                val = 2
            elif sens_ind_mod == 2:
                val = 5
            sens = val * 10 ** (-8 + sens_ind // 3)

        self.sensitivity = round(sens, 7)
        return str(self.sensitivity)

    def set_sensitivity(self, sens):
        self.is_settled = False
        sens_set = True
        if sens == 2e-9:
            self.write("SENS 0")
        elif sens == 5e-9:
            self.write("SENS 1")
        elif sens == 10e-9:
            self.write("SENS 2")
        elif sens == 20e-9:
            self.write("SENS 3")
        elif sens == 50e-9:
            self.write("SENS 4")
        elif sens == 100e-9:
            self.write("SENS 5")
        elif sens == 200e-9:
            self.write("SENS 6")
        elif sens == 500e-9:
            self.write("SENS 7")
        elif sens == 1e-6:
            self.write("SENS 8")
        elif sens == 2e-6:
            self.write("SENS 9")
        elif sens == 5e-6:
            self.write("SENS 10")
        elif sens == 10e-6:
            self.write("SENS 11")
        elif sens == 20e-6:
            self.write("SENS 12")
        elif sens == 50e-6:
            self.write("SENS 13")
        elif sens == 100e-6:
            self.write("SENS 14")
        elif sens == 200e-6:
            self.write("SENS 15")
        elif sens == 500e-6:
            self.write("SENS 16")
        elif sens == 1e-3:
            self.write("SENS 17")
        elif sens == 2e-3:
            self.write("SENS 18")
        elif sens == 5e-3:
            self.write("SENS 19")
        elif sens == 10e-3:
            self.write("SENS 20")
        elif sens == 20e-3:
            self.write("SENS 21")
        elif sens == 50e-3:
            self.write("SENS 22")
        elif sens == 100e-3:
            self.write("SENS 23")
        elif sens == 200e-3:
            self.write("SENS 24")
        elif sens == 500e-3:
            self.write("SENS 25")
        elif sens == 1:
            self.write("SENS 26")
        else:
            sens_set = False
            raise RuntimeError("Invalid input given to set_sensitivity()")

        if sens_set:
            self.sensitivity = sens

    def get_time_constant(self):
        tc_ind = float(self.query("OFLT"))
        tc_ind_mod = tc_ind % 2
        val = 1
        if tc_ind_mod == 0:
            val = 1
        elif tc_ind_mod == 1:
            val = 3

        tc = val * 10 ** (-5 + tc_ind // 2)
        self.time_constant = tc
        return str(tc)

    def set_time_constant(self, tc):
        self.is_settled = False
        tc_set = True
        if tc == 10e-6:
            cmd = "OFLT 0"
        elif tc == 30e-6:
            cmd = "OFLT 1"
        elif tc == 100e-6:
            cmd = "OFLT 2"
        elif tc == 300e-6:
            cmd = "OFLT 3"
        elif tc == 1e-3:
            cmd = "OFLT 4"
        elif tc == 3e-3:
            cmd = "OFLT 5"
        elif tc == 10e-3:
            cmd = "OFLT 6"
        elif tc == 30e-3:
            cmd = "OFLT 7"
        elif tc == 100e-3:
            cmd = "OFLT 8"
        elif tc == 300e-3:
            cmd = "OFLT 9"
        elif tc == 1:
            cmd = "OFLT 10"
        elif tc == 3:
            cmd = "OFLT 11"
        elif tc == 10:
            cmd = "OFLT 12"
        elif tc == 30:
            cmd = "OFLT 13"
        elif tc == 100:
            cmd = "OFLT 14"
        elif tc == 300:
            cmd = "OFLT 15"
        elif tc == 1e3:
            cmd = "OFLT 16"
        elif tc == 3e3:
            cmd = "OFLT 17"
        elif tc == 10e3:
            cmd = "OFLT 18"
        elif tc == 30e3:
            cmd = "OFLT 19"
        else:
            raise RuntimeError("Invalid input given to set_time_constant()")

        if tc_set:
            self.time_constant = tc
            self.write(cmd)

    def get_sample_rate(self):
        srate_ind = float(self.query("SRAT"))
        self.sample_rate = 2 ** (srate_ind - 4)
        return str(self.sample_rate)

    def set_sample_rate(self, srate):
        valid_input = False
        for i in range(-4, 10):
            if srate == 2 ** i:
                self.write("SRAT{}".format(i + 4))
                valid_input = True
                break
        if not valid_input:
            raise RuntimeError("Invalid input given to set_sample_rate()")

        if valid_input:
            self.sample_rate = srate

    def get_lia_status(self):
        """
        
        """
        lia_bytes = self.query("LIAS")
        return "{0:b}".format(int(lia_bytes))

    def get_error_status(self):
        """
        
        """
        err_bytes = self.query("ERRS")
        return "{0:b}".format(int(err_bytes))

    def snap(self, val1="X", val2="Y", *vals):
        """ Method that records and retrieves 2 to 6 parameters at a single
        instant. The parameters can be one of: X, Y, R, Theta, Aux In 1,
        Aux In 2, Aux In 3, Aux In 4, Frequency, CH1, CH2.
        Default is "X" and "Y".
        :param val1: first parameter to retrieve
        :param val2: second parameter to retrieve
        :param vals: other parameters to retrieve (optional)
        """
        if len(vals) > 4:
            raise ValueError("No more that 6 values (in total) can be captured"
                             "simultaneously.")

        # check if additional parameters are given as a list
        if len(vals) == 1 and isinstance(vals[0], (list, tuple)):
            vals = vals[0]

        # make a list of all vals
        vals = [val1, val2] + list(vals)

        vals_idx = [str(self.SNAP_ENUMERATION[val.lower()]) for val in vals]

        command = "SNAP? " + ",".join(vals_idx)
        return self.query(command)

    def write(self, command):
        self.inst.write(command)

    def query(self, parameter):
        return self.inst.query("{}?".format(parameter))

    async def start_measurement(self, measure_parameters, metadata=None):
        """Description: Run a measurement on the sr830 lockin.

        :param measure_parameters: (dict) dictionary containing parameters of the measurement. Should be of the form:
                                          {"sample rate": <(float) sampling frequency in Hz.>,
                                           "sample time": <(float) sample time in s.>,
                                          "measurement storage path": <(str) .csv file path>}
        :param metadata: (dict) dictionary containing additional metadata to include
        :return: None, but outputs a .csv file
        """
        sr830_proc = Sr830Measurement()
        sr830_proc.sr830_instance = self
        sr830_proc.sample_frequency = measure_parameters["sample rate"]
        sr830_proc.sample_time = measure_parameters["sample time"]
        if metadata is not None:
            sr830_proc.set_metadata(metadata)

        results = Results(sr830_proc, measure_parameters["measurement storage path"])
        worker = Worker(results)
        worker.start()
        worker.join(timeout=100)
    #########################################################################################

    # STATIC METHOD HELPERS ####################################################
    @staticmethod
    def calc_sens_val_mult_unit(lockin_params):
        """calc_sens_val_mult_unit:
            Given a set of lockin parameters, return the sensitivity value, multiplier, and units as seen on the
            SRS830m lockin front panel.
        """
        sens = lockin_params["sensitivity"]
        sens_log = np.log10(sens)
        # Calculate sensitivity multiplier ####
        if sens_log < 0:
            sens_mult = np.floor(sens_log)
        else:
            sens_mult = np.ceil(sens_log)
        #######################################

        sens_val = sens * (10 ** (-1 * sens_mult))

        # Determine proper units and multiplier ##############
        units = None
        if sens_log >= 0:
            units = "V."
            sens_div = sens / 10
            if sens_div >= 10:
                sens_mult = 100
            elif sens_div >= 1:
                sens_mult = 10
            elif sens_div >= 0.1:
                sens_mult = 1
        elif -3 <= sens_log < 0:
            units = "mV."
            sens_div = sens / 10e-3
            if sens_div >= 10:
                sens_mult = 100
            elif sens_div >= 1:
                sens_mult = 10
            elif sens_div >= 0.1:
                sens_mult = 1
        elif -6 <= sens_log < -3:
            units = "uV."
            sens_div = sens / 10e-6
            if sens_div >= 10:
                sens_mult = 100
            elif sens_div >= 1:
                sens_mult = 10
            elif sens_div >= 0.1:
                sens_mult = 1
        elif -9 <= sens_log < -6:
            sens_div = sens / 10e-9
            if sens_div >= 10:
                sens_mult = 100
            elif sens_div >= 1:
                sens_mult = 10
            elif sens_div >= 0.1:
                sens_mult = 1
            units = "nV."
        #######################################################

        return {"value": sens_val, "multiplier": sens_mult, "units": units}

    @staticmethod
    def calc_tc_val_mult_unit(lockin_params):

        tc = lockin_params["time constant"]
        tc_log = np.log10(tc)
        if tc_log < 0:
            tc_mult = np.floor(tc_log)
        else:
            tc_mult = np.ceil(tc_log)
        tc_val = tc * (10 ** (-1 * tc_mult))

        units = None
        if tc_log >= 3:
            units = "ks."
            tc_div = tc / 1e3
            if tc_div >= 10:
                tc_mult = 100
            elif tc_div >= 1:
                tc_mult = 10
            elif tc_div >= 0.1:
                tc_mult = 1
        elif 0 <= tc_log < 3:
            units = "s."
            if tc >= 100:
                tc_mult = 100
            elif tc >= 10:
                tc_mult = 10
            elif tc >= 1:
                tc_mult = 1
        elif -3 <= tc_log < 0:
            units = "ms."
            tc_div = tc / 1e-3
            if tc_div >= 10:
                tc_mult = 100
            elif tc_div >= 1:
                tc_mult = 10
            elif tc_div >= 0.1:
                tc_mult = 1

        return {"value": tc_val, "multiplier": tc_mult, "units": units}
    #############################################################################
