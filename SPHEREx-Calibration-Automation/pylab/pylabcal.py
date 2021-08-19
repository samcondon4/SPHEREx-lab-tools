"""pylabcal:

    This is the main module for the SPHEREx spectral calibration automation software.

Contributors:
    Sam Condon, California Institute of Technology
    Marco Viero, California Institute of Technology

06/21/2021
"""

# IMPORT PACKAGES #################################################################################
import json
import sys
import datetime
import numpy as np
import asyncio
from qasync import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablibsm import SM
from pylablib.housekeeping import Housekeeping
from pylablib.instruments.CS260 import CS260
from pylablib.instruments.SR830 import SR830
from pylablib.instruments.labjacku6 import Labjack
from pylablib.instruments.ndfwheel import NDF
from pylabcal.pylabcalgui.pylabcalgui_main import GUI


###################################################################################################

# Miscellaneous helper functions/variables ###################################################################
FILTER_MAP = {"No OSF": 4, "OSF1": 1, "OSF2": 2, "OSF3": 3}
SHUTTER_MAP = {"Open": "O", "Closed": "C"}


##############################################################################################################


# STATE MACHINE ACTIONS#############################################################################
class SpectralCalibrationMachine:
    """Actions:

        This class defines all of the actions to execute within the state machine
    """

    def __init__(self, root_path, seq_config_path, instruments=None):

        # Instruments #############
        self.lock_in = None
        self.monochromator = None
        self.labjack = None
        self.ndf = None

        # Configuration paths #

        #######################

        # Gui initialization ###########################################################################################
        self.gui = GUI(root_path=root_path, seq_config_path=seq_config_path)
        ################################################################################################################

        # State Machine################################################################################################
        # actions##################
        self.state_machine = SM()
        self.state_machine.add_action_to_state('Initializing', 'init_action_0', self.init_action, coro=True)
        self.state_machine.add_action_to_state("Waiting", "waiting_action_0", self.waiting_action, coro=True)
        #self.state_machine.add_action_to_state('Waiting', 'manual_waiting_action', self.manual_waiting_action,
        # coro=True)
        #self.state_machine.add_action_to_state('Waiting', 'auto_waiting_action', self.auto_waiting_action, coro=True)
        self.state_machine.add_action_to_state('Thinking', 'thinking_action_0', self.thinking_action, coro=False)
        self.state_machine.add_action_to_state('Moving', 'moving_action_0', self.moving_action, coro=True)
        self.state_machine.add_action_to_state("Measuring", "measuring_action_0", self.measuring_action, coro=True)
        self.state_machine.add_action_to_state("Checking", "checking_action_0", self.checking_action, coro=False)
        self.state_machine.add_action_to_state("Compressing", "compressing_action_0", self.compressing_action,
                                               coro=False)
        self.state_machine.add_action_to_state("Writing", "writing_action_0", self.writing_action, coro=True)
        self.state_machine.add_action_to_state("Resetting", "resetting_action_0", self.resetting_action, coro=False)

        # action coordination variables###
        self.waiting_complete = False
        self.control_loop_index = 0
        self.control_loop_length = 0
        ###############################################################################################################

        # Start state machine ##############
        self.state_machine.start_machine()
        ####################################

    async def init_action(self, action_dict):
        """init_action: **STATE_MACHINE ACTION**

                Initialize communication w/ monochromator, lock-in, and populate gui displays with
                default values

        :param action_dict: action dictionary passed in through state machine.
        :return: None
        """
        init_success = True
        # Initialize communication with all instruments in experiment setup ##
        self.monochromator = CS260()
        #self.monochromator.open()
        self.lock_in = SR830()
        #self.lock_in.open()
        self.labjack = Labjack()
        #self.labjack.open()
        self.ndf = NDF()
        #self.ndf.open()
        #######################################################################

        # Initialize labjack dio ports and gui control window #############################
        """
        dio_cfg_init = {"dio config": {}}
        dio_state_init = {"dio state": {}}
        dio_init = {}
        for i in range(22):
            dio_cfg_init["dio config"][i] = "Output"
            dio_state_init["dio state"][i] = 0
            dio_init[i] = {"State": 0, "Config": "Output"}
        await self.labjack.set_parameters(dio_cfg_init)
        await self.labjack.set_parameters(dio_state_init)

        get_task = await self.labjack.get_parameters("All")
        await get_task
        self.gui.manual.set_parameters({"labjack": dio_init})
        """
        ###################################################################################

        # Initialize monochromator gui control window #####################################
        """
        get_task = asyncio.create_task(self.monochromator.get_parameters("All"))
        await get_task
        mono_params = get_task.result()
        self.gui.manual.set_parameters({"monochromator": mono_params})
        """
        ###################################################################################

        # Initialize lock_in gui control window ###########################################
        """
        lockin_params = await asyncio.create_task(self.lock_in.get_parameters("All"))
        phase = lockin_params["phase"]
        ref_freq = lockin_params["reference frequency"]
        sens = self.lock_in.calc_sens_val_mult_unit(lockin_params)
        tc = self.lock_in.calc_tc_val_mult_unit(lockin_params)
        fs = lockin_params["sample rate"]
        if fs >= 1:
            fs = int(fs)
        lockin_gui_dict = {
            "phase": phase,
            "reference frequency": ref_freq,
            "sensitivity": "{}{}".format(sens["value"] * sens["multiplier"], sens["units"]),
            "time-constant": "{}{}".format(tc["value"] * tc["multiplier"], tc["units"]),
            "sample rate": str(fs),
            "sample time": "10"
        }
        self.gui.manual.set_parameters({"Lock-In": lockin_gui_dict})
        """
        ###################################################################################

        # Initialize ndf gui control window ###############################################
        #ndf_params = await self.ndf.get_parameters("All")
        #self.gui.manual.set_parameters({"ndf": ndf_params})
        ###################################################################################

        # Initialize housekeeping window ##################################################
        """
        get_task = asyncio.create_task(self.powermax.get_parameters("active wavelength"))
        await get_task
        active_wave = get_task.result()
        print(active_wave)
        self.hk_gui.tabs["Powermax"].set_parameters({"active wavelength": active_wave["active wavelength"]})
        """
        ###################################################################################

        # If all initializations were successful, transition to the Waiting state
        if init_success:
            action_dict['state_machine'].init_to_wait()

    async def waiting_action(self):
        pass

    def thinking_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    async def moving_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    async def measuring_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    def checking_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    def compressing_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    async def writing_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    def resetting_action(self, action_dict):
        self.control_loop_index += 1
        action_dict["state_machine"].control_loop_next()

    def troubleshooting_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()


####################################################################################################


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ControlDialog = QtWidgets.QDialog()
    HKDialog = QtWidgets.QDialog()
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    # Create SpectralCalibrationMachine################
    root_dir = "C:\\Users\\thoma\\Documents\\Github\\SPHEREx-lab-tools\\SPHEREx-Calibration-Automation\\pylab\\"
    seq_cfg_dir = "\\pylabcal\\config\\sequence\\"
    SpectralCal = SpectralCalibrationMachine(root_dir, seq_cfg_dir)
    ControlDialog.setWindowTitle("Control Window")
    HKDialog.setWindowTitle("Housekeeping Window")
    ControlDialog.show()
    HKDialog.show()
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
