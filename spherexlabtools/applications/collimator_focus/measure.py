# Recorder configs ###############################
CollimatorFocus_Recorder = {
    "instance_name": "CollimatorFocusRecorder",
    "type": "HDF5Recorder",
    "filename": "test.h5",
}

RECORDERS = [CollimatorFocus_Recorder]


# Viewer configs #################################
Camera_Viewer = {
    "instance_name": "CamView",
    "type": "ImageViewer",
    "kwargs": {
        "levels": [0, 255]
    }
}

CameraAvg_Viewer = {
    "instance_name": "CamViewAvg",
    "type": "ImageViewer"
}

VIEWERS = [Camera_Viewer, CameraAvg_Viewer]


# Procedure configs ##############################
CameraView_Proc = {
    "instance_name": "CamViewProc",
    "type": "CamViewProc",
    "hw": "Microscope",
    "records": {
        "cam_latest_frame": {"viewer": "CamView"},
    },
    "params": {
        "frames_per_image": 100
    }
}

CollimatorFocus_Proc = {
    "instance_name": "CollimatorFocusProc",
    "type": "CollimatorFocusProc",
    "hw": "Microscope",
    "records": {
        "frame": {"viewer": "CamView"},
        "frame_avg": {"viewer": "CamViewAvg"},
        "image": {"recorder": "CollimatorFocusRecorder"}
    }
}

PROCEDURES = [CameraView_Proc, CollimatorFocus_Proc]
