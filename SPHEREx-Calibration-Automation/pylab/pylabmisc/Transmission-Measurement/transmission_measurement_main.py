##Transmission measurement main####################
'''
This file extends the main GUI with an additional tab containing two buttons
used to control the LabJack readout of the detector during the transmission
measurement effort.

'''
import asyncio
import u6
import pandas as pd
import time
from PyQt5.QtWidgets import *
from transmission_ui import *


TAB_NAME = "LabJack Power Measure"
SINGLE_MEASURE_PATH = 'data\\singles.csv'
DETECTOR_PORT = 'AIN0'


class LabJackU6:

    def __init__(self):
        # Initialize LabJack U6
        self.u6 = u6.U6()
        self.u6.getCalibrationData()
        self.u6.streamConfig(NumChannels=2, ChannelNumbers=[0, 1], ChannelOptions=[0, 0],
                             SettlingFactor=1, ResolutionIndex=1, ScanFrequency=5e3)

    async def stream(self, measure_interval=5.0, avg=True):
        detector_data = []
        start_time = time.perf_counter()
        self.u6.streamStart()
        for measure in self.u6.streamData():
            # stop condition
            if time.perf_counter() >= (start_time + measure_interval):
                break

            if measure is not None and measure['errors'] == 0:
                d = measure[DETECTOR_PORT]
                if avg:
                    detector_data.append(sum(d) / len(d))
                else:
                    detector_data.append(d)

            await asyncio.sleep(0.001)  # short pend to allow other things to run

        self.u6.streamStop()
        return detector_data


async def lj_scan_measure_task(sync_queue):
    pass


def add_transmission_measure(scan_series_task, single_task, sync_queue):
    pass


def add_transmission_tab(tabWidget):
    transmission_tab = QWidget()
    transmission_tab.setObjectName(TAB_NAME)
    gridLayout = QtWidgets.QGridLayout(transmission_tab)
    gridLayout.setObjectName("gridLayout")
    verticalLayout = QtWidgets.QVBoxLayout()
    verticalLayout.setObjectName("verticalLayout")
    power_measure_scan_series = QtWidgets.QPushButton(transmission_tab)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(power_measure_scan_series.sizePolicy().hasHeightForWidth())
    power_measure_scan_series.setSizePolicy(sizePolicy)
    power_measure_scan_series.setObjectName("power_measure_scan_series")
    verticalLayout.addWidget(power_measure_scan_series)
    power_measure_single = QtWidgets.QPushButton(transmission_tab)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(power_measure_single.sizePolicy().hasHeightForWidth())
    power_measure_single.setSizePolicy(sizePolicy)
    power_measure_single.setObjectName("power_measure_single")
    verticalLayout.addWidget(power_measure_single)
    gridLayout.addLayout(verticalLayout, 0, 0, 1, 1)
    power_measure_scan_series.setText("Run Power Measurements over Scan Series")
    power_measure_single.setText("Run Single Power Measurement")
    tabWidget.addTab(transmission_tab, TAB_NAME)


async def labjack_measure_task(sync_queue):
    # Initialize LabJack U6
    lju6 = u6.U6()
    lju6.getCalibrationData()
    lju6.streamConfig(NumChannels=2, ChannelNumbers=[0, 1], ChannelOptions=[0, 0],
                      SettlingFactor=1, ResolutionIndex=1, ScanFrequency=5e3)

    data = {'Sequence': [], 'Grating': [], 'Wavelength': [], 'Filter': [],
            'Shutter': [], 'Integration Time': [], 'Detector Voltage': []}



    # Task run loop
    while True:
        # pend on sync_event set by cs scan task
        message = asyncio.create_task(sync_queue.get())
        await message
        message = message.result()
        # if message received from queue is a .csv file name, then write out a csv and prepare dictionary for new scan series
        if type(message) is str and message == "done":
            df = pd.DataFrame(data)
            df.to_csv(message['Sequence'], index=False)
            data = {'Grating': [], 'Wavelength': [], 'Detector Voltage': []}

        elif type(message) is dict and message['Sequence'] == '_manual-measurement_':
            df = pd.read_csv(SINGLE_MEASURE_PATH)

        # otherwise, run LabJack measurement over the measure interval received through message
        else:
            # copy data from message, this is just for readability
            measure_interval = message
            # record current monochromator state
            data['Grating'].append(message['Grating'])
            data['Wavelength'].append(message['Wavelength'])
            # start taking data on Labjack
            detector_data = []
            start_time = time.perf_counter()
            lju6.streamStart()
            for measure in lju6.streamData():
                # stop condition
                if time.perf_counter() >= (start_time + measure_interval):
                    break

                if measure is not None and measure['errors'] == 0:
                    d = measure[DETECTOR_PORT]
                    detector_data.append(sum(d) / len(d))

                await asyncio.sleep(0.001)  # short pend to allow other things to run
            # End labjack stream and add average detector voltage to dictionary
            lju6.streamStop()
            data['Detector Voltage'].append(sum(detector_data) / len(detector_data))
            # acknowledge that data has been read and recorded for the specified measurement interval
            sync_queue.put_nowait("ack")
