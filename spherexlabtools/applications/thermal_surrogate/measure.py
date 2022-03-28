# VIEWER CONFIG #########################################
ls218_viewer = {
    "instance_name": "Ls218View",
    "type": "LineViewer",
    "params": {
        "labels": {
            "left": "Temperature (K.)",
            "bottom": "Sample"
        }
    }
}

ls336_analog_viewer = {
    "instance_name": "Ls336AnalogView",
    "type": "LineViewer",
    "params": {
        "labels": {
            "left": "Voltage (V.)",
            "bottom": "Sample"
        }
    }
}


VIEWERS = [ls218_viewer, ls336_analog_viewer]


# RECORDER CONFIG #########################################
temp_rec_cfg = {
    "instance_name": "TempRecorder",
    "type": "CsvRecorder"
}


RECORDERS = [temp_rec_cfg]

# PROCEDURE CONFIG ########################################
ls218_temp_proc = {
    "instance_name": "Ls218TempProc",
    "type": "Ls218TempProc",
    "hw": "ls218",
    "records": {
        "temperature1": {"viewer": "Ls218View"},
        "temperature2": {"viewer": "Ls218View"},
        #"temperature3": {"viewer": "Ls218View"},
        #"temperature4": {"viewer": "Ls218View"},
        "temp_to_csv": {"recorder": "TempRecorder"}
    }
}


ls336_aout_proc = {
    "instance_name": "Ls336AoutProc",
    "type": "Ls336AoutProc",
    "hw": "ls336",
    "records": {
        "analog_out": {"viewer": "Ls336AnalogView"},
    }
}


PROCEDURES = [ls218_temp_proc, ls336_aout_proc]
