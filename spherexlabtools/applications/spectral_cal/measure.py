"""
Procedures
-----------

    - "LockinViewProc": Logging procedure to retrieve output voltages from the sr510 and sr830 lockin amplifiers.
    - "SpecCalProc": Procedure to run monochromator scans, log lockin reference detector data, and trigger detector
                     exposures.

Viewers
-------

    - "LockinView": LineViewer to view live data recorded from the lock-in amplifiers.

Recorders
---------

    - "SpecCalMetaRecorder": CsvRecorder to log all spectral calibration warm optics instrumentation metadata.

"""

lockin_viewer = {
    "instance_name": "LockinView",
    "type": "LineViewer",
    "params": {
        "labels": {
            "left": "Output Voltage (V.)",
            "bottom": "Sample"
        }
    }
}

VIEWERS = [lockin_viewer]


LockinLog_Recorder = {
    "instance_name": "LockinLog",
    "type": "PyhkRecorder"
}


SpecCalMeta_Recorder = {
    "instance_name": "SpecCalMetaRecorder",
    "type": "CsvRecorder",
}

SpecCalSql_Recorder = {
    "instance_name": "SQLRecorder",
    "type": "SQLRecorder",
    "params": {
        "table": "spectral_cal"
    }
}


RECORDERS = [SpecCalMeta_Recorder, SpecCalSql_Recorder]


LockinViewProc = {
    "instance_name": "LockinViewProc",
    "type": "LogProc",
    "hw": "lockin",
    "records": {
        "sr510_output": {"viewer": "LockinView"},
        "sr830_x": {"viewer": "LockinView"},
        "sr830_y": {"viewer": "LockinView"}
    }
}


SpecCalProc = {
    "instance_name": "SpecCalProc",
    "type": "SpecCalProc",
    "hw": ["mono", "ndf", "lockin", "readout"],
    "records": {
        "spec_cal_csv": {"recorder": "SpecCalMetaRecorder"},
        "spec_cal_sql": {"recorder": "SQLRecorder"},
    }
}

PROCEDURES = [LockinViewProc, SpecCalProc]
