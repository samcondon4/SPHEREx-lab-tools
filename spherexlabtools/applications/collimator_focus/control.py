MScope_Controller = {
    "instance_name": "MicroscopeCntrl",
    "type": "InstrumentController",
    "hw": "Microscope",
    "control_parameters": [
        {"name": "focuser_step_position", "type": "int"},
        {"name": "focuser_absolute_position", "type": "float"},
        {"name": "cam_gain_auto", "type": "list", "values": ["Off", "Once", "Continuous"]},
        {"name": "cam_gain", "type": "float"}
    ],
    "status_parameters": [
        {"name": "focuser_step_position", "type": "int"},
        {"name": "gauge_position", "type": "float"},
        {"name": "focuser_absolute_position", "type": "float"},
        {"name": "cam_gain", "type": "float"}
    ],
    "status_refresh": 2,
    "actions": [
        "focuser_stop", "focuser_reset_position"
    ]
}

Gimbal0_Controller = {
    "instance_name": "Gimbal0Cntrl",
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
    "status_refresh": 2,
    "actions": [
        "az_stop", "za_stop", "az_home", "za_home", "az_reset_position", "za_reset_position"
    ]
}

LogProc_Controller = {
    "instance_name": "CamViewProcCntrl",
    "type": "LogProcController",
    "procedure": "CamViewProc",
}

CollimatorFocus_Controller = {
    "instance_name": "CollimatorFocusProcCntrl",
    "type": "ProcedureController",
    "procedure": "CollimatorFocusProc"
}

CONTROLLERS = [MScope_Controller, Gimbal0_Controller, LogProc_Controller, CollimatorFocus_Controller]
