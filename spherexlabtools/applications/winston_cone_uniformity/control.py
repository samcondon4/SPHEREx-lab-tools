detector_stage_cntrl = {
    "instance_name": "StageController",
    "type": "InstrumentController",
    "hw": "stage",
    "control_parameters": [
        {"name": "x_maxspeed", "type": "int"},
        {"name": "y_maxspeed", "type": "int"},
        {"name": "x_step_position", "type": "int"},
        {"name": "y_step_position", "type": "int"},
        {"name": "x_absolute_position", "type": "int"},
        {"name": "y_absolute_position", "type": "int"},
    ],
    "status_parameters": [
        {"name": "x_maxspeed", "type": "int"},
        {"name": "y_maxspeed", "type": "int"},
        {"name": "x_step_position", "type": "int"},
        {"name": "y_step_position", "type": "int"},
        {"name": "x_absolute_position", "type": "int"},
        {"name": "y_absolute_position", "type": "int"},
    ],
    "status_refresh": 1
}

logproc_controller = {
    "instance_name": "PowerViewProcCntrl",
    "type": "LogProcController",
    "procedure": "PowerViewProc",
}

CONTROLLERS = [detector_stage_cntrl, logproc_controller]
