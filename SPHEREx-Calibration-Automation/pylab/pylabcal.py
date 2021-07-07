"""pylabcal:

    This is the main module for the SPHEREx spectral calibration automation software.

Contributors:
    Sam Condon, California Institute of Technology
    Marco Viero, California Institute of Technology

06/21/2021
"""

# IMPORT PACKAGES #################################################################################
import asyncio
import sys
import datetime
import numpy as np
from qasync import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablibsm import SM
from pylablib.housekeeping import Housekeeping

sys.path.append(r"pylabcal\\pylabcalgui\\ManualWindow")
from manualWindowDialogWrapper2 import ManualWindow

sys.path.append(r"pylabcal\\pylabcalgui\\AutomationWindow")
from automationWindowDialogWrapper import AutomationWindow

sys.path.append(r"pylabcal\\pylabcalgui\\PowermaxWindow")
from powermaxLiveWindowDialogWrapper import PowermaxWindow

sys.path.append(r"pylablib\\instruments")
from CS260 import CS260
from powermaxusb2 import Powermax
from labjacku6 import Labjack
###################################################################################################


# MAIN GUI CLASS ###################################################################################
class MainWindow:
    """MainWindow:

        This class connects all of the spectral calibration tabs into one QTabWidget
    """

    def __init__(self, tabs, dialog, root_path=".\\", seq_config_path="pylabcal\\config\\sequence"):
        self.gridLayout = QtWidgets.QGridLayout(dialog)
        self.tabWidget = QtWidgets.QTabWidget(dialog)
        self.tabs = {}
        for tab in tabs:
            self.tabWidget.addTab(tab["Qt"].form, tab["id"])
            self.tabs[tab["id"]] = tab["Qt"]

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(dialog)


####################################################################################################


