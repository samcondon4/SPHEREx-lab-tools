MScope_Controller = {
    "instance_name": "MicroscopeCntrl",
    "type": "InstrumentController",
    "hw": "Microscope",
    "control_parameters": [
        {"name": "focuser_step_position", "type": "int"},
        {"name": "cam_gain_auto", "type": "list", "values": ["Off", "Once", "Continuous"]},
        {"name": "cam_gain", "type": "float"}
    ],
    "status_parameters": [
        {"name": "gauge_position", "type": "float"},
        {"name": "cam_gain", "type": "float"}
    ],
    "status_refresh": 2
}

Gimbal0_Controller = {
    "instance_name": "Gimbal0Cntrl",
    "type": "InstrumentController",
    "hw": "Gimbal0",
    "control_parameters": [
        {"name": "az_absolute_position", "type": "float"},
        {"name": "zth_absolute_position", "type": "float"},
    ],
    "status_parameters": [
        {"name": "az_absolute_position", "type": "float"},
        {"name": "zth_absolute_position", "type": "float"},
    ],
    "status_refresh": 2,
    "actions": [
        "az_stop", "zth_stop", "az_home", "zth_home", "az_reset_position", "zth_reset_position"
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
