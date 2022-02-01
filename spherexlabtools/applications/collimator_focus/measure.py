# Recorder configs ###############################
CollimatorFocus_Recorder = {
    "instance_name": "CollimatorFocusRecorder",
    "type": "hdf5"
}

RECORDERS = [CollimatorFocus_Recorder]


# Viewer configs #################################
Camera_Viewer = {
    "instance_name": "CameraViewer",
    "type": "ImageViewer"
}

VIEWERS = [Camera_Viewer]


# Procedure configs ##############################
CameraView_Proc = {
    "instance_name": "CameraView",
    "type": "LogProc",
    "hw": "Microscope",
    "viewer": "CameraViewer",
    "props": ["cam_latest_frame"]
}

PROCEDURES = [CameraView_Proc]
