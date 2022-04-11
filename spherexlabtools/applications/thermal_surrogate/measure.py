# VIEWER CONFIG #########################################
temp_viewer = {
    "instance_name": "TempView",
    "type": "LineViewer",
    "params": {
        "labels": {
            "left": "Temperature (K.)",
            "bottom": "Sample"
        }
    }
}

ls336_analog_viewer = {
    "instance_name": "Ls336AoutView",
    "type": "LineViewer",
    "params": {
        "labels": {
            "left": "Voltage (V.)",
            "bottom": "Sample"
        }
    }
}


VIEWERS = [temp_viewer, ls336_analog_viewer]


# RECORDER CONFIG #########################################
pyhk_rec = {
    "instance_name": "PyhkRecorder",
    "type": "PyhkRecorder"
}

temp_rec_cfg = {
    "instance_name": "TempRecorder",
    "type": "CsvRecorder"
}


RECORDERS = [temp_rec_cfg, pyhk_rec]

# PROCEDURE CONFIG ########################################
log_proc = {
    "instance_name": "DataLogProc",
    "type": "DataLogProc",
    "hw": "ts_log_hw",
    "records": {
        "ls218_temperature1": {"viewer": "TempView", "recorder": "PyhkRecorder",
                               "alias": "TS_TEL_IF_SIM_2 T1", "type": "temperature"},
        "ls218_temperature2": {"viewer": "TempView", "recorder": "PyhkRecorder",
                               "alias": "TS_FPA_OUTER_RING T2", "type": "temperature"},
        "ls218_temperature3": {"viewer": "TempView", "recorder": "PyhkRecorder",
                               "alias": "TS_FPA_MID_RING T3", "type": "temperature"},
        "ls218_temperature4": {"viewer": "TempView", "recorder": "PyhkRecorder",
                               "alias": "TS_FPA_MID_RING T4", "type": "temperature"},
        "ls218_temperature5": {"viewer": "TempView", "recorder": "PyhkRecorder",
                               "alias": "TS_FPA_CABLE_IF T5", "type": "temperature"},
        "ls336_temperatureA": {"viewer": "TempView", "recorder": "PyhkRecorder",
                               "alias": "TS_TEL_IF_SIM_1 T1", "type": "temperature"},
        "ls336_temperatureB": {"viewer": "TempView", "recorder": "PyhkRecorder",
                               "alias": "TS_FPA_RAD_SIM T7", "type": "temperature"},
        "ls336_temperatureC": {"viewer": "TempView", "recorder": "PyhkRecorder",
                               "alias": "TS_FPA_MOSAIC_PLATE", "type": "temperature"},
        "ls336_mout1": {},
        "ls336_mout2": {},
        "ls336_mout3": {"viewer": "Ls336AoutView"},
        "aglnt_daq_dc_voltage": {},
        "csv_data": {"recorder": "TempRecorder", "subrecords": [
            "ls218_temperature1", "ls218_temperature2", "ls218_temperature3", "ls218_temperature4",
            "ls218_temperature5", "ls336_temperatureA", "ls336_temperatureB", "ls336_temperatureC",
            "ls336_mout1", "ls336_mout2", "ls336_mout3", "aglnt_daq_dc_voltage"
        ]}
    }
}


ls336_aout_proc = {
    "instance_name": "Ls336AoutProc",
    "type": "Ls336AoutProc",
    "hw": "ls336",
    "records": {}
}


PROCEDURES = [log_proc, ls336_aout_proc]
