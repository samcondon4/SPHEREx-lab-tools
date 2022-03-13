""" Hardware configuration for the SPHEREx Spectral Calibration Measurement.
"""
import os

HOST = "131.215.200.118"
PORT = 6550

rec_name = f"TCPIP::{HOST}::{PORT}::SOCKET"

Mono = {
    "instance_name": "Monochromator",
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

Ndf = {
    "instance_name": "NDFWheel",
    "manufacturer": "edmund",
    "resource_name": "",
    "instrument": "NDF",
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
    "instance_name": "Lockin",
    "subinstruments": [
        Sr830, Sr510
    ]
}

INSTRUMENT_SUITE = [Mono, Ndf, Lockin]
