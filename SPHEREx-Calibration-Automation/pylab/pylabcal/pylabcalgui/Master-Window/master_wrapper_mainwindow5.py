import sys
import os
import pdb
import asyncio
from qasync import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from scanWindowDialog4 import Ui_Dialog as masterDialog

#add package root directory to search path
sys.path.append("..\\..\\..\\")
from pylabcal.pylabcalsm.pylabcal_sm import SpectralCalibrationMachine, ControlLoopParams


class masterWindow(QtWidgets.QDialog):
    """
    Spectral calibration master control GUI window
    """
    def __init__(self):
        super().__init__()

        ##State Machine#############################
        self.state_machine = SpectralCalibrationMachine()
        self.control_loop_params = ControlLoopParams()

        ##Set up main UI dialog############################################################
        self.ui = masterDialog()
        self.ui.setupUi(self)
        ###################################################################################

        #If initialization was successful, then move on to Waiting state
        state_status = self.state_machine.get_state_status()
        if state_status == SpectralCalibrationMachine.STATE_COMPLETE_SUCCESS:
            self.state_machine.next_state()

        self.ui.set_parameters_button_tab4.clicked.connect(self.set_monochromator_parameters_manual)
        self.ui.run_single_tab1.clicked.connect(self.start_scan_series)
        self.ui.run_series_tab1.clicked.connect(self.start_scan_series)
        self.ui.run_single_tab2.clicked.connect(self.start_scan_series)
        self.ui.run_series_tab2.clicked.connect(self.start_scan_series)

    def set_monochromator_parameters_manual(self):
        cur_state = self.state_machine.get_state()
        if cur_state == 'Waiting':
            #Reset control loop parameters
            self.control_loop_params.reset()

            #Set monochromator params#################################################
            grating = self.ui.grating_new_cbox_tab4.currentIndex() + 1
            self.control_loop_params.monochromator['grating'] = [grating]
            wavelength = float(self.ui.wavelength_new_ledit_tab4.text())
            self.control_loop_params.monochromator['start-wavelength'] = [wavelength]
            self.control_loop_params.monochromator['stop-wavelength'] = [wavelength]
            self.control_loop_params.monochromator['step-size'] = [0]

            ##Since this function should only change Monochromator, leave all other parameters in reset state

            #Enter next state, pass in new control loop parameters
            self.state_machine.next_state(next_state_data=self.control_loop_params)
        else:
            print("Cannot enter Thinking from {}".format(cur_state))

    def start_scan_series(self):
        cur_state = self.state_machine.get_state()
        if cur_state == 'Waiting':
            self.state_machine.next_state()
        else:
            print("Cannot enter Thinking from {}".format(cur_state))


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
