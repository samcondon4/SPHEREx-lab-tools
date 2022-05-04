"""
Hardware
--------
The spectral_cal control software implements control over the following instruments:

    - "ndf": Edmund Optics neutral density filter wheel.
    - "mono": Newport CS260 monochromator.
    - "lockin": Compound instrument wrapping the sr510 and sr830 lockin amplifiers.

Each of these hardware components must be plugged into the computer and turned on or errors will be thrown when the
nominal configuration is imported. Note that the monochromator is controlled via an interface to the mono control laptop
on the optical bench. To start the mono control laptop interface, start an anaconda prompt on the laptop and run
the following code::

   cd Documents\Github\SPHERExLabTools
   conda activate spherexlabtools
   python
   from spherexlabtools.instruments.spherex import MonoControlServer
   mserve = MonoControlServer()
   mserve.start()

These steps must be executed **before** creating the experiment object with exp = slt.create_experiment(sc).
"""
HOST = "131.215.200.118"
PORT = 6550

rec_name = f"TCPIP::{HOST}::{PORT}::SOCKET"


Readout = {
    "instance_name": "readout",
    "manufacturer": "spherex",
    "resource_name": "",
    "instrument": "DetectorCom"
}


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

INSTRUMENT_SUITE = [Ndf, Mono, Lockin, Readout]
