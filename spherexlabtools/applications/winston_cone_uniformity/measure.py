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

# Proc configs ########################
powerview_proc = {
    "instance_name": "PowerViewProc",
    "type": "LogProc",
    "hw": "detector",
    "records": {
        "power": {"viewer": "PowerView"}
    }
}

VIEWERS = [detector_viewer]
RECORDERS = []
PROCEDURES = [powerview_proc]

