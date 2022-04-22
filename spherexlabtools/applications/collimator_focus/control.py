Camera_Controller = {
    "instance_name": "CameraCntrl",
    "type": "InstrumentController",
    "hw": "Camera",
    "control_parameters": [
        {"name": "gain", "type": "float"},
        {"name": "acquisition_frame_rate_en", "type": "bool"},
        {"name": "acquisition_frame_rate_auto", "type": "list", "limits": [
            "Off", "Continuous"]},
        {"name": "acquisition_frame_rate", "type": "float"},
        {"name": "exposure_mode", "type": "list", "limits": [
            "Timed", "TriggerWidth"]},
        {"name": "exposure_auto", "type": "list", "limits": [
            "Off", "Once", "Continuous"]},
        {"name": "exposure_time", "type": "float"},
        {"name": "pixel_format", "type": "list", "limits": [
            "Mono8", "Mono16", "Mono12Packed"]}
    ],
    "status_parameters": [
        {"name": "gain", "type": "float"},
        {"name": "acquisition_frame_rate_en", "type": "bool"},
        {"name": "acquisition_frame_rate_auto", "type": "list", "limits": [
            "Off", "Continuous"]},
        {"name": "acquisition_frame_rate", "type": "float"},
        {"name": "exposure_mode", "type": "list", "limits": [
            "Timed", "TriggerWidth"]},
        {"name": "exposure_auto", "type": "list", "limits": [
            "Off", "Once", "Continuous"]},
        {"name": "exposure_time", "type": "float"},
        {"name": "pixel_format", "type": "list", "limits": [
            "Mono8", "Mono16", "Mono12Packed"]}
    ],
    "status_refresh": "manual"
}

MScope_Controller = {
    "instance_name": "MicroscopeMotorCntrl",
    "type": "InstrumentController",
    "hw": "MscopeMotors",
    "control_parameters": [
        {"name": "focuser_step_position", "type": "int"},
        {"name": "focuser_absolute_position", "type": "float"},
    ],
    "status_parameters": [
        {"name": "focuser_step_position", "type": "int"},
        {"name": "gauge_position", "type": "float"},
    ],
    "status_refresh": "manual",
    "actions": [
        "focuser_stop", "focuser_reset_position"
    ]
}

Gimbal0_Controller = {
    "instance_name": "RelayMotorCntrl",
    "type": "InstrumentController",
    "hw": "Gimbal0",
    "control_parameters": [
        {"name": "az_absolute_position", "type": "float"},
        {"name": "za_absolute_position", "type": "float"},
    ],
    "status_parameters": [
        {"name": "az_absolute_position", "type": "float"},
        {"name": "za_absolute_position", "type": "float"},
    ],
    "status_refresh": "manual",
    "actions": [
        "az_stop", "za_stop", "az_home", "za_home", "az_reset_position", "za_reset_position"
    ]
}

LogProc_Controller = {
    "instance_name": "CamViewProcCntrl",
    "type": "ProcedureController",
    "procedure": "CamViewProc",
    "kwargs": {
        "sequencer": False
    }
}

CollimatorFocus_Controller = {
    "instance_name": "CollimatorFocusProcCntrl",
    "type": "ProcedureController",
    "procedure": "CollimatorFocusProc"
}

CONTROLLERS = [Camera_Controller, MScope_Controller, Gimbal0_Controller, LogProc_Controller, 
               CollimatorFocus_Controller]
