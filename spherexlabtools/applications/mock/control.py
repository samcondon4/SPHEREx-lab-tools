HeaterCntrl = {
    "instance_name": "HeaterCntrl",
    "type": "InstrumentController",
    "hw": "Heater",
    "control_parameters": [
        {"name": "output_voltage", "type": "str"}
    ]
}

CamCntrl = {
    "instance_name": "CameraCntrl",
    "type": "InstrumentController",
    "hw": "Camera",
    "control_parameters": [
        {"name": "frame_width", "type": "int", "value": "2448"},
        {"name": "frame_height", "type": "int", "value": "2048"},
        {"name": "frame_format", "type": "list", "limits": ["mono_8", "mono_16"]}
    ],
    "status_parameters": [
        {"name": "frame_width", "type": "str"},
        {"name": "frame_height", "type": "str"},
        {"name": "frame_format", "type": "list", "limits": ["mono_8", "mono_16"]}
    ],
    "status_refresh": "after_set"
}

CamViewProcCntrl = {
    "instance_name": "CamViewProcCntrl",
    "type": "ProcedureController",
    "procedure": "CamViewProc",
    "kwargs": {
        "sequencer": False
    }
}

TestProcCtnrl = {
    "instance_name": "TestProcCntrl",
    "type": "ProcedureController",
    "procedure": "TestProc",
}

CONTROLLERS = [HeaterCntrl, CamCntrl, CamViewProcCntrl, TestProcCtnrl]
