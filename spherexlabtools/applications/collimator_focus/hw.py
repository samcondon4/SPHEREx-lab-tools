from spherexlabtools.instruments.flir import Flea3 as _Fl3

CamCfg = {
    "instance_name": "cam",
    "resource_name": _Fl3.cam_list[0],
    "manufacturer": "flir",
    "instrument": "Flea3",
    "params": {
        "gain_auto": "Off",
        "gain": 0,
        "blacklevel_en": False,
        "gamma_en": False,
        "sharpess_en": False,
        "acquisition_frame_rate_auto": "Off",
        "acquisition_frame_rate_en": True,
        "acquisition_frame_rate": 8,
        "exposure_width": 2448,
        "exposure_height": 2048,
    }
}

GaugeCfg = {
    "instance_name": "gauge",
    "resource_name": "ASRL/dev/ttyUSB0::INSTR",
    "manufacturer": "heidenhain",
    "instrument": "ND287",
    "params": {
        "units": "inch",
    },
    "kwargs": {
        "baud_rate": 115200
    }
}

FocuserCfg = {
    "instance_name": "focuser",
    "resource_name": "ASRL/dev/ttyUSB1::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "LinearStageController",
    "kwargs": {
        "log_id": "mscope_focus",
        "homedir": "CCW",
        "address": 3,
    }
}

MscopeCfg = {
    "instance_name": "Microscope",
    "subinstruments": [CamCfg, GaugeCfg, FocuserCfg]
}

INSTRUMENT_SUITE = [MscopeCfg]
