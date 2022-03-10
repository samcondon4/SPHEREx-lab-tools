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

INSTRUMENT_SUITE = [Mono]
