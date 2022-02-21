"""
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
    "status_refresh": 0.5
}
"""

Gimbal0_Controller = {
    "instance_name": "Gimbal0Cntrl",
    "type": "InstrumentController",
    "hw": "Gimbal0",
    "control_parameters": [
        {"name": "gimbal0_az_step_position", "type": "int"},
        {"name": "gimbal0_zth_step_position", "type": "int"}
    ],
    "status_parameters": [
        {"name": "gimbal0_az_step_position", "type": "int"},
        {"name": "gimbal0_zth_step_position", "type": "int"}
    ],
    "status_refresh": 1
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

CONTROLLERS = [Gimbal0_Controller]
