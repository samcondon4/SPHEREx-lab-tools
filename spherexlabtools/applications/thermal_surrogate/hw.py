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
    "resource_name": "ASRL/dev/ttyUSB3::INSTR",
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
    "resource_name": "ASRL/dev/ttyUSB1::INSTR"
}


INSTRUMENT_SUITE = [ls218, ls336]

