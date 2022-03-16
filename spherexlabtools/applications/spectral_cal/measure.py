lockin_viewer = {
    "instance_name": "LockinView",
    "type": "LineViewer",
    "kwargs": {
        "buf_size": 500,
    },
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


SpecCalProc = {
    "instance_name": "SpecCalProc",
    "type": "SpecCalProc",
    "hw": ["mono", "ndf", "lockin"],
    "records": {
        "lockin_output_view": {"viewer": "LockinView"},
        "lockin_output_record": {"recorder": "SpecCalMetaRecorder"},
        "sequence": {"recorder": "SpecCalMetaRecorder"}
    }
}

PROCEDURES = [SpecCalProc]
