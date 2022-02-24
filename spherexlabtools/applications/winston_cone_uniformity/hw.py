xstage_cfg = {
    "instance_name": "x",
    "resource_name": "ASRL3::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "LinearStageController",
    "kwargs": {
        "encoder_enabled": True,
        "homedir": "CCW",
        "address": 1
    },
    "params": {
        "units_per_turn": 1,
        "turns_per_step": 1/1600,
        "encoder_autocorrect": True,
        "encoder_retries": 5,
        "homespeed": 1500
    }
}

ystage_cfg = {
    "instance_name": "y",
    "resource_name": "ASRL3::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "LinearStageController",
    "kwargs": {
        "encoder_enabled": True,
        "homedir": "CCW",
        "address": 3
    },
    "params": {
        "units": "mm.",
        "units_per_turn": 1,
        "turns_per_step": 1 / 1600,
        "encoder_autocorrect": True,
        "encoder_retries": 5,
        "homespeed": 1500
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
