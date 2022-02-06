# Recorder configs ###############################
CollimatorFocus_Recorder = {
    "instance_name": "CollimatorFocusRecorder",
    "type": "hdf5"
}

RECORDERS = [CollimatorFocus_Recorder]


# Viewer configs #################################
Camera_Viewer = {
    "instance_name": "CamView",
    "type": "ImageViewer"
}

VIEWERS = [Camera_Viewer]


# Procedure configs ##############################
CameraView_Proc = {
    "instance_name": "CamProc",
    "type": "CamViewProc",
    "hw": "Microscope",
    "records": {
        "cam_latest_frame": {"viewer": "CamView"}
    }
}

PROCEDURES = [CameraView_Proc]
