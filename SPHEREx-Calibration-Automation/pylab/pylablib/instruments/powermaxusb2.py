"""powermaxusb:

    This module implements a getter/setter wrapper for the powermax usb
    power sensor

Sam Condon, 07/02/2021
"""

import pyvisa
import pandas as pd
from pylablib.instruments.pylablib_instrument import Instrument
from pylablib.housekeeping import Housekeeping


class Powermax(Instrument, Housekeeping):

    def __init__(self, log_path=".\\housekeeping\\Powermax.csv"):
        Instrument.__init__(self)
        Housekeeping.__init__(self)

        # Configure open method ##########################
        self.set_open_method(self.open_com)
        self.com = None
        ##################################################

        # Configure parameters ###################################################
        self.add_get_parameter("system status", self.get_system_status)
        self.add_get_parameter("sensor temperature", self.get_sensor_temperature)
        self.add_get_parameter("sync timer", self.get_system_sync_timer)
        self.add_set_parameter("sync timer", self.set_system_sync_timer)
        self.add_get_parameter("error count", self.get_error_count)
        self.add_get_parameter("error", self.get_error)
        self.add_set_parameter("error", self.clear_error)
        self.add_get_parameter("active wavelength", self.get_wavelength)
        self.add_set_parameter("active wavelength", self.set_wavelength)
        self.add_get_parameter("gain compensation", self.get_gain_compensation)
        self.add_set_parameter("gain compensation", self.set_gain_compensation)
        self.add_set_parameter("zero", self.set_zero)
        self.add_get_parameter("data", self.get_data)
        ############################################################################

        # Set housekeeping parameters #######################
        self.set_log_path(log_path)
        self.set_log_method("Powermax", self.log_data)
        #####################################################

    def open_com(self):
        '''open_com:

            Open communication channel to Powermax USB sensor as a pyVISA resource.
        '''
        open_fail = 1
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        for i in resources:
            try:
                rec = rm.open_resource(i)
                rec_id = rec.query('*IDN?')
            except Exception as e:
                e = 0
            else:
                if "PowerMax USB" in rec_id:
                    self.com = rec
                    open_fail = 0
                    break
        if open_fail:
            raise RuntimeError("PowerMax USB Sensor not found")
        else:
            print("PowerMax USB Sensor found at:")
            print(self.com.resource_info.alias)

    # PARAMETER GETTERS/SETTERS ################################################
    def get_system_status(self):
        return self.com.query("SYSTem:STATus?")

    def get_sensor_temperature(self):
        return self.com.query("SYSTem:INFormation:TEMPerature?")

    def get_system_sync_timer(self):
        return self.com.query("SYSTem:SYNC?")

    def set_system_sync_timer(self, dummy):
        """set_system_sync_timer: sets system sync timer to 0
        """
        self.com.write("SYSTem:SYNC")

    def get_error_count(self):
        return self.com.query("SYSTem:ERRor:COUNt?")

    def get_error(self, all=False):
        if not all:
            return self.com.query("SYSTem:ERRor:NEXT?")
        else:
            return self.com.query("SYSTem:ERRor:ALL?")

    def clear_error(self):
        self.com.write("SYSTem:ERRor:CLEar")

    def get_wavelength(self):
        return self.com.query("CONFigure:WAVElength?")

    def set_wavelength(self, wave):
        self.com.write("CONFigure:WAVElength {}".format(wave))

    def get_gain_compensation(self):
        return self.com.query("CONFigure:GAIN:COMPensation?")

    def set_gain_compensation(self, gc):
        self.com.write("CONFigure:GAIN:COMPensation {}".format(gc))

    def set_zero(self):
        self.com.write("CONFigure:ZERO")

    def get_data(self):
        return self.com.query("READ?")

    def log_data(self):
        data = self.get_data().split(',')[0]
        time = Housekeeping.time_sync_method()
        write_df = pd.DataFrame({"Time-stamp": [time], "Watts": [data], "Wavelength": [float(self.get_wavelength())*1e-3]})
        try:
            df = pd.read_csv(self.log_path)
        except pd.errors.EmptyDataError as e:
            header = True
        else:
            header = False
        write_df.to_csv(self.log_path, mode='a', header=header, index=False)

    async def get_log(self, start=None, end=None, final_val=False):
        df = pd.read_csv(self.log_path)
        if final_val:
            df = df.iloc[-1]
        return df
    #############################################################################
