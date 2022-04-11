""" Controller configuration for thermal surrogate testing.
"""


def outmode_get_process(outmode_list):
    output_map = {
        0.0: "Off",
        1.0: "Closed Loop PID",
        2.0: "Zone",
        3.0: "Open Loop",
        4.0: "Monitor Out",
        5.0: "Warmup Supply"
    }
    input_map = {
        0.0: "None",
        1.0: "A",
        2.0: "B",
        3.0: "C",
        4.0: "D",
    }
    return [output_map[outmode_list[0]], input_map[outmode_list[1]], outmode_list[2]]


ls336_cntrl = {
    "instance_name": "Ls336Cntrl",
    "type": "InstrumentController",
    "hw": "ls336",
    "control_parameters": [
        {"name": "mout1", "type": "float"},
        {"name": "mout2", "type": "float"},
        {"name": "mout3", "type": "float"},
        {"name": "mout4", "type": "float"},
        {"name": "range1", "type": "list", "limits": ["off", "low", "medium", "high"]},
        {"name": "range2", "type": "list", "limits": ["off", "low", "medium", "high"]},
        {"name": "range3", "type": "list", "limits": ["off", "on"]},
        {"name": "range4", "type": "list", "limits": ["off", "on"]},
        {"name": "setpoint1", "type": "float"},
        {"name": "setpoint2", "type": "float"},
        {"name": "setpoint3", "type": "float"},
        {"name": "setpoint4", "type": "float"},
    ],
    "status_parameters": [
        {"name": "mout1", "type": "float"},
        {"name": "mout2", "type": "float"},
        {"name": "mout3", "type": "float"},
        {"name": "mout4", "type": "float"},
        {"name": "range1", "type": "list", "limits": ["off", "low", "medium", "high"]},
        {"name": "range2", "type": "list", "limits": ["off", "low", "medium", "high"]},
        {"name": "range3", "type": "list", "limits": ["off", "on"]},
        {"name": "range4", "type": "list", "limits": ["off", "on"]},
        {"name": "setpoint1", "type": "float"},
        {"name": "setpoint2", "type": "float"},
        {"name": "setpoint3", "type": "float"},
        {"name": "setpoint4", "type": "float"},
        {"name": "pid1", "type": "str"},
        {"name": "pid2", "type": "str"},
        {"name": "pid3", "type": "str"},
        {"name": "pid4", "type": "str"},
        {"name": "outmode1", "type": "str", "get_process": outmode_get_process},
        {"name": "outmode2", "type": "str", "get_process": outmode_get_process},
        {"name": "outmode3", "type": "str", "get_process": outmode_get_process},
        {"name": "outmode4", "type": "str", "get_process": outmode_get_process},
    ],
    "status_refresh": "manual",
    "actions": [
        {"name": "set_output_mode", "type": "action", "children": [
            {"name": "channel", "type": "list", "limits": [1, 2, 3, 4]},
            {"name": "mode", "type": "list", "limits": ["Off", "Closed Loop PID", "Open Loop", "Zone", "Monitor Out",
                                                        "Warmup Supply"]},
            {"name": "input_source", "type": "list", "limits": ["None", "A", "B", "C", "D"]}
        ]},
        {"name": "set_pid", "type": "action", "children": [
            {"name": "channel", "type": "list", "limits": [1, 2, 3, 4]},
            {"name": "p", "type": "float"},
            {"name": "i", "type": "float"},
            {"name": "d", "type": "float"},
        ]}
    ]
}


logproc_cntrl = {
    "instance_name": "LogProcCntrl",
    "type": "ProcedureController",
    "procedure": "DataLogProc",
    "kwargs": {
        "sequencer": False,
    }
}


ls336_aout_proc_cntrl = {
    "instance_name": "Ls336AoutProcCntrl",
    "type": "ProcedureController",
    "procedure": "Ls336AoutProc",
    "kwargs": {
        "sequencer": False
    }
}


CONTROLLERS = [ls336_cntrl, logproc_cntrl, ls336_aout_proc_cntrl]
