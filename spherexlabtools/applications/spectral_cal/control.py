Mono_Controller = {
    "instance_name": "MonoCntrl",
    "type": "InstrumentController",
    "hw": "Monochromator",
    "control_parameters": [
        {"name": "osf", "type": "list", "limits": [1, 2, 3, 4, 5, 6, "Auto"]},
        {"name": "grating", "type": "list", "limits": [1, 2, 3, "Auto"]},
        {"name": "wavelength", "type": "float"},
        {"name": "shutter", "type": "list", "limits": ["O", "C"]},
    ],
    "status_parameters": [
        {"name": "osf", "type": "list", "limits": [1, 2, 3, 4, 5, 6]},
        {"name": "grating", "type": "list", "limits": [1, 2, 3]},
        {"name": "wavelength", "type": "float"},
        {"name": "shutter", "type": "list", "limits": ["O", "C"]},
    ],
    "status_refresh": "after_set",
}

CONTROLLERS = [Mono_Controller]
