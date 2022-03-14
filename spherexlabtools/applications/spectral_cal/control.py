# INSTRUMENT CONTROLLERS #######################################################################################
Mono_Controller = {
    "instance_name": "MonoCntrl",
    "type": "InstrumentController",
    "hw": "mono",
    "control_parameters": [
        {"name": "osf", "type": "list", "limits": [1, 2, 3, 4, 5, 6, "Auto"]},
        {"name": "grating", "type": "list", "limits": [1, 2, 3, "Auto"]},
        {"name": "wavelength", "type": "float"},
        {"name": "shutter", "type": "list", "limits": [0, 1],
         "set_process": lambda param: {0: "C", 1: "O"}[param.value()]},
    ],
    "status_parameters": [
        {"name": "osf", "type": "list", "limits": [1, 2, 3, 4, 5, 6]},
        {"name": "grating", "type": "list", "limits": [1, 2, 3]},
        {"name": "wavelength", "type": "float"},
        {"name": "shutter", "type": "list", "limits": [0, 1]},
    ],
    "status_refresh": "manual",
}

Ndf_Controller = {
    "instance_name": "NdfCntrl",
    "type": "InstrumentController",
    "hw": "ndf",
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

sens_units_map = {
    "nV.": 1e-9,
    "uW.": 1e-6,
    "mV.": 1e-3,
    "V.": 1
}

tc_units_map = {
    "uS.": 1e-6,
    "mS.": 1e-3,
    "S.": 1,
    "kS.": 1e3
}

sensitivity_children = [
    {"name": "Value", "type": "list", "limits": [1, 2, 5]},
    {"name": "Multiplier", "type": "list", "limits": [1, 1e1, 1e2]},
    {"name": "Units", "type": "list", "limits": ["nV.", "uV.", "mV.", "V."]}
]

timeconstant_children = [
    {"name": "Value", "type": "list", "limits": [1, 3]},
    {"name": "Multiplier", "type": "list", "limits": [1, 1e1, 1e2]},
    {"name": "Units", "type": "list", "limits": ["uS.", "mS.", "S.", "kS."]}
]


def tc_sens_setting(parameter, units_mapping):
    children = {p.name(): p.value() for p in parameter.children()}
    val = children["Value"]
    mult = children["Multiplier"]
    units = units_mapping[children["Units"]]

    return val * mult * units


Lockin_Controller = {
    "instance_name": "LockinCntrl",
    "type": "InstrumentController",
    "hw": "lockin",
    "control_parameters": [
        {"name": "sr510_sensitivity", "type": "group", "children": sensitivity_children,
         "set_process": lambda param, units_mapping=sens_units_map: tc_sens_setting(param, units_mapping)},

        {"name": "sr510_time_constant", "type": "group", "children": timeconstant_children,
         "set_process": lambda param, units_mapping=tc_units_map: tc_sens_setting(param, units_mapping)},

        {"name": "sr830_sensitivity", "type": "group", "children": sensitivity_children,
         "set_process": lambda param, units_mapping=sens_units_map: tc_sens_setting(param, units_mapping)},

        {"name": "sr830_time_constant", "type": "group", "children": timeconstant_children,
         "set_process": lambda param, units_mapping=tc_units_map: tc_sens_setting(param, units_mapping)},
    ],
    "status_parameters": [
        {"name": "sr510_sensitivity", "type": "float"},
        {"name": "sr510_time_constant", "type": "float"},
        {"name": "sr830_sensitivity", "type": "float"},
        {"name": "sr830_time_constant", "type": "float"},
    ],
    "status_refresh": "after_set"
}
##############################################################################################################

# PROCEDURE CONTROLLERS ######################################################################################
SpecCalProc_Controller = {
    "instance_name": "SpecCalProcCntrl",
    "type": "ProcedureController",
    "procedure": "SpecCalProc"
}
##############################################################################################################

CONTROLLERS = [Mono_Controller, Ndf_Controller, Lockin_Controller, SpecCalProc_Controller]
