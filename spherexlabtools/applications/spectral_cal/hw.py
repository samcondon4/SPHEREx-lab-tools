""" Hardware configuration for the SPHEREx Spectral Calibration Measurement.
"""
import os

HOST = "131.215.200.118"
PORT = 6550

rec_name = f"TCPIP::{HOST}::{PORT}::SOCKET"


Ndf = {
    "instance_name": "ndf",
    "manufacturer": "edmund",
    "resource_name": "",
    "instrument": "NDF",
}


Mono = {
    "instance_name": "mono",
    "manufacturer": "spherex",
    "resource_name": rec_name,
    "instrument": "MonoControlClient",
    "params": {
        "units": "UM"
    },
    "kwargs": {
        "timeout": 10000
    }
}


Sr510 = {
    "instance_name": "sr510",
    "manufacturer": "srs",
    "resource_name": "GPIB0::6::INSTR",
    "instrument": "SR510"
}

Sr830 = {
    "instance_name": "sr830",
    "manufacturer": "srs",
    "resource_name": "GPIB0::15::INSTR",
    "instrument": "SR830"
}

Lockin = {
    "instance_name": "lockin",
    "subinstruments": [
        Sr830, Sr510
    ]
}

INSTRUMENT_SUITE = [Ndf, Mono, Lockin]
