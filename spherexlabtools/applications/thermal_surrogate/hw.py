"""
Hardware
--------

    - "ls218": LakeShore218 temperature monitor.
    - "ls336": LakeShore336 temperature controller.
    - "aglnt_daq": Agilent34970A multiplexing DMM.
    - "ts_log_hw": Compound instrument wrapping all the above drivers.

"""

from pyvisa.constants import Parity, StopBits


ls218 = {
    "instance_name": "ls218",
    "manufacturer": "lakeshore",
    "instrument": "LakeShore218",
    "resource_name": "ASRL/dev/ttyUSB1::INSTR",
    "kwargs": {
        "baud_rate": 9600,
        "data_bits": 7,
        "parity": Parity.odd,
        "stop_bits": StopBits.one,
        "write_termination": "\r\n",
    }
}

ls336 = {
    "instance_name": "ls336",
    "manufacturer": "lakeshore",
    "instrument": "LakeShore336",
    "resource_name": "ASRL/dev/ttyUSB4::INSTR",
    "kwargs": {
        "baud_rate": 57600,
        "data_bits": 7,
        "parity": Parity.odd,
        "stop_bits": StopBits.one,
        "write_termination": "\r\n",
        "read_termination": "\r\n"
    }
}

agilent_34970 = {
    "instance_name": "aglnt_daq",
    "manufacturer": "agilent",
    "instrument": "Agilent34970A",
    "resource_name": "ASRL/dev/ttyUSB5::INSTR",
    "params": {
        "scan_list": ["101", "102"]
    },
    "kwargs": {
        "baud_rate": 115200,
    }
}

ts_compound_inst = {
    "instance_name": "ts_log_hw",
    "subinstruments": [ls218, ls336, agilent_34970]
}

INSTRUMENT_SUITE = [agilent_34970, ls218, ls336, ts_compound_inst]

