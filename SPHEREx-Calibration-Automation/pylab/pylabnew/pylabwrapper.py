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

# Global data objects ###################################
# queue for communication between gui and state machine
GuiToSmDataQueue = asyncio.Queue()
SmToGuiDataQueue = asyncio.Queue()
#########################################################


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    queue = asyncio.Queue()
    seq_dir = ".\\config\\sequence\\"
    gui = GUI(sequence_dir=seq_dir, data_queue_rx=SmToGuiDataQueue, data_queue_tx=GuiToSmDataQueue)
    SM = SpectralCalibrationMachine(data_queue_rx=GuiToSmDataQueue, data_queue_tx=SmToGuiDataQueue)
    asyncio.create_task(SM.start_machine())
    gui.form.show()
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
