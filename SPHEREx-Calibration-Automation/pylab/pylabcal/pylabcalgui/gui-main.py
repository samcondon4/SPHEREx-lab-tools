import sys
from PyQt5.QtWidgets import QDialog, QApplication
from cs260dialogv2 import *


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
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.add_new_sequence_button.clicked.connect(self.add_sequence)
        self.ui.edit_sequence_button.clicked.connect(self.edit_sequence)
        self.ui.remove_sequence_button.clicked.connect(self.remove_sequence)

    def add_sequence(self):
        seq = ScanSequence()
        seq.name = self.ui.sequence_name_ledit.text()
        #seq.grating = self.ui.grating_select_cbox.currentIndex() + 1
        #seq.osf = self.ui.osf_select_cbox() + 1
        #seq.start_wave = float(self.ui.sequence_wave_start_ledit.text())
        #seq.end_wave = float(self.ui.sequence_wave_end_ledit.text())
        #seq.step_wave = float(self.ui.sequence_wave_step_ledit.text())
        #seq.measure_interval = float(self.ui.sequence_measure_int_ledit.text())
        self.ui.series_list.addItem(seq.name)

    def edit_sequence(self):
        self.ui.series_list.currentItem().setText("Edit")

    def remove_sequence(self):
        cur_row = self.ui.series_list.currentRow()
        self.ui.series_list.takeItem(cur_row)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CS260Window()
    window.show()
    sys.exit(app.exec_())
