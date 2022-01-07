""" main:

    Main module for the SPHEREx Spectral Calibration Measurement.

Sam Condon, California Institute of Technology
Marco Viero, California Institute of Technology
"""


# IMPORT PACKAGES ###########################################################
import os
import sys
import asyncio
from qasync import QEventLoop
from PyQt5 import QtCore, QtWidgets
from .gui_main import GUI
from .sm_main import SpectralCalibrationMachine
#############################################################################

# Global data objects ###################################
# queue for communication between gui and state machine
#########################################################


async def main():
    try:
        gui_to_sm_data_queue = asyncio.Queue()
        sm_to_gui_data_queue = {}
        seq_dir = os.path.join(os.getcwd(), "applications", "spectral_cal", "config", "sequence", "")
        SM = SpectralCalibrationMachine(data_queue_rx=gui_to_sm_data_queue, data_queue_tx=sm_to_gui_data_queue)
        gui = GUI(sequence_dir=seq_dir, data_queue_rx=sm_to_gui_data_queue, data_queue_tx=gui_to_sm_data_queue)
        sm_task = asyncio.create_task(SM.start_machine())
        await asyncio.sleep(5)
        gui.form.show()
        gui_task = asyncio.create_task(gui.run())
        await asyncio.gather(sm_task, gui_task)
    except Exception as e:
        print("Exception {} occured".format(e))


def run():
    app = QtWidgets.QApplication(sys.argv)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    with EventLoop:
        EventLoop.create_task(main())
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
