LockinRecord = {
    "instance_name": "LockinRecord",
    "type": "CsvRecorder"
}

RECORDERS = [LockinRecord]


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
        "lockin_output": {"recorder": "LockinRecord"}
    }
}

PROCEDURES = [CamViewProc, TestProc]
