""" This module provides the driver for the Oriel/Newport Cs260 Monochromator.
"""
import numpy as np
import subprocess as sp
from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_range, strict_discrete_set


class CS260:

    wavelength = Instrument.control("WAVE?", "GOWAVE %f", """Float property representing
    the current wavelength setting in um. or nm. This property can be set.""")

    grating = Instrument.control("GRAT?", "GRAT %i", """Integer property representing
    the current grating setting. This property can be set.""",
                                 validator=strict_discrete_set,
                                 values=[1, 2, 3])

    osf = Instrument.control("FILTER?", "FILTER %i", """Integer property representing the current
    order sort filter setting. This property can be set.""",
                             validator=strict_discrete_range,
                             values=[1, 7, 1])

    shutter = Instrument.control("SHUTTER?", "SHUTTER %s", """String property representing the current
    shutter setting. This property can be set.""",
                                 validator=strict_discrete_set,
                                 values=["O", "C"])

    units = Instrument.control("UNITS?", "UNITS %s", """String property representing the current units of the
    wavelength setting. This property can be set with "NM" for nanometers and "UM" for microns.""",
                               validator=strict_discrete_set,
                               values=["NM", "UM"])

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
        args = [self.resource_name, 'ask', cmd]
        cp = sp.run(args, capture_output=True, check=True)
        return cp.stdout.decode("utf-8")


