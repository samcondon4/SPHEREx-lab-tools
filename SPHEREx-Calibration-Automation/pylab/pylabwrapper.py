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
#########################################################


async def main():
    try:
        gui_to_sm_data_queue = asyncio.Queue()
        sm_to_gui_data_dict = {}
        seq_dir = ".\\config\\sequence\\"
        gui = GUI(sequence_dir=seq_dir, data_queue_rx=sm_to_gui_data_dict, data_queue_tx=gui_to_sm_data_queue)
        SM = SpectralCalibrationMachine(data_queue_rx=gui_to_sm_data_queue, data_queue_tx=sm_to_gui_data_dict)
        sm_task = asyncio.create_task(SM.start_machine())
        inst_init_complete = False
        await asyncio.sleep(5)
        gui.form.show()
        gui_task = asyncio.create_task(gui.run())
        await asyncio.gather(sm_task, gui_task)
    except Exception as e:
        print("Exception {} occured".format(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    with EventLoop:
        EventLoop.create_task(main())
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
