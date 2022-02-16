MScope_Controller = {
    "instance_name": "Microscope Control",
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
    "status_refresh": 0.5
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

CONTROLLERS = [MScope_Controller, LogProc_Controller, CollimatorFocus_Controller]
