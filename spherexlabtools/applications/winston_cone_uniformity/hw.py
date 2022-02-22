xstage_cfg = {
    "instance_name": "x",
    "resource_name": "ASRL3::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "LinearStageController",
    "kwargs": {
        "homedir": "CCW",
        "address": 1
    }
}

ystage_cfg = {
    "instance_name": "y",
    "resource_name": "ASRL3::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "LinearStageController",
    "kwargs": {
        "homedir": "CCW",
        "address": 0
    }
}

detector_stage = {
    "instance_name": "stage",
    "subinstruments": [xstage_cfg, ystage_cfg]
}

detector_cfg = {
    "instance_name": "detector",
    "resource_name": "USB0::0x1313::0x8072::1912813 ::INSTR",
    "manufacturer": "thorlabs",
    "instrument": "ThorlabsPM100USB"
}

INSTRUMENT_SUITE = [detector_stage, detector_cfg]
