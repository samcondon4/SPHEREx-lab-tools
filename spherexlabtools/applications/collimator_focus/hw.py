from spherexlabtools.instruments.flir import Flea3 as _Fl3

# MICROSCOPE ##############################################################
CamCfg = {
    "instance_name": "Camera",
    "resource_name": _Fl3.cam_list[0],
    "manufacturer": "flir",
    "instrument": "Flea3",
    "params": {
        "gain_auto": "Off",
        "gain": 0,
        "blacklevel_en": False,
        "gamma_en": False,
        "sharpess_en": False,
        "acquisition_frame_rate_en": False,
        "exposure_width": 2448,
        "exposure_height": 2048,
        "exposure_mode": "Timed",
        "exposure_auto": "Off"
    }
}


GaugeCfg = {
    "instance_name": "gauge",
    "resource_name": "ASRL/dev/ttyUSB2::INSTR",
    "manufacturer": "heidenhain",
    "instrument": "ND287",
    "params": {
        "units": "mm",
    },
    "kwargs": {
        "baud_rate": 115200
    }
}

FocuserCfg = {
    "instance_name": "focuser",
    "resource_name": "ASRL/dev/ttyUSB3::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "FocuserDrive",
    "kwargs": {
        "address": 0,
        "homedir": "CCW",
        "encoder_enabled": False,
    },
    "params": {
        "turns_per_step": 1 / 3600,
        "units_per_turn": 1.87,
        "units": "mm",
    }
}

ShutterCfg = {
    "instance_name": "shutter",
    "resource_name": "ASRL/dev/ttyUSB1::INSTR",
    "manufacturer": "spherex",
    "instrument": "CSLD",
    "kwargs": {
        "baud_rate": 115200,
        "write_termination": "\r"
    }
}

MscopeCfg = {
    "instance_name": "Mscope",
    "subinstruments": [GaugeCfg, FocuserCfg, ShutterCfg],
    "property_config": [
        ("focuser_absolute_position", "gauge_position", "focuser_absolute_position")
    ]
}
##################################################################

# RELAY ##########################################################
# relay gimbal0 az config
relay_gimbal0_az = {
    "instance_name": "az",
    "resource_name": "ASRL/dev/ttyUSB4::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "LinearStageController",
    "kwargs": {
        "address": 1,
        "homedir": "CCW",
        "encoder_enabled": True,
    },
    "params": {
        "turns_per_step": 1/200,
        "units_per_turn": 0.625,
        "units": "degrees",
        "encoder_motor_ratio": 2.5,
    }
}
# relay gimbal1 zth config
relay_gimbal0_zth = {
    "instance_name": "za",
    "resource_name": "ASRL/dev/ttyUSB4::INSTR",
    "manufacturer": "anaheimautomation",
    "instrument": "LinearStageController",
    "kwargs": {
        "address": 3,
        "homedir": "CCW",
        "encoder_enabled": False,
    },
    "params": {
        "turns_per_step": 1 / 200,
        "units_per_turn": 0.625,
        "units": "degrees",
        "encoder_motor_ratio": 2.5,
    }
}

Gimbal0 = {
    "instance_name": "Gimbal0",
    "subinstruments": [relay_gimbal0_az, relay_gimbal0_zth]
}
##################################################################

# Instrument suite list for the experiment object ################
INSTRUMENT_SUITE = [MscopeCfg, CamCfg, Gimbal0, FocuserCfg]


