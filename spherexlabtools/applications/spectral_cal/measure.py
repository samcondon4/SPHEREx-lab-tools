lockin_viewer = {
    "instance_name": "LockinView",
    "type": "LineViewer",
    "kwargs": {
        "buf_size": 500
    },
    "params": {
        "labels": {
            "left": "Output Voltage (V.)",
            "bottom": "Sample"
        }
    }
}

VIEWERS = [lockin_viewer]
