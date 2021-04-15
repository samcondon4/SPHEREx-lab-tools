import sys
from PyQt5.QtWidgets import *
from cs260dialog import *
from cs260_invalid_scansequence_dialog import *


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
    def __init__(self):
        super().__init__()

        ##Set up main UI dialog#####################################################
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.add_new_sequence_button.clicked.connect(self.add_sequence)
        self.ui.edit_sequence_button.clicked.connect(self.edit_sequence)
        self.ui.remove_sequence_button.clicked.connect(self.remove_sequence)
        ############################################################################

        ##Set up invalid scan sequence dialog#######################################
        self.invalid_scan_sequence_dialog = InvalidScanSequenceDialog()
        ############################################################################
 		

    def add_sequence(self):
        seq = ScanSequence()
        errors = []
        warnings = []
        seq.name = self.ui.sequence_name_ledit.text()
        if seq.name == "":
            errors.append("Sequence Name left blank")
        #Grabbing value from cbox so no check needed yet.
        seq.grating = self.ui.grating_select_cbox.currentIndex() + 1
        #Grabbing value from cbox so no check needed yet.
        seq.osf = self.ui.osf_select_cbox.currentIndex() + 1
        
        try:
            seq.start_wave = float(self.ui.sequence_wave_start_ledit.text())
        except ValueError as e:
            errors.append("Invalid start wave arg: {}".format(e))
        #else: check input against valid wavelength range for grating and filters

        try:
            seq.end_wave = float(self.ui.sequence_wave_end_ledit.text())    
        except ValueError as e:
            errors.append("Invalid end wave arg: {}".format(e))
        #else: check input against valid wavelength range for grating and filters

        try:
            seq.step_wave = float(self.ui.sequence_wave_step_ledit.text())
        except ValueError as e:
            errors.append("Invalid wave step arg: {}".format(e))
        #else: check input against grating step resolution    

        try:
            seq.measure_interval = float(self.ui.sequence_measure_int_ledit.text())
        except ValueError as e:
            errors.append("Invalid measure interval arg: {}".format(e))
        else:
            if seq.measure_interval < 0.5:
                warnings.append("Small Measure Interval provided. Monochromator wavelength drive may not step as fast as the specified interval demands.")
        
        if len(errors) > 0:
        	self.show_invalid_seq_popup(errors)
        else:
        	self.ui.series_list.addItem(seq.name)
        

    def edit_sequence(self):
        self.ui.series_list.currentItem().setText("Edit")

    def remove_sequence(self):
        cur_row = self.ui.series_list.currentRow()
        self.ui.series_list.takeItem(cur_row)

    def show_invalid_seq_popup(self, error_list):
    	self.invalid_scan_sequence_dialog.disp_errors(error_list)
    	self.invalid_scan_sequence_dialog.dialog.exec_()
    	


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CS260Window()
    window.show()
    sys.exit(app.exec_())
