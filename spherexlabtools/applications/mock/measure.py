LockinRecord = {
    "instance_name": "LockinRecorder",
    "type": "CsvRecorder"
}

ImRecord = {
    "instance_name": "ImRecorder",
    "type": "HDF5Recorder"
}

RECORDERS = [LockinRecord, ImRecord]


CamView = {
    "instance_name": "CamView",
    "type": "ImageViewer",
    "kwargs": {
        "levels": [0, 2**16]
    }
}

VIEWERS = [CamView]


CamViewProc = {
    "instance_name": "CamViewProc",
    "type": "LogProc",
    "hw": "Camera",
    "records": {
        "frame": {"viewer": "CamView"}
    }
}

TestProc = {
    "instance_name": "TestProc",
    "type": "TestProc",
    "hw": ["Camera", "Heater", "LockinAmp"],
    "records": {
        "lockin_output": {"recorder": "LockinRecorder"},
        "image": {"recorder": "ImRecorder", "viewer": "CamView"}
    }
}

PROCEDURES = [CamViewProc, TestProc]
