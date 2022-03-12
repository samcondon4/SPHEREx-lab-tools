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
    "status_refresh": "manual",
}

Ndf_Controller = {
    "instance_name": "NdfCntrl",
    "type": "InstrumentController",
    "hw": "NDFWheel",
    "control_parameters": [
        {"name": "position", "type": "list", "limits": [1, 2, 3, 4, 5, 6, 7, 8]}
    ],
    "status_parameters": [
        {"name": "position", "type": "list", "limits": [1, 2, 3, 4, 5, 6, 7, 8]}
    ],
    "status_refresh": "after_set",
    "actions": [
        "check_errors"
    ]
}

CONTROLLERS = [Mono_Controller, Ndf_Controller]
