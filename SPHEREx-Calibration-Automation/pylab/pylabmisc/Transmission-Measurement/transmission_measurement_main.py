import sys
import asyncio
import qasync
import u6
import time
import pandas as pd

sys.path.append('..\\..\\pylabcal\\pylabcalgui\\CS260-Window')
sys.path.append('..\\..\\pylablib\\instruments')

from cs260_dialog_mainwindow import *
from CS260 import *

#ADC inputs on the LabJack
DETECTOR_PORT = 'AIN0'
CHOPREF_PORT = 'AIN1'

MANUAL_MEASURE_PATH = '.\\data\\manual-measurements.csv'

async def main():
    #Create and start measure task execution
    scan_sync_queue = asyncio.Queue() #queue for syncronization between scan task and measure task
    meas_task = asyncio.create_task(measure_task(scan_sync_queue))
    window = CS260Window(cs, scan_sync_queue=scan_sync_queue)
    window.show()
    #infinite pend loop so that program execution doesn't halt
    await meas_task


async def measure_task(scan_sync_queue):
    #Initialize LabJack U6
    lju6 = u6.U6()
    lju6.getCalibrationData()
    lju6.streamConfig(NumChannels=2, ChannelNumbers=[0, 1], ChannelOptions=[0, 0], 
                      SettlingFactor=1, ResolutionIndex=1, ScanFrequency=5e3)

    data = {'Sequence': [], 'Grating': [], 'Wavelength': [], 'Filter': [],
            'Shutter': [], 'Integration Time': [], 'Detector Voltage': []}

    #Task run loop
    while True:
        #pend on sync_event set by cs scan task
        message = asyncio.create_task(scan_sync_queue.get())
        await message
        message = message.result() 
        #if message received from queue is a .csv file name, then write out a csv and prepare dictionary for new scan series
        if type(message) is str and message == "done":
            df = pd.DataFrame(data)
            df.to_csv(message['Sequence'], index=False)
            data = {'Grating': [], 'Wavelength': [], 'Detector Voltage': []}

        elif type(message) is dict and message['Sequence'] == '_manual-measurement_':
            df = pd.read_csv(MANUAL_MEASURE_PATH)

        #otherwise, run LabJack measurement over the measure interval received through message
        else:
            #copy data from message, this is just for readability
            measure_interval = message
            #record current monochromator state
            data['Grating'].append(message['Grating'])
            data['Wavelength'].append(message['Wavelength'])
            #start taking data on Labjack
            detector_data = []
            start_time = time.perf_counter()
            lju6.streamStart()
            for measure in lju6.streamData():
                #stop condition
                if time.perf_counter() >= (start_time + measure_interval):
                    break

                if measure is not None and measure['errors'] == 0:
                    d = measure[DETECTOR_PORT]
                    detector_data.append(sum(d)/len(d))

                await asyncio.sleep(0.001) #short pend to allow other things to run
            #End labjack stream and add average detector voltage to dictionary
            lju6.streamStop()
            data['Detector Voltage'].append(sum(detector_data)/len(detector_data))
            #acknowledge that data has been read and recorded for the specified measurement interval
            scan_sync_queue.put_nowait("ack")


if __name__ == "__main__":
    
    #Create cs260 control instance
    exe_path = "..\\..\\pylablib\\instruments\\CS260-Drivers\\C++EXE.exe"
    cs = CS260(exe_path)

    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(main())
        loop.close()
    cs.close()
    sys.exit(app.exec_())
