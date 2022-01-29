
MScope_Controller = {
    "type": "instrument::mscope",
    "control_parameters": [
        {"name": "focuser_step_position", "type": "int"}
    ],
    "status_parameters": [
        {"name": "gauge_position", "type": "float"}
    ]
}

CONTROLLERS = [MScope_Controller]
