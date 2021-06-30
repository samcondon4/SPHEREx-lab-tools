"""pylabcal:

    This is the main module for the SPHEREx spectral calibration automation software.

Contributors:
    Sam Condon, California Institute of Technology
    Marco Viero, California Institute of Technology

06/21/2021
"""

##IMPORT PACKAGES#################################################################################
import asyncio
import sys
import os
from qasync import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablibsm import SM
from pylablib.utils.parameters import write_config_file, get_params_dict

sys.path.append(r"pylabcal\\pylabcalgui\\ManualWindow")
from manualWindowDialogWrapper import ManualWindow

sys.path.append(r"pylabcal\\pylabcalgui\\AutomationWindow")
from automationWindowDialogWrapper import AutomationWindow

sys.path.append(r"pylablib\\instruments")
from CS260 import CS260
###################################################################################################


##MAIN GUI CLASS###################################################################################
class MainWindow:
    """MainWindow:

        This class connects all of the spectral calibration tabs into one QTabWidget
    """
    def __init__(self, Dialog, root_path=".\\", seq_config_path="pylabcal\\config\\sequence"):
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.auto_gui = AutomationWindow()
        self.manual_gui = ManualWindow()

        self.tabWidget.addTab(self.auto_gui.form, "Automation")
        self.tabWidget.addTab(self.manual_gui.form, "Manual Control")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
####################################################################################################


##STATE MACHINE ACTIONS#############################################################################
class SpectralCalibrationMachine:
    """Actions:

        This class defines all of the actions to execute within the state machine
    """
    def __init__(self, dialog):
        #Instruments##############
        self.monochromator = None
        self.lock_in = None
        ##########################

        #State Machine##########################################################################################
        #actions##################
        self.state_machine = SM()
        self.state_machine.add_action_to_state('Initializing', 'init_action_0', self.init_action)
        self.state_machine.add_action_to_state('Waiting', 'manual_waiting_action', self.manual_waiting_action, coro=True)
        self.state_machine.add_action_to_state('Waiting', 'auto_waiting_action', self.auto_waiting_action, coro=True)
        self.state_machine.add_action_to_state('Thinking', 'thinking_action_0', self.thinking_action, coro=False)

        #action coordination variables###
        self.waiting_complete = False
        ########################################################################################################

        #Gui###########################
        self.gui = MainWindow(dialog)
        ###############################

        #Start state machine#
        self.state_machine.start_machine()

    def init_action(self, action_dict):
        """init_action: **STATE_MACHINE ACTION**

                Initialize communication w/ monochromator, lock-in, and populate gui displays with
                default values

        :param action_dict: action dictionary passed in through state machine.
        :return: None
        """
        init_success = True
        #Initialize communication with monochromator
        #self.monochromator = CS260()
        # Initialize communication with lock in amplifier

        # Initialize gui ##############################################################################################
        ###############################################################################################################

        '''
        if not self.monochromator.com_success:
            init_success = False
        '''

        #If all initializations were successful, transition to the Waiting state
        if init_success:
            action_dict['state_machine'].init_to_wait()

    async def manual_waiting_action(self, action_dict):
        """ manual_waiting_action: **STATE MACHINE ACTION**

               Poll for Manual Tab button presses and send appropriate arguments to thinking
               action when a press is seen.

        :param action_dict: action dictionary passed in through state-machine.
        :return: None
        """
        complete_set = False
        while not self.waiting_complete:
            manual_press = self.gui.manual_gui.get_button()
            if manual_press == "Monochromator Set Parameters":
                mono_params = self.gui.manual_gui.get_parameters("Monochromator")
                self.state_machine.set_action_parameters("Thinking", "thinking_action_0", mono_params)
                self.waiting_complete = True
                complete_set = True
            await asyncio.sleep(0.001)

        #Coordination with the auto_waiting_action and state transition######
        if not complete_set:
            self.waiting_complete = False
            self.state_machine.wait_to_think()
        ######################################################################

    async def auto_waiting_action(self, action_dict):
        """ auto_waiting_action: **STATE MACHINE ACTION**

               Poll for Automation Tab button presses and send appropriate arguments to thinking
               action when a press is seen.

        :param action_dict: action dictionary passed in through state-machine.
        :return: None
        """
        complete_set = False
        while not self.waiting_complete:
            auto_press = self.gui.auto_gui.get_button()
            if auto_press == "Run Series":
                auto_params = self.gui.auto_gui.get_parameters("Series")
                self.state_machine.set_action_parameters('Thinking', 'thinking_action_0', auto_params)
                self.waiting_complete = True
                complete_set = True
            await asyncio.sleep(0.001)

        #Coordination with the manual_waiting_action and state transition####
        if not complete_set:
            self.waiting_complete = False
            self.state_machine.wait_to_think()
        ######################################################################

    def thinking_action(self, action_dict):
        """ thinking_action: **STATE MACHINE ACTION**

                Build control loop from parameters that are passed in through the waiting actions.

        :param action_dict: action dictionary passed in through state-machine
        :return:
        """
        print(action_dict['params'])

    def moving_action(self, action_dict):
        pass

    def measuring_action(self, action_dict):
        pass

    def checking_action(self, action_dict):
        pass

    def compressing_action(self, action_dict):
        pass

    def writing_action(self, action_dict):
        pass

    def resetting_action(self, action_dict):
        pass

    def troubleshooting_action(self, action_dict):
        pass
####################################################################################################


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    #Create SpectralCalibrationMachine################
    SpectralCal = SpectralCalibrationMachine(Dialog)
    Dialog.show()
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
