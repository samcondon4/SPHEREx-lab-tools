MScope_Controller = {
    "type": "instrument::mscope",
    "control_parameters": [
        {"name": "focuser_step_position", "type": "int"},
        {"name": "cam_gain_auto", "type": "list", "values": ["Off", "Once", "Continuous"]}
    ],
    "status_parameters": [
        {"name": "gauge_position", "type": "float"},
        {"name": "cam_gain", "type": "float"}
    ],
    "status_refresh": 0.5
}

CONTROLLERS = [MScope_Controller]
