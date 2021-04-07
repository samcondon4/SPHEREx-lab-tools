import pdb
import pyvisa
import pandas as pd
import time, threading
from pylablib.instruments.repeatedtimer import RepeatedTimer

class PowermaxUSB:
    _info_dict = {'ID': '*IDN?',
                  'STATUS': 'SYSTem:STATus?',
                  'TEMP': 'SYSTem:INFormation:TEMPerature?',
                  'TIMER': 'SYSTem:SYNC?',
                  'HANDSHAKE': 'SYSTem:COMMunicate:HANDshaking?',
                  'ERR_CNT': 'SYSTem:ERRor:COUNt?',
                  'ERR_NXT': 'SYSTem:ERRor:NEXT?',
                  'ERR_ALL': 'SYSTem:ERRor:ALL?',
                  'MEASURE_MODE': 'CONFigure:MEASure?',
                  'SPEEDUP': 'CONFigure:SPEedup?',
                  'WAVELENGTH_ACTIVE': 'CONFigure:WAVElength?',
                  'WAVELENGTH_MIN': 'CONFigure:WAVElength?MINimum',
                  'WAVELENGTH_MAX': 'CONFigure:WAVElength?MAXimum',
                  'GAIN_COMP': 'CONFigure:GAIN:COMPensation?',
                  'GAIN_FACTOR': 'CONFigure:GAIN:FACTor?',
                  'POWER': 'READ?'
                  # accuracy mode
                  # pulse thermopile joules trigger level
                  # measurement data format
                  # sensor info
                  }

    _cmd_dict = {'RESET': '*RST',
                 'TIMER_ZERO': 'SYSTem:SYNC',
                 'POWER_ZERO': 'CONFigure:ZERO',
                 'RESTORE': 'SYSTem:RESTore',
                 'HANDSHAKING': 'SYSTem:COMMunicate:HANDshaking{}',
                 'CLR_ERR': 'SYSTem:ERRor:CLEar',
                 'MEASURE_MODE': 'CONFigure:MEASure{}',
                 'SPEEDUP': 'CONFigure:SPEedup{}',
                 'WAVELENGTH_ACTIVE': 'CONFigure:WAVElength{}',
                 'WAVELENGTH_MIN': 'CONFigure:WAVElengthMINimum{}',
                 'WAVELENGTH_MAX': 'CONFigure:WAVElengthMAXimum{}',
                 'GAIN_COMP': 'CONFigure:GAIN:COMPensation{}',
                 'GAIN_FACTOR': 'CONFigure:GAIN:FACTor{}',
                 # accuracy mode
                 # pulse thermopile joules trigger level
                 # measurement data format
                 # sensor info
                 }

    def __init__(self):
        self.com = None  # Holds pyVISA returned resource class
        self.error_record = None  # Store error records from sensor (associated method not implemented yet)

        self.open_com()  # Open communication channel to sensor
        self.data = {'Power': [],
                     'Flags': [],
                     'Timestamp': []}  # Dictionary to store measurements before converting to dataframe
        self.is_running = 0  # Flag to tell if timer is triggering periodic measurements
        self.is_handshaking = 0  # Flag to tell if handshaking mode is on (associated method not implemented yet)
        self.measure_mode = "W"  # Power measurement mode. Default is "W" for watts (method not implemented yet)
        self.wavelength_min = None  # Minimum wavelength for range of potential power measurements
        self.wavelength_max = None  # Maximum wavelength in range of potential power measurements
        self.wavelength_active = None  # Current wavelength that power measurements are taken from
        self.timer = RepeatedTimer(1, self.get_power)  # Repeted timer object to initiate or halt periodic measurements

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
        if (open_fail):
            print("PowerMax USB Sensor not found...")
            self.error_record = 1
        else:
            print("PowerMax USB Sensor found at:")
            print(self.com.resource_info.alias)

    def set_power_zero(self):
        '''set_power_zero:

            Set current power measurement as zero standard.
        '''
        self.set_data('POWER_ZERO')

    def set_timer_zero(self):
        '''set_timer_zero:

            Set internal synchronization timer count to zero.
        '''
        self.set_data('TIMER_ZERO')

    def set_wavelength(self, minimum=None, maximum=None, active=None):
        '''set_wavelength:

            Set minimum, maximum, and active wavelength to measure power.
            Can set one, two, or all three of the wavelength parameters with
            this method.
        '''
        wave_set = 1
        if (minimum != None):
            self.set_data('WAVELENGTH_MIN', val=minimum)
            wave_set = 0
        if (maximum != None):
            self.set_data('WAVELENGTH_MAX', val=maximum)
            wave_set = 0
        if (active != None):
            self.set_data('WAVELENGTH_ACTIVE', val=active)
            wave_set = 0

        if (wave_set != 0):
            print("Please specify a wavelength parameter to set.")

        return wave_set

    def start_measure(self, interval):
        '''start_measure:

            Start taking power measurements at a periodic interval, set in seconds.
        '''
        self.timer.interval = interval
        self.timer.start()
        self.is_running = 1

    def stop_measure(self):
        '''stop_measure:

            Stop periodic power measurements.
        '''
        self.timer.stop()
        self.is_running = 0

    def clear_data(self):
        '''clear_data:

            Reset internal data dictionary.
        '''
        self.data = {'Power': [],
                     'Flags': [],
                     'Timestamp': []}

    def get_power(self, rec=True):
        '''get_power:

            record most recent power measurement.
        '''
        power = self.get_info('POWER')
        if (rec == True):
            valstr = power.strip('\r\n')
            p, f, ts = valstr.split(',')
            self.data['Power'].append(float(p))
            self.data['Flags'].append(f)
            self.data['Timestamp'].append(float(ts))
        return power

    def get_info(self, qry_str):
        '''get_info:

            send query command to sensor. Valid queries are found in the _info_dict dictionary.
        '''
        return self.com.query(PowermaxUSB._info_dict[qry_str])

    def get_dataframe(self):
        '''get_dataframe:

            Convert current data dictionary into pandas dataframe and return this.
        '''
        return pd.DataFrame(self.data)

    def set_data(self, cmd_str, val=None):
        '''set_data:

            Send command to sensor. Valid commands are found in the _cmd_dict dictionary.
        '''
        if (val != None):
            self.com.write((PowermaxUSB._cmd_dict[cmd_str]).format(val))
        else:
            self.com.write(PowermaxUSB._cmd_dict[cmd_str])

    def reset(self):
        '''reset:

            Reset sensor to its most recent power on state.
        '''
        self.set_data('RESET')

    def restore(self):
        '''restore:

            Set sensor to its factory default settings.
        '''
        self.set_data('RESTORE')

    # Place holders: may implement these later on...
    '''
    def set_handshaking(self, onoff):

        self.set_data('HANDSHAKING', val=onoff)

    def set_measure_mode(self, mm):
        self.set_data('MEASURE_MODE', val=mm)

    def set_speedup(self, onoff):
        self.set_data('SPEEDUP', val=onoff)

    def set_gain(self, onoff=None, factor=None):
        gain_set = 0
        if(onoff != None):
            self.set_data('GAIN_COMP', comp)
            gain_set = 1
        if(factor != None):
            self.set_data('GAIN_FACTOR', factor)
            gain_set = 1
        if(gain_set != 1):
            print("Please specify gain parameter to set.")

    def clear_error(self):
        self.set_data('CLR_ERR')
    '''