Mono_Controller = {
    "instance_name": "MonoCntrl",
    "type": "InstrumentController",
    "hw": "Monochromator",
    "control_parameters": [
        {"name": "wavelength", "type": "float"},
        {"name": "grating", "type": "list", "limits": [1, 2, 3]},
        {"name": "osf", "type": "list", "limits": [1, 2, 3, 4, 5, 6]},
        {"name": "shutter", "type": "list", "limits": ["O", "C"]},
    ],
    "status_parameters": [
        {"name": "wavelength", "type": "float"},
        {"name": "grating", "type": "list", "limits": [1, 2, 3]},
        {"name": "osf", "type": "list", "limits": [1, 2, 3, 4, 5, 6]},
        {"name": "shutter", "type": "list", "limits": ["O", "C"]},
    ],
    "status_refresh": 3,
}

