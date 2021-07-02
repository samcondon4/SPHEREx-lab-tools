"""SRS830m: This module implements a getter/setter based control wrapper for the SRS830m Lock-in amplifier

Sam Condon, 07/01/2021
"""

from pylablib.instruments.pylablib_instrument import Instrument


class SRS830m(Instrument):

    def __init__(self):
        super().__init__("SRS830m")

        self.add_get_parameter("phase", self.get_phase)
        self.add_set_parameter("phase", self.set_phase)
        self.add_get_parameter("reference frequency", self.get_reference_frequency)
        self.add_set_parameter("reference frequency", self.set_reference_frequency)
        self.add_get_parameter("sensitivity", self.get_sensitivity)
        self.add_set_parameter("sensitivity", self.set_sensitivity)
        self.add_get_parameter("time constant", self.set_time_constant)
        self.add_set_parameter("time constant", self.get_time_constant)
        self.add_get_parameter("sample rate", self.get_sample_rate)
        self.add_set_parameter("sample rate", self.set_sample_rate)

    # PARAMETER GETTER/SETTERS ##############################################################
    def get_phase(self):
        return self.query("PHAS")

    def set_phase(self, phase):
        if type(phase) is float:
            self.write("PHAS {}".format(phase))
        else:
            raise TypeError("set_phase() expects input of type float but {} was given".format(type(phase)))

    def get_reference_frequency(self):
        return self.query("FREQ")

    def set_reference_frequency(self, rfreq):
        arg_type = type(rfreq)
        if arg_type is float:
            self.write("FREQ {}".format(rfreq))
        else:
            raise TypeError("set_reference_frequency() expects input of type float but {} was given".format(arg_type))

    def get_sensitivity(self):
        return self.query("SENS?")

    def set_sensitivity(self, sens):
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
            raise RuntimeError("Invalid input given to set_sensitivity()")

    def get_time_constant(self):
        return self.query("OFLT?")

    def set_time_constant(self, tc):
        if tc == 10e-6:
            self.write("OFLT 0")
        elif tc == 30e-6:
            self.write("OFLT 1")
        elif tc == 100e-6:
            self.write("OFLT 2")
        elif tc == 300e-6:
            self.write("OFLT 3")
        elif tc == 1e-3:
            self.write("OFLT 4")
        elif tc == 3e-3:
            self.write("OFLT 5")
        elif tc == 10e-3:
            self.write("OFLT 6")
        elif tc == 30e-3:
            self.write("OFLT 7")
        elif tc == 100e-3:
            self.write("OFLT 8")
        elif tc == 300e-3:
            self.write("OFLT 9")
        elif tc == 1:
            self.write("OFLT 10")
        elif tc == 3:
            self.write("OFLT 11")
        elif tc == 10:
            self.write("OFLT 12")
        elif tc == 30:
            self.write("OFLT 13")
        elif tc == 100:
            self.write("OFLT 14")
        elif tc == 300:
            self.write("OFLT 15")
        elif tc == 1e3:
            self.write("OFLT 16")
        elif tc == 3e3:
            self.write("OFLT 17")
        elif tc == 10e3:
            self.write("OFLT 18")
        elif tc == 30e3:
            self.write("OFLT 19")
        else:
            raise RuntimeError("Invalid input given to set_time_constant()")

    def get_sample_rate(self):
        return self.query("SRAT?")

    def set_sample_rate(self, srate):
        valid_input = False
        for i in range(-4, 10):
            if srate == 2**i:
                self.write("SRAT {}".format(i+4))
                valid_input = True
                break
        if not valid_input:
            raise RuntimeError("Invalid input given to set_sample_rate()")

    def write(self, command):
        pass

    def query(self, parameter):
        pass
    #########################################################################################


