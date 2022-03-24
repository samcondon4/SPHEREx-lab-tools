lockin_viewer = {
    "instance_name": "LockinView",
    "type": "LineViewer",
    "params": {
        "labels": {
            "left": "Output Voltage (V.)",
            "bottom": "Sample"
        }
    }
}

VIEWERS = [lockin_viewer]


SpecCalMeta_Recorder = {
    "instance_name": "SpecCalMetaRecorder",
    "type": "HDF5Recorder",
    "filename": "spec_cal.h5"
}


RECORDERS = [SpecCalMeta_Recorder]


LockinViewProc = {
    "instance_name": "LockinViewProc",
    "type": "LogProc",
    "hw": "lockin",
    "records": {
        "sr510_output": {"viewer": "LockinView"},
        "sr830_x": {"viewer": "LockinView"},
        "sr830_y": {"viewer": "LockinView"}
    }
}


SpecCalProc = {
    "instance_name": "SpecCalProc",
    "type": "SpecCalProc",
    "hw": ["mono", "ndf", "lockin"],
    "records": {
        "sr830_x": {"viewer": "LockinView"},
        "sr830_y": {"viewer": "LockinView"},
        "sr510_output": {"viewer": "LockinView"},
        "lockin_output": {"recorder": "SpecCalMetaRecorder"}
    }
}

PROCEDURES = [LockinViewProc, SpecCalProc]
