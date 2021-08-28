""" pylabwrapper:

    Main module for the SPHEREx Optical Test and Calibration Software Pipeline.

Sam Condon, California Institute of Technology
Marco Viero, California Institute of Technology
"""


# IMPORT PACKAGES ###########################################################
import sys
import asyncio
from qasync import QEventLoop
from PyQt5 import QtCore, QtWidgets
from pylabgui.pylabcalgui_main import GUI
from pylabsm.pylabsm_spectral import SpectralCalibrationMachine
#############################################################################


async def main():
    # Global data objects ###################################
    # queue for communication between gui and state machine
    gui_to_sm_data_queue = asyncio.Queue()
    sm_to_gui_data_queue = asyncio.Queue()
    #########################################################

    queue = asyncio.Queue()
    seq_dir = ".\\config\\sequence\\"
    gui = GUI(sequence_dir=seq_dir, data_queue_rx=sm_to_gui_data_queue, data_queue_tx=gui_to_sm_data_queue)
    SM = SpectralCalibrationMachine(data_queue_rx=gui_to_sm_data_queue, data_queue_tx=sm_to_gui_data_queue)
    sm_task = asyncio.create_task(SM.start_machine())
    gui_task = asyncio.create_task(gui.standalone_run())
    gui.form.show()
    await asyncio.gather(sm_task, gui_task)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    asyncio.create_task(main())
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