# STATE MACHINE ACTIONS#############################################################################
class SpectralCalibrationMachine:
    """Actions:

        This class defines all of the actions to execute within the state machine
    """

    def __init__(self, control_dialog, hk_dialog):
        # Instruments##############
        self.monochromator = None
        self.lock_in = None
        self.powermax = None
        self.labjack = None
        ##########################

        # Gui initialization ###########################################################################################
        hk_tabs = [{"Qt": PowermaxWindow(), "id": "Powermax"}]
        self.hk_gui = MainWindow(hk_tabs, hk_dialog)

        control_tabs = [{"Qt": AutomationWindow(), "id": "Automation"}, {"Qt": ManualWindow(), "id": "Manual"}]
        self.control_gui = MainWindow(control_tabs, control_dialog)
        ################################################################################################################

        # State Machine################################################################################################
        # actions##################
        self.state_machine = SM()
        self.state_machine.add_action_to_state('Initializing', 'init_action_0', self.init_action)
        self.state_machine.add_action_to_state('Waiting', 'manual_waiting_action', self.manual_waiting_action,
                                               coro=True)
        self.state_machine.add_action_to_state('Waiting', 'auto_waiting_action', self.auto_waiting_action, coro=True)
        self.state_machine.add_action_to_state('Thinking', 'thinking_action_0', self.thinking_action, coro=False)
        self.state_machine.add_action_to_state('Moving', 'moving_action_0', self.moving_action, coro=True)
        self.state_machine.add_action_to_state("Measuring", "measuring_action_0", self.measuring_action, coro=False)
        self.state_machine.add_action_to_state("Checking", "checking_action_0", self.checking_action, coro=False)
        self.state_machine.add_action_to_state("Compressing", "compressing_action_0", self.compressing_action,
                                               coro=False)
        self.state_machine.add_action_to_state("Writing", "writing_action_0", self.writing_action, coro=False)
        self.state_machine.add_action_to_state("Resetting", "resetting_action_0", self.resetting_action, coro=False)

        # action coordination variables###
        self.waiting_complete = False
        self.control_loop_index = 0
        self.control_loop_length = 0
        ###############################################################################################################

        # Start housekeeping ###############
        self.hk_task = asyncio.create_task(self.run_housekeeping())
        ####################################

        # Start state machine ##############
        self.state_machine.start_machine()
        ####################################

    async def run_housekeeping(self):
        """run_housekeeping: **HOUSEKEEPING COROUTINE**
                Run all housekeeping data-logging and gui displays.

        :param: None
        :return: None
        """
        # Initialize housekeeping class, instruments, and gui ###############
        Housekeeping.time_sync_method = datetime.datetime.now
        self.powermax = Powermax()
        self.powermax.open()
        active_wave = str(float(self.powermax.get_parameters("active wavelength")["active wavelength"]) * (1e-3))
        self.hk_gui.tabs["Powermax"].set_parameters({"active wavelength": active_wave})
        Housekeeping.start()
        powermax_logging = False
        #####################################################################

        # Run housekeeping data logging and display ##############################################################
        while True:
            button = self.hk_gui.tabs["Powermax"].get_button()

            if button == "Start Acquisition":
                active_wave = float(
                    self.hk_gui.tabs["Powermax"].get_parameters("active wavelength")["active wavelength"]) \
                              * 1e3
                await self.powermax.set_parameters({"active wavelength": active_wave})
                await self.powermax.on_data_log()
                powermax_logging = True

            elif button == "Stop Acquisition":
                await self.powermax.off_data_log()
                powermax_logging = False

            elif button == "Zero Sensor":
                self.powermax.set_zero()

            if powermax_logging:
                get_log_task = asyncio.create_task(self.powermax.get_log(final_val=True))
                await get_log_task
                data = get_log_task.result()
                data = float(data["Watts"])
                self.hk_gui.tabs["Powermax"].set_parameters({"data append": data})

            await asyncio.sleep(0.001)
        ############################################################################################################

    def init_action(self, action_dict):
        """init_action: **STATE_MACHINE ACTION**

                Initialize communication w/ monochromator, lock-in, and populate gui displays with
                default values

        :param action_dict: action dictionary passed in through state machine.
        :return: None
        """
        init_success = True
        # Initialize communication with all instruments in experiment setup ##
        self.monochromator = CS260()
        self.monochromator.open()
        self.labjack = Labjack()
        self.labjack.open()
        #######################################################################

        # Initialize labjack dio ports and gui control window #############################
        dio_cfg_init = {}
        dio_state_init = {}
        dio_init = {}
        for i in range(22):
            dio_cfg_init[i] = "Output"
            dio_state_init[i] = 0
            dio_init[i] = {"State": 0, "Config": "Output"}
        self.labjack.set_dio_config(dio_cfg_init)
        self.labjack.set_dio_state(dio_state_init)

        self.control_gui.tabs["Manual"].set_parameters({"LabJack": dio_init})
        ###################################################################################

        # Initialize monochromator gui control window #####################################
        mono_params = self.monochromator.get_parameters("All")
        self.control_gui.tabs["Manual"].set_parameters({"Monochromator": mono_params})
        ###################################################################################

        # If all initializations were successful, transition to the Waiting state
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
        thinking_params = {"Manual": True}
        while not self.waiting_complete:
            manual_press = self.control_gui.tabs["Manual"].get_button()
            if manual_press == "Monochromator Set Parameters":
                mono_params = self.control_gui.tabs["Manual"].get_parameters("Monochromator")
                thinking_params["Monochromator"] = mono_params["Monochromator"]
                self.state_machine.set_action_parameters("Thinking", "thinking_action_0", thinking_params)
                self.waiting_complete = True
                complete_set = True

            elif manual_press == "Lock-In Set Parameters":
                lockin_params = self.control_gui.tabs["Manual"].get_parameters("Lock-In")
                thinking_params["Lock-In"] = lockin_params["Lock-In"]
                thinking_params["Lock-In"].pop("sample time")
                thinking_params["Lock-In"].pop("measurement storage path")
                action_dict["state_machine"].set_action_parameters("Thinking", "thinking_action_0", thinking_params)
                self.waiting_complete = True
                complete_set = True

            elif manual_press == "Start Measurement":
                lockin_params = self.control_gui.tabs["Manual"].get_parameters("Lock-In")
                thinking_params["Lock-In"] = lockin_params["Lock-In"]
                action_dict["state_machine"].set_action_parameters("Thinking", "thinking_action_0", thinking_params)
                self.waiting_complete = True
                complete_set = True

            await asyncio.sleep(0.001)

        # Coordination with the auto_waiting_action and state transition######
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
        thinking_params = {"Manual": False}
        while not self.waiting_complete:
            auto_press = self.control_gui.tabs["Automation"].get_button()
            if auto_press == "Run Series":
                auto_params = self.control_gui.tabs["Automation"].get_parameters("Series")
                thinking_params["Series"] = auto_params["Series"]
                action_dict['state_machine'].set_action_parameters('Thinking', 'thinking_action_0', thinking_params)
                self.waiting_complete = True
                complete_set = True
            await asyncio.sleep(0.001)

        # Coordination with the manual_waiting_action and state transition####
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
        params = action_dict["params"]
        self.control_loop_index = 0
        if params["Manual"]:
            if "Lock-In" in params:
                measuring_control_loop = [params]
            else:
                measuring_control_loop = None
            moving_control_loop = [params]
            self.control_loop_length = 1
        else:
            # Build monochromator control loop parameters ############################################################
            mono_params = [sequence["Monochromator"] for sequence in params["Series"]]
            # wavelengths ##
            mono_waves = [np.arange(float(m["start wavelength"]), float(m["stop wavelength"]), float(m["step size"]))
                          for m in mono_params]
            # gratings ##
            g1g2_transitions = [float(m["g1 to g2 transition wavelength"]) for m in mono_params]
            g2g3_transitions = [float(m["g2 to g3 transition wavelength"]) for m in mono_params]
            mono_gratings = [[0 for w in waves] for waves in mono_waves]
            transition_ind = 0
            for wave_arr in mono_waves:
                grating_ind = 0
                for w in wave_arr:
                    if w < g1g2_transitions[transition_ind]:
                        mono_gratings[transition_ind][grating_ind] = "G1"
                    elif g1g2_transitions[transition_ind] < w < g2g3_transitions[transition_ind]:
                        mono_gratings[transition_ind][grating_ind] = "G2"
                    elif w > g2g3_transitions[transition_ind]:
                        mono_gratings[transition_ind][grating_ind] = "G3"
                    grating_ind += 1
                transition_ind += 1

            # order sort filters #
            noosf_osf1_transitions = [float(m["no osf to osf1 transition wavelength"]) for m in mono_params]
            osf1_osf2_transitions = [float(m["osf1 to osf2 transition wavelength"]) for m in mono_params]
            osf2_osf3_transitions = [float(m["osf2 to osf3 transition wavelength"]) for m in mono_params]
            mono_filters = [[0 for w in waves] for waves in mono_waves]
            transition_ind = 0
            for wave_arr in mono_waves:
                filter_ind = 0
                for w in wave_arr:
                    if w < noosf_osf1_transitions[transition_ind]:
                        mono_filters[transition_ind][filter_ind] = "No OSF"
                    elif noosf_osf1_transitions[transition_ind] < w < osf1_osf2_transitions[transition_ind]:
                        mono_filters[transition_ind][filter_ind] = "OSF1"
                    elif osf1_osf2_transitions[transition_ind] < w < osf2_osf3_transitions[transition_ind]:
                        mono_filters[transition_ind][filter_ind] = "OSF2"
                    elif osf2_osf3_transitions[transition_ind] < w:
                        mono_filters[transition_ind][filter_ind] = "OSF3"
                    filter_ind += 1
                transition_ind += 1
            ##########################################################################################################

            # Build Lock-In Control Loop Parameters ##################################################################
            lockin_params = [sequence["Lock-In"] for sequence in params["Series"]]
            lockin_fs = [[lockin_params[i]["sample frequency"] for n in range(len(mono_waves[i]))]
                         for i in range(len(lockin_params))]
            lockin_ts = [[lockin_params[i]["sample time"] for n in range(len(mono_waves[i]))]
                         for i in range(len(lockin_params))]
            lockin_tc = [[lockin_params[i]["time constant"] for n in range(len(mono_waves[i]))]
                         for i in range(len(lockin_params))]
            lockin_sens = [lockin["sensitivity string"].split(',') for lockin in lockin_params]
            lockin_sens_transitions = [np.linspace(mono_waves[i][0], mono_waves[i][-1], len(lockin_sens[i]))
                                       for i in range(len(lockin_sens))]
            lockin_sensitivites = [[0 for w in waves] for waves in mono_waves]
            transition_ind = 0
            for wave_arr in mono_waves:
                sens_ind = 0
                i = 0
                for w in wave_arr:
                    if w > lockin_sens_transitions[transition_ind][i]:
                        i += 1
                    lockin_sensitivites[transition_ind][sens_ind] = lockin_sens[transition_ind][i]
                    sens_ind += 1
                transition_ind += 1
            ##########################################################################################################

            # Flatten parameter arrays ################################################################
            mono_waves = [w for wave_arr in mono_waves for w in wave_arr]
            mono_gratings = [g for g_arr in mono_gratings for g in g_arr]
            mono_filters = [f for f_arr in mono_filters for f in f_arr]

            lockin_fs = [fs for fs_arr in lockin_fs for fs in fs_arr]
            lockin_ts = [ts for ts_arr in lockin_ts for ts in ts_arr]
            lockin_tc = [tc for tc_arr in lockin_tc for tc in tc_arr]
            lockin_sensitivites = [sens for sens_arr in lockin_sensitivites for sens in sens_arr]
            ###########################################################################################

            # Construct control loop for the moving action############################################################
            self.control_loop_length = len(mono_waves)

            moving_control_loop = [{
                "Monochromator": {"wavelength": mono_waves[i], "grating": mono_gratings[i],
                                  "filter": mono_filters[i], "shutter": "Open"},

                "Lock-In": {"sensitivity": lockin_sensitivites[i], "time constant": lockin_tc[i]}
            }
                for i in range(len(mono_waves))]
            ##########################################################################################################

            # Construct control loop for the measuring action ########################################################
            measuring_control_loop = [{
                "Lock-In": {"sample rate": lockin_fs[i], "sample time": lockin_ts[i]}
            }
                for i in range(len(mono_waves))]
            ##########################################################################################################

        # Pass control loop parameters to actions and start the control loop #########################################
        action_dict["state_machine"].set_action_parameters("Moving", "moving_action_0", moving_control_loop)
        action_dict["state_machine"].set_action_parameters("Measuring", "measuring_action_0", measuring_control_loop)
        action_dict["state_machine"].start_control_loop()
        ##############################################################################################################

    async def moving_action(self, action_dict):
        if not self.control_loop_index < self.control_loop_length:
            action_dict["state_machine"].control_loop_complete()
        else:
            move_params = action_dict["params"][self.control_loop_index]
            for instrument in move_params:
                inst_params = move_params[instrument]

                if instrument == "Monochromator":
                    await self.monochromator.set_parameters({"shutter": inst_params["shutter"]})
                    grating = inst_params["grating"]
                    grating = int(grating[1:])
                    await self.monochromator.set_parameters({"grating": grating})
                    filt = inst_params["filter"]
                    if filt == "No OSF":
                        filt = 4
                    else:
                        filt = int(filt[3:])
                    await self.monochromator.set_parameters({"filter": filt})
                    await self.monochromator.set_parameters({"wavelength": float(inst_params["wavelength"])})

            action_dict["state_machine"].control_loop_next()

    def measuring_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    def checking_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    def compressing_action(self, action_dict):
        action_dict["state_machine"].control_loop_next()

    def writing_action(self, action_dict):
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
    SpectralCal = SpectralCalibrationMachine(ControlDialog, HKDialog)
    ControlDialog.setWindowTitle("Control Window")
    HKDialog.setWindowTitle("Housekeeping Window")
    ControlDialog.show()
    HKDialog.show()
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
