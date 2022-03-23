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
    "filename": "test.h5"
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
        "lockin_output_view": {"viewer": "LockinView"},
        "lockin_output_record": {"recorder": "SpecCalMetaRecorder"},
    }
}

PROCEDURES = [LockinViewProc, SpecCalProc]
