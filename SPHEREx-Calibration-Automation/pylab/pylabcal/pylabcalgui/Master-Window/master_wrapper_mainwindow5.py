import sys
import os
import pdb
import asyncio
from qasync import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from scanWindowDialog4 import Ui_Dialog as masterDialog

#add package root directory to search path
sys.path.append("..\\..\\..\\")
from pylabcal.pylabcalsm.pylabcal_sm import SpectralCalibrationMachine


class masterWindow(QtWidgets.QDialog):
    """
    Spectral calibration master control GUI window
    """
    def __init__(self):
        super().__init__()

        ##State Machine#############################
        self.state_machine = SpectralCalibrationMachine()

        ##Set up main UI dialog############################################################
        self.ui = masterDialog()
        self.ui.setupUi(self)
        ###################################################################################

        #If initialization was successful, then move on to Waiting state
        state_status = self.state_machine.get_state_status()
        if state_status == SpectralCalibrationMachine.STATE_COMPLETE_SUCCESS:
            self.state_machine.next_state()

        self.ui.set_parameters_button_tab4.clicked.connect(self.set_monochromator_parameters_manual)

    def set_monochromator_parameters_manual(self):
        if self.state_machine.get_state() == 'Waiting':
            self.state_machine.next_state()
        else:
            print("Cannot enter Thinking state from {}".format(self.state_machine.get_state()))

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    window = masterWindow()#cs)
    window.show()
    with loop:
        loop.run_forever()
        loop.close()
    sys.exit(app.exec_())
