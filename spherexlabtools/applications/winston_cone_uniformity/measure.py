# Viewer configs ######################
detector_viewer = {
    "instance_name": "PowerView",
    "type": "LineViewer",
    "kwargs": {
        "buf_size": 500
    },
    "params": {
        "labels": {
            "left": "Power (W.)",
            "bottom": "Sample"
        }
    }
}

# Recorder configs ####################
power_recorder = {
    "instance_name": "PowerMeanStdRecorder",
    "type": "HDF5Recorder",
    "filename": "winston_cone_uniformity.h5"
}

# Proc configs ########################
powerview_proc = {
    "instance_name": "PowerViewProc",
    "type": "LogProc",
    "hw": "detector",
    "records": {
        "power": {"viewer": "PowerView"}
    }
}

wcu_proc = {
    "instance_name": "WcuProc",
    "type": "WcuProc",
    "hw": ["detector", "stage"],
    "records": {
        "power": {"viewer": "PowerView"},
        "power_mean_std": {"recorder": "PowerMeanStdRecorder"}
    }
}

VIEWERS = [detector_viewer]
RECORDERS = [power_recorder]
PROCEDURES = [powerview_proc, wcu_proc]

