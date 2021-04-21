import sys
from qasync import QEventLoop
import asyncio
from PyQt5.QtWidgets import *
#UI files
from cs260_dialog_ui import *
from cs260_dialog_error import *
#Function files
from cs260_dialog_manualtab import *
from cs260_dialog_scantab import *

sys.path.append("..\\..\\..\\pylablib\\instruments")
from CS260 import *

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


class CS260Window(QDialog):
    """
    CS260 dialog class.
    """
    def __init__(self, cs260_obj):
        super().__init__()

        ##Class attributes###############################
        #cs260 monochromator class instance
        self.cs260 = cs260_obj
        self.current_sequence = None
        #################################################

        ##Set up main UI dialog############################################################
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        ##Scan tab buttons#######################################################
        self.ui.add_new_sequence_button.clicked.connect(self.add_sequence)
        self.ui.edit_sequence_button.clicked.connect(self.edit_sequence)
        self.ui.remove_sequence_button.clicked.connect(self.remove_sequence)
        self.ui.series.clicked.connect(self.update_current_sequence)
        self.ui.start_scan_series_button.clicked.connect(self.start_scan_series)
        #########################################################################

        ##Manual tab buttons#####################################################

        #########################################################################

        ####################################################################################

        ##Set up invalid scan sequence dialog#######################################
        self.error_dialog = Cs260ErrorDialog()
        ############################################################################

    def start_scan_series(self):
        if self.cs260.get_units() != "UM":
            self.cs260.set_units("UM")
        asyncio.ensure_future(self.scan_series_async())

    async def scan_series_async(self):
        """start_scan_series: Begin user programmed scan series

        :return: completion code
        """

        sequence_count = self.ui.series.count()
        scan_series = []
        for i in range(sequence_count):
            scan_series.append(self.ui.series.item(i))

        ##Run through each sequence in the series#####
        for seq in scan_series:
            seq_filter, seq_grating, seq_start_wave, seq_end_wave, seq_step_wave, seq_measure_int = \
                                                                                self.get_seq_from_item(seq)
            seq_step_wave = float(seq_step_wave) / 1000
            cur_filter = self.cs260.get_filter()
            cur_grating = self.cs260.get_grating()
            next_wave = seq_start_wave
            #Close shutter before changing grating and filter
            self.cs260.set_shutter("C")
            #Move grating to sequence specified position
            if seq_grating != cur_grating:
                grating_task = asyncio.create_task(self.cs260.set_grating(seq_grating))
                await grating_task
            #Move filter to sequence specified position
            if seq_filter != cur_filter:
                filter_task = asyncio.create_task(self.cs260.set_filter(seq_filter))
                await filter_task
            #Run through wave step sequence######################################
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

    def abort_scan_series(self):
        pass

    def add_sequence(self):
        seq = ScanSequence()
        c = self.get_seq_values(seq)
        if c == 0:
            seq_item = QListWidgetItem()
            seq_item.setText(seq.name)
            seq_item.setData(SEQUENCE_ROLE, seq)
            self.ui.series.addItem(seq_item)
        
    def edit_sequence(self):
        if self.current_sequence is not None:
            prev_seq = self.current_sequence.data(SEQUENCE_ROLE)
            seq = prev_seq
            edit_code = self.get_seq_values(seq)
            if edit_code != 0:
                self.current_sequence = prev_seq
            else:
                self.current_sequence = seq
                self.ui.series.currentItem().setText(seq.name)
                self.ui.series.currentItem().setData(SEQUENCE_ROLE, seq)

        else:
            self.error_dialog.disp_errors(["No sequence selected to edit!"])
            self.error_dialog.dialog.exec_()

    def remove_sequence(self):
        cur_row = self.ui.series.currentRow()
        self.ui.series.takeItem(cur_row)

    def update_current_sequence(self):
        cur_item = self.ui.series.currentItem()
        if cur_item is not self.current_sequence:
            self.current_sequence = cur_item
            cur_seq_data = self.current_sequence.data(SEQUENCE_ROLE)
            #Update display values:
            self.ui.grating_select_cbox.setCurrentIndex(cur_seq_data.grating - 1)
            self.ui.osf_select_cbox.setCurrentIndex(cur_seq_data.osf - 1)
            self.ui.sequence_wave_start_ledit.setText(str(cur_seq_data.start_wave))
            self.ui.sequence_wave_end_ledit.setText(str(cur_seq_data.end_wave))
            self.ui.sequence_wave_step_ledit.setText(str(cur_seq_data.step_wave))
            self.ui.sequence_measure_int_ledit.setText(str(cur_seq_data.measure_interval))
            self.ui.sequence_name_ledit.setText(cur_seq_data.name)

    def show_invalid_seq_popup(self, error_list):
        error_list = ["Invalid scan sequence will not be added to the series.", "Fix the following errors:"] + error_list
        self.error_dialog.disp_errors(error_list)
        self.error_dialog.dialog.exec_()

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
        seq.grating = self.ui.grating_select_cbox.currentIndex() + 1
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


if __name__ == "__main__":
    #Create cs260 control instance
    exe_path = "..\\..\\..\\pylablib\\instruments\\CS260-Drivers\\C++EXE.exe"
    cs = CS260(exe_path)

    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    window = CS260Window(cs)
    window.show()
    with loop:
        loop.run_forever()
        loop.close()
    cs.close()
    sys.exit(app.exec_())
