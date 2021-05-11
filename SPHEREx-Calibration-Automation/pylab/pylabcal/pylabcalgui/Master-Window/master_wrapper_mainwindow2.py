import pdb
import sys
import os
import datetime as datetime
from qasync import QEventLoop
import asyncio
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append("..\\CS260-Window")
sys.path.append("..\\..\\..\\pylablib\\instruments")

# UI files
# from cs260_dialog_ui import Ui_Dialog as cs260_dialog
from cs260_dialog_popup import Cs260PopupDialog
from scanWindowDialog2 import Ui_Dialog as masterDialog
from CS260 import CS260

SEQUENCE_ROLE = 1


class ScanSequence:
    """
    data structure to hold the parameters of a single scan sequence
    """

    def __init__(self, name=None, grating=None, osf=None, start_wave=None,
                 end_wave=None, step_wave=None, measure_interval=None):
        self.name = name
        self.grating = grating
        self.osf = osf
        self.start_wave = start_wave
        self.end_wave = end_wave
        self.step_wave = step_wave
        self.measure_interval = measure_interval


class masterWindow(QDialog):
    """
    masterWindow dialog class.
    """

    #def __init__(self, cs260_obj, sync_queue=None):
    def __init__(self, sync_queue=None):
        super().__init__()

        ##Class attributes###############################
        # cs260 monochromator class instance
        # self.cs260 = cs260_obj
        self.current_sequence = None

        # event for synchronization between an external task and the scan series task
        self.sync_queue = sync_queue
        #################################################

        ##Set up main UI dialog############################################################
        self.ui = masterDialog()
        self.ui.setupUi(self)
        # self.ui.sequence_config_files = QListWidget()
        ###################################################################################

        ##Common tab buttons: Add/Edit/Remove Sequence #############################
        self.ui.add_sequence_button_tab1.clicked.connect(self.add_sequence)
        self.ui.add_sequence_button_tab2.clicked.connect(self.add_sequence)
        self.ui.add_sequence_button_tab3.clicked.connect(self.add_sequence)
        self.ui.edit_sequence_button_tab2.clicked.connect(self.edit_sequence)
        self.ui.remove_sequence_button_tab1.clicked.connect(self.remove_sequence)
        self.ui.remove_sequence_button_tab2.clicked.connect(self.remove_sequence)
        #self.ui.remove_sequence_button_tab3.clicked.connect(self.remove_sequence)
        self.ui.sequence_config_files_tab1.clicked.connect(self.update_current_sequence)
        self.ui.sequence_config_files_tab2.clicked.connect(self.update_current_sequence)
        self.ui.sequence_config_files_tab3.clicked.connect(self.update_current_sequence)

        ##Common tab buttons: Run Sequence, Run Series, Abort #############################
        self.ui.run_single_tab1.clicked.connect(self.start_scan_series)
        self.ui.run_single_tab2.clicked.connect(self.start_scan_series)
        self.ui.run_single_tab3.clicked.connect(self.start_scan_series)
        self.ui.run_series_tab1.clicked.connect(self.start_scan_series)
        self.ui.run_series_tab2.clicked.connect(self.start_scan_series)
        self.ui.run_series_tab3.clicked.connect(self.start_scan_series)
        self.ui.abort_scan_button_tab1.clicked.connect(self.abort)
        self.ui.abort_scan_button_tab2.clicked.connect(self.abort)
        self.ui.abort_scan_button_tab3.clicked.connect(self.abort)
        #########################################################################

        ### First Tab Sequence File List

        ### Common tab Status Log

        ##Manual tab init#####################################################
        ####Set all display values to monochromator current state#######
        asyncio.create_task(self.update_manual_display())
        #################################################################

        ####Manual tab buttons###########################################
        self.ui.set_parameters_button_tab4.clicked.connect(self.set_parameters)
        self.ui.abort_manual_button_tab4.clicked.connect(self.abort)
        #################################################################
        #########################################################################

        ####################################################################################

        ##Set up error dialog#######################################
        self.popup_dialog = Cs260PopupDialog()
        ############################################################################

        # Maintain list of executing coroutines. Anytime a coroutine is scheduled,
        # its associated task will be set to the corresponding dictionary value.
        self.coro_exec = {"grating": None, "osf": None, "wave": None, "set_params": None, "scan_series": None}

        # Display list of .cfg files in Tab 1
        path_config_file = self.ui.config_path_lineEdit_tab3.text()
        self.saved_config_files = []
        for file in os.listdir(path_config_file):
            # check the files which are end with specific extension
            if file.endswith(".cfg"):
                self.saved_config_files.append(file)

        for ifile in self.saved_config_files:
            self.ui.sequence_config_files_tab1.addItem(ifile)
            self.ui.sequence_config_files_tab2.addItem(ifile)
            self.ui.sequence_config_files_tab3.addItem(ifile)

    ##METHODS FOR BOTH SCAN AND MANUAL TABS#######################################
    def cs260_is_busy(self, error=True):
        """cs260_is_busy: check if there are any monochromator associated coroutines
                          active. Returns 1 if there are and 0 if not.
        """
        is_busy = 0
        error_message = []
        for coro_key in self.coro_exec:
            if self.coro_exec[coro_key] is not None:
                is_busy = 1
                if error:
                    error_message.append("CS260 busy!")
                    error_message.append("Abort current task or wait until it completes!")
                    self.popup_dialog.disp_errors(error_message)
                    self.popup_dialog.popup()
                break
        return is_busy

    def abort(self):
        """abort: kill all running cs260 coroutines/tasks and stop all cs260 motion

        """

        # Send abort command to cs260
        self.cs260.abort()
        # Always close shutter when aborting
        self.cs260.set_shutter("C")

        # Kill all running coroutines/tasks
        for coro in self.coro_exec:
            coro_exec = self.coro_exec[coro]
            if coro_exec is not None:
                coro_exec.cancel()
                self.coro_exec[coro] = None

        # Prompt user to check manual display for current state
        # Update manual display w/ current values
        asyncio.create_task(self.update_manual_display())
        msg = ["Abort complete.", "Check the manual display tab for current cs260 state."]
        self.popup_dialog.disp_msg(msg)
        self.popup_dialog.popup()

    ##############################################################################

    ##MANUAL TAB METHODS##########################################################
    def set_parameters(self):

        # Check if a monochromator control task is already running before starting anything else
        if self.cs260_is_busy():
            return

        # Always close shutter as first movement
        new_params = [("shutter", "C")]

        # If grating needs to be changed, do this next
        cur_grating = self.cs260.get_grating()
        new_grating = self.ui.grating_new_cbox_tab4.currentIndex() + 1
        if new_grating != cur_grating:
            new_params.append(("grating", new_grating))

        # Next take care of filter
        cur_osf = self.cs260.get_filter()
        new_osf = self.ui.osf_new_cbox_tab4.currentIndex() + 1
        if cur_osf != new_osf:
            new_params.append(("osf", new_osf))

        # Now wavelength
        cur_wave = self.cs260.get_wavelength()
        new_wave = float(self.ui.wavelength_new_ledit_tab4.text())
        if cur_wave != new_wave:
            new_params.append(("wave", new_wave))

        # If shutter needs to be opened, do this last
        new_shutter = self.ui.shutter_new_cbox_tab4.currentIndex()
        if new_shutter == 0:
            new_params.append(("shutter", "O"))

        # If any changes were made, execute asynchronous transition function
        if len(new_params) > 0:
            set_params_task = asyncio.create_task(self.set_parameters_async(new_params))
            # Register newly created task w/ executing task dictionary
            self.coro_exec['set_params'] = set_params_task

    async def set_parameters_async(self, params):
        for p in params:
            task = None
            if p[0] == "shutter":
                self.cs260.set_shutter(p[1])
            elif p[0] == "grating":
                task = asyncio.create_task(self.cs260.set_grating(p[1]))
            elif p[0] == "osf":
                task = asyncio.create_task(self.cs260.set_filter(p[1]))
            elif p[0] == "wave":
                task = asyncio.create_task(self.cs260.set_wavelength(p[1]))

            if task is not None:
                self.coro_exec[p[0]] = task
                await task
                self.coro_exec[p[0]] = None

        await asyncio.create_task(self.update_manual_display())
        # Task has completed. Remove it from the executing coroutine/task dictionary
        self.coro_exec['set_params'] = None

    async def update_manual_display(self):
        # Filter reading######################################################
        filter_read_task = asyncio.create_task(self.cs260.async_pend("osf"))
        await filter_read_task
        cur_filter = filter_read_task.result()
        self.ui.osf_current_ledit_tab4.setText("OSF{}".format(cur_filter))
        self.ui.osf_new_cbox_tab4.setCurrentIndex(cur_filter - 1)
        ######################################################################

        # Grating reading##############################################################
        grating_read_task = asyncio.create_task(self.cs260.async_pend("grating"))
        await grating_read_task
        cur_grating = grating_read_task.result()
        self.ui.grating_current_ledit_tab4.setText("G{}".format(self.cs260.get_grating()))
        self.ui.grating_new_cbox_tab4.setCurrentIndex(cur_grating - 1)
        ###############################################################################

        # Shutter reading###############################################################
        shutter_state = self.cs260.get_shutter()
        if shutter_state == "O":
            self.ui.shutter_current_ledit_tab4.setText("Open")
            self.ui.shutter_new_cbox_tab4.setCurrentIndex(0)
        elif shutter_state == "C":
            self.ui.shutter_current_ledit_tab4.setText("Closed")
            self.ui.shutter_new_cbox_tab4.setCurrentIndex(1)
        ###############################################################################

        # Wavelength reading###################################
        wave_read_task = asyncio.create_task(self.cs260.async_pend("wave"))
        await wave_read_task
        cur_wave = str(wave_read_task.result())
        self.ui.wavelength_current_ledit_tab4.setText(cur_wave)
        self.ui.wavelength_new_ledit_tab4.setText(cur_wave)
        #######################################################

    ################################################################################

    ##SCAN TAB METHODS#############################################################
    def start_scan_series(self):

        if self.cs260.get_units() != "UM":
            self.cs260.set_units("UM")

        # Check if a monochromator control task is already running before starting anything else
        if not self.cs260_is_busy():
            scan_task = asyncio.create_task(self.scan_series_async())
            # Register scan task as running
            self.coro_exec['scan_series'] = scan_task

    async def scan_series_async(self):
        """start_scan_series: Begin user programmed scan series

        :return: completion code
        """

        sequence_count = self.ui.series_config_files_tab1.count()
        scan_series = []
        for i in range(sequence_count):
            scan_series.append(self.ui.series_config_files_tab1.item(i))

        ##Run through each sequence in the series#####
        for seq in scan_series:
            seq_filter, seq_grating, seq_start_wave, seq_end_wave, seq_step_wave, seq_measure_int = \
                self.get_seq_from_item(seq)
            seq_step_wave = float(seq_step_wave) / 1000
            cur_filter = self.cs260.get_filter()
            cur_grating = self.cs260.get_grating()
            next_wave = seq_start_wave
            # Close shutter before changing grating and filter
            self.cs260.set_shutter("C")
            # Move grating to sequence specified position
            if seq_grating != cur_grating:
                grating_task = asyncio.create_task(self.cs260.set_grating(seq_grating))
                await grating_task

            # Move filter to sequence specified position
            if seq_filter != cur_filter:
                filter_task = asyncio.create_task(self.cs260.set_filter(seq_filter))
                await filter_task
            # Run through wave step sequence######################################
            while next_wave < seq_end_wave + seq_step_wave:
                self.cs260.set_shutter("C")
                wave_task = asyncio.create_task(self.cs260.set_wavelength(next_wave))
                await wave_task
                self.cs260.set_shutter("O")
                print(self.cs260.get_grating(), self.cs260.get_filter(), self.cs260.get_wavelength())
                await asyncio.sleep(seq_measure_int)
                next_wave = self.cs260.get_wavelength() + seq_step_wave
            ####################################################################
        ##############################################

        self.coro_exec['scan_series'] = None

    def abort_scan_series(self):
        pass

    def add_sequence(self):
        #pdb.set_trace()
        seq = ScanSequence()
        c = self.get_seq_values(seq)
        if c == 0:
            seq_item = QListWidgetItem()
            seq_item.setText(seq.name)
            seq_item.setData(SEQUENCE_ROLE, seq)
            self.ui.sequence_config_files_tab1.addItem(seq_item)
            self.ui.sequence_config_files_tab2.addItem(seq_item)
            self.ui.sequence_config_files_tab3.addItem(seq_item)

    def edit_sequence(self):
        if self.current_sequence is not None:
            prev_seq = self.current_sequence.data(SEQUENCE_ROLE)
            seq = prev_seq
            edit_code = self.get_seq_values(seq)
            if edit_code != 0:
                self.current_sequence = prev_seq
            else:
                self.current_sequence = seq
                self.ui.sequence_config_files_tab1.currentItem().setText(seq.name)
                self.ui.sequence_config_files_tab1.currentItem().setData(SEQUENCE_ROLE, seq)
                self.ui.sequence_config_files_tab2.currentItem().setText(seq.name)
                self.ui.sequence_config_files_tab2.currentItem().setData(SEQUENCE_ROLE, seq)
                self.ui.sequence_config_files_tab3.currentItem().setText(seq.name)
                self.ui.sequence_config_files_tab3.currentItem().setData(SEQUENCE_ROLE, seq)

        else:
            self.popup_dialog.disp_errors(["No sequence selected to edit!"])
            self.popup_dialog.popup()

    def remove_sequence(self):
        cur_row_tab1 = self.ui.series_config_files_tab1.currentRow()
        #cur_row_tab2 = self.ui.sequence_config_files_tab2.currentRow()
        #cur_row_tab3 = self.ui.sequence_config_files_tab3.currentRow()
        self.ui.series_config_files_tab1.takeItem(cur_row_tab1)
        #self.ui.sequence_config_files_tab2.takeItem(cur_row_tab2)
        #self.ui.sequence_config_files_tab3.takeItem(cur_row_tab3)

    def update_current_sequence(self):
        cur_item_tab1 = self.ui.sequence_config_files_tab1.currentItem()
        if cur_item_tab1 is not self.current_sequence:
            self.current_sequence = cur_item_tab1
            cur_seq_data = self.current_sequence.data(SEQUENCE_ROLE)
            # Update display values:
            self.ui.grating_select_cbox_tab2.setCurrentIndex(cur_seq_data.grating - 1)
            self.ui.osf_select_cbox.setCurrentIndex(cur_seq_data.osf - 1)
            self.ui.sequence_wave_start_ledit.setText(str(cur_seq_data.start_wave))
            self.ui.sequence_wave_end_ledit.setText(str(cur_seq_data.end_wave))
            self.ui.sequence_wave_step_ledit.setText(str(cur_seq_data.step_wave))
            self.ui.sequence_measure_int_ledit.setText(str(cur_seq_data.measure_interval))
            self.ui.sequence_name_ledit.setText(cur_seq_data.name)

    def show_invalid_seq_popup(self, error_list):
        error_list = ["Invalid scan sequence will not be added to the series.",
                      "Fix the following errors:"] + error_list
        self.popup_dialog.disp_errors(error_list)
        self.popup_dialog.popup()

    @staticmethod
    def get_seq_from_item(item):
        seq_data = item.data(SEQUENCE_ROLE)
        seq_filter = seq_data.osf
        seq_grating = seq_data.grating
        seq_start_wave = seq_data.start_wave
        seq_end_wave = seq_data.end_wave
        seq_step_wave = seq_data.step_wave
        seq_measure_int = seq_data.measure_interval
        return [seq_filter, seq_grating, seq_start_wave, seq_end_wave, seq_step_wave, seq_measure_int]

    def get_seq_values(self, seq):

        errors = []
        warnings = []
        seq.name = self.ui.sequence_name_ledit.text()
        if seq.name == "":
            errors.append("Sequence Name left blank")
        # Grabbing value from cbox so no check needed yet.
        seq.grating = self.ui.grating_select_cbox_tab2.currentIndex() + 1
        # Grabbing value from cbox so no check needed yet.
        seq.osf = self.ui.osf_select_cbox.currentIndex() + 1

        try:
            seq.start_wave = float(self.ui.sequence_wave_start_ledit.text())
        except ValueError as e:
            errors.append("Invalid start wave arg: {}".format(e))
        # else: check input against valid wavelength range for grating and filters

        try:
            seq.end_wave = float(self.ui.sequence_wave_end_ledit.text())
        except ValueError as e:
            errors.append("Invalid end wave arg: {}".format(e))
        # else: check input against valid wavelength range for grating and filters

        try:
            seq.step_wave = float(self.ui.sequence_wave_step_ledit.text())
        except ValueError as e:
            errors.append("Invalid wave step arg: {}".format(e))
        # else: check input against grating step resolution

        try:
            seq.measure_interval = float(self.ui.sequence_measure_int_ledit.text())
        except ValueError as e:
            errors.append("Invalid measure interval arg: {}".format(e))
        else:
            if seq.measure_interval < 0.5:
                warnings.append("Small Measure Interval provided. Monochromator wavelength drive may not step as fast "
                                "as the specified interval demands.")

        if len(errors) > 0:
            ret = -1
            self.show_invalid_seq_popup(errors)
        else:
            ret = 0

        return ret
    ###################################################################################################################


if __name__ == "__main__":
    # Create cs260 control instance
    exe_path = "..\\..\\..\\pylablib\\instruments\\CS260-Drivers\\C++EXE.exe"
    #cs = CS260(exe_path)

    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    window = masterWindow()#cs)
    window.show()
    with loop:
        loop.run_forever()
        loop.close()
    cs.close()
    sys.exit(app.exec_())
