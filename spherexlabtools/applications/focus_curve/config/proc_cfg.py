import os

# FocusCurveProc initial configuration #
ProcCfg = {
    "focus_position": 0,
    "frames_per_image": 100,
    "images": 1,
    "output_directory": os.path.join(os.environ["SLT_DATA"], "focus_curve"),
    "filename": "focus_curve_0",
}


