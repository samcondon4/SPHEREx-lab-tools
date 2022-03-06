""" This module provides the driver for the Oriel/Newport Cs260 Monochromator.
"""
import subprocess as sp
from pymeasure.instruments import Instrument


class CS260:

    wavelength = Instrument.control("WAVE?", "GOWAVE %f", """Float property representing
    the current wavelength setting in um. or nm.""", get_process=lambda w: w.stdout.decode("utf-8"))

    def __init__(self, resourceName, **kwargs):
        """ Initialize communication with the CS260 monochromator. Note that the USB interface
        of this device utilizes a set of Newport proprietary DLL drivers. The provided C++EXE.exe
        file wraps the communication with these files in a combiled binary that python can execute
        with the subprocess (:module:`.sp`) module.

        :param resourceName: Path to the compiled exe driver for DLL utilization. This should remain static.
        """

        self.resource_name = resourceName
        self.cs260_open()

    # C++ EXE Methods ###################################################################
    def cs260_open(self):
        cp = sp.run([self.resource_name, 'open'], capture_output=True, check=True)
        return cp

    def close(self):
        cp = sp.run([self.resource_name, 'close'], capture_output=True, check=True)
        return cp

    def list(self):
        cp = sp.run([self.resource_name, 'list'], capture_output=True, check=True)
        return cp

    def write(self, cmd):
        args = [self.resource_name, 'write', cmd]
        cp = sp.run(args, capture_output=True, check=True)
        return cp

    def values(self, cmd):
        args = [self.resource_name, 'ask']
        cp = sp.run(args, capture_output=True, check=True)
        return cp


