# Recorder configs ###############################
import numpy as np

CollimatorFocus_Recorder = {
    "instance_name": "CollimatorFocusRecorder",
    "type": "HDF5Recorder",
}

RECORDERS = [CollimatorFocus_Recorder]


# Viewer configs #################################
Camera_Viewer = {
    "instance_name": "CamView",
    "type": "ImageViewer",
    "kwargs": {
        "levels": [2**4, 2**16]
    }
}

CameraAvg_Viewer = {
    "instance_name": "CamViewAvg",
    "type": "ImageViewer",
    "kwargs": {
        "levels": [2**4, 2**16]
    }
}

VIEWERS = [Camera_Viewer, CameraAvg_Viewer]


def histogram_gen(record):
    """ Method used as an ancillary generator for a histogram of frame values on a log scale.
    """
    hist = np.histogram(record.data)
    ret_hist = (np.log10(hist[0]), hist[1])
    return {"histogram": ret_hist}


# Procedure configs ##############################
CameraView_Proc = {
    "instance_name": "CamViewProc",
    "type": "CamViewProc",
    "hw": "Camera",
    "records": {
        "latest_frame": {"viewer": "CamView", "ancillary_generator": histogram_gen},
    }
}

CollimatorFocus_Proc = {
    "instance_name": "CollimatorFocusProc",
    "type": "CollimatorFocusProc",
    "hw": ["Mscope", "Camera"],
    "records": {
        "frame": {"viewer": "CamView", "ancillary_generator": histogram_gen},
        "frame_avg": {"viewer": "CamViewAvg", "ancillary_generator": histogram_gen},
        "image": {"recorder": "CollimatorFocusRecorder"},
    }
}

PROCEDURES = [CameraView_Proc, CollimatorFocus_Proc]
