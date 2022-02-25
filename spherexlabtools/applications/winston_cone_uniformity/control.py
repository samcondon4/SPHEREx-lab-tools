detector_stage_cntrl = {
    "instance_name": "StageController",
    "type": "InstrumentController",
    "hw": "stage",
    "control_parameters": [
        {"name": "x_maxspeed", "type": "int"},
        {"name": "y_maxspeed", "type": "int"},
        {"name": "x_absolute_position", "type": "float"},
        {"name": "y_absolute_position", "type": "float"},
    ],
    "status_parameters": [
        {"name": "x_absolute_position", "type": "float"},
        {"name": "y_absolute_position", "type": "float"},
    ],
    "status_refresh": 3,
    "actions": ["x_home", "y_home", "x_stop", "y_stop", "x_reset_position", "y_reset_position", "x_check_errors",
                "y_check_errors"]
}

logproc_controller = {
    "instance_name": "PowerViewProcCntrl",
    "type": "LogProcController",
    "procedure": "PowerViewProc",
}

wcuproc_controller = {
    "instance_name": "WcuProcCntrl",
    "type": "ProcedureController",
    "procedure": "WcuProc"
}

CONTROLLERS = [detector_stage_cntrl, logproc_controller, wcuproc_controller]
