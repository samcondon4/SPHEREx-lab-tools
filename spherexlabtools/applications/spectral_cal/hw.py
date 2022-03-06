""" Hardware configuration for the SPHEREx Spectral Calibration Measurement.
"""
import os

Mono = {
    "instance_name": "Monochromator",
    "manufacturer": "newport",
    "resource_name": os.path.join(os.getcwd(), "spherexlabtools", "instruments",
                                  "newport", "CS260_DLLs", "C++EXE.exe"),
    "instrument": "CS260",
    "params": {
        "units": "UM"
    }
}

INSTRUMENT_SUITE = [Mono]
