"""SRS830m: This module implements a getter/setter based control wrapper for the SRS830m Lock-in amplifier

Sam Condon, 07/01/2021
"""

import pyvisa
import numpy as np
import asyncio
import struct
import pandas as pd
from pylabinst.pylabinst_instrument_base import Instrument


class SR830(Instrument):

    def __init__(self, gpib_id="GPIB0::8::INSTR", log_path=".\\housekeeping\\Lockin.csv"):
        Instrument.__init__(self)

        # Configure open method and pyvisa resources #################################
        self.set_open_method(self.open_com)
        self.gpib_id = gpib_id
        self.pyvisa_rm = None
        self.inst = None
        #############################################################################

        # Add getter and setter methods to Instrument base class ###############################
        self.add_get_parameter("current phase", self.get_phase)
        self.add_set_parameter("current phase", self.set_phase)
        self.add_get_parameter("reference frequency", self.get_reference_frequency)
        self.add_set_parameter("reference frequency", self.set_reference_frequency)
        self.add_get_parameter("current sensitivity", self.get_sensitivity)
        self.add_set_parameter("current sensitivity", self.set_sensitivity)
        self.add_get_parameter("current time constant", self.get_time_constant)
        self.add_set_parameter("current time constant", self.set_time_constant)
        self.add_get_parameter("sample rate", self.get_sample_rate)
        self.add_set_parameter("sample rate", self.set_sample_rate)

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
        sens_ind = self.query("SENS")
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
        tc_ind = self.query("OFLT")
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
        srate_ind = self.query("SRAT")
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

    def write(self, command):
        self.inst.write(command)

    def query(self, parameter):
        return float(self.inst.query("{}?".format(parameter)))

    async def measure_hk(self):
        """measure_hk:

            This coroutine records data from the SR830 lockin as housekeeping.
            That is, all data recorded here is logged to the Lockin.csv hk file.
        """
        async with self.log_lock:
            data = float(self.inst.query("OUTP?1"))
            lia = self.get_lia_status()
            err = self.get_error_status()
            time = Housekeeping.time_sync_method()
            write_df = pd.DataFrame(
                {"Time-stamp": [time], "Detector Voltage": [data], "lia status": [lia], "error status": [err]}
            )
            self.append_to_log(write_df)

    async def measure(self, sample_time, settled_override=False):
        """measure:
            
            This coroutine continuously reads data from the SR830 lockin
            at the set sample rate for the specified sample time and returns
            all data that was read. The array of data that is returned is the 
            output voltage from the detector input to the lockin
            
            Params:
                sample_time: time (in seconds) to record data from the lockin
                settled_override: Normally, this method will wait for 5 times
                                  the set time constant to begin recording data.
                                  If this argument is set to True, then data
                                  recording begins without waiting this time.
        """
        fs = self.get_sample_rate()
        tc = self.get_time_constant()
        sens = self.get_sensitivity()
        if not self.is_settled and not settled_override:
            await asyncio.sleep(5 * tc)
            self.is_settled = True
        # initialize data dictionary
        data_dict = {"detector voltage": [0 for _ in range(int(sample_time * fs))],
                     "lia status": None,
                     "error status": None
                     }

        # set output interface to GPIB
        self.write("OUTX1")
        # start data transfer via fast mode
        self.write("FAST2;STRD")

        # read data
        for i in range(len(data_dict["detector voltage"])):
            data_read = self.inst.read_bytes(4)[:2]
            data_dict["detector voltage"][i] = (struct.unpack("h", data_read)[0] / 30000) * sens
            await asyncio.sleep(0)

        # halt fast mode data transfer
        self.write("FAST0;PAUS")
        # reset the data buffer #
        self.write("REST")
        # dummy query to clear GPIB queue
        try:
            self.inst.query("OEXP?1")
        except UnicodeDecodeError as e:
            pass

        data_dict["lia status"] = self.get_lia_status()
        data_dict["error status"] = self.get_error_status()

        return data_dict

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
