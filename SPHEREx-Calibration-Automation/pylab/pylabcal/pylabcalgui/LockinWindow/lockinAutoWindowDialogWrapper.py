"""lockinAutoWindowDialogWrapper:

    This module provides a wrapper class, LockinAutoWindow, around the lockinAutoWindowDialog class created using
    QT-Designer.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.LockinWindow.lockinAutoWindowDialog import Ui_Form
from pylablib.QListWigetSubclass import QListWidgetItemCustom

# CONSTANTS ################################
QtUNCHECKED = QtCore.Qt.Unchecked
QtCHECKED = QtCore.Qt.Checked
QtFULL_MATCH = QtCore.Qt.MatchExactly
SEQUENCE_ROLE = 0
###########################################


class LockinAutoWindow(Ui_Form, GuiTab):

    def __init__(self):
        super().__init__(self)
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)

        # Configure Parameters #######################################################################
        self.add_parameter("SR830", self.get_sr830_parameters, self.set_sr830_parameters)
        self.add_parameter("SR510", self.get_sr830_parameters, self.set_sr830_parameters)
        self.add_parameter("Sample Time", self.get_sampletime, self.set_sampletime)
        ##############################################################################################

        # Configure button methods #####################################################################################
        self.sequence_sr510_senstransition_add_button.clicked.connect(self._on_add_sr510_sens_transition)
        self.sequence_sr510_senstransition_remove_button.clicked.connect(self._on_remove_sr510_sens_transition)
        self.sequence_sr510_senstransition_removeall_button.clicked.connect(self._on_remove_all_sr510_sens_transitions)
        self.sequence_sr830_senstransition_add_button.clicked.connect(self._on_add_sr830_sens_transition)
        self.sequence_sr830_sens_transition_remove_button.clicked.connect(self._on_remove_sr830_sens_transition)
        self.sequence_sr830_sens_transition_removeall_button.clicked.connect(self._on_remove_all_sr830_sens_transitions)
        ################################################################################################################

    # PARAMETER GETTER/SETTERS #######################################################################
    def get_sr830_parameters(self):
        params = {
            'sample frequency': self.sequence_sr830_samplerate_combobox.currentText(),
            'time constant': self.sequence_sr830_timeconstant_ledit.text(),
            'sensitivity string': self.sequence_sr830_sensitivity_ledit.text()
        }

        return params

    def set_sr830_parameters(self, params_dict):
        for key in params_dict:
            value = params_dict[key]
            if key == "sample frequency":
                self.sequence_sr830_samplerate_combobox.setCurrentText(value)
            elif key == "time constant":
                self.sequence_sr830_timeconstant_ledit.setText(value)
            elif key == "sensitivity string":
                self.sequence_sr830_sensitivity_ledit.setText(value)

    def get_sr510_parameters(self):
        params = {
            'sample frequency': self.sequence_sr510_samplerate_combobox.currentText(),
            'time constant': self.sequence_sr510_timeconstant_ledit.text(),
            'sensitivity string': self.sequence_sr510_sensitivity_ledit.text()
        }

        return params

    def set_sr510_parameters(self, params_dict):
        for key in params_dict:
            value = params_dict[key]
            if key == "sample frequency":
                self.sequence_sr510_samplerate_combobox.setCurrentText(value)
            elif key == "time constant":
                self.sequence_sr510_timeconstant_ledit.setText(value)
            elif key == "sensitivity string":
                self.sequence_sr510_sensitivity_ledit.setText(value)

    def get_sampletime(self):
        return {"Sample Time": self.sequence_lockin_sampletime_ledit.text()}

    def set_sampletime(self, time):
        self.sequence_lockin_sampletime_ledit.setText(time)
    ####################################################################################################

    # PRIVATE METHODS ##################################################################################
    def _on_add_sr510_sens_transition(self):
        list_item = QListWidgetItemCustom()

        valid_input = True
        try:
            sens = int(self.sequence_sr510_sens_ledit.text())
        except ValueError as e:
            print(e)
            valid_input = False
        try:
            transition_wavelength = float(self.sequence_sr510_wave_ledit.text())
        except ValueError as e:
            print(e)
            valid_input = False

        if valid_input:
            item_data = {"Position": sens, "Wavelength": transition_wavelength}
            list_item.setData(SEQUENCE_ROLE, item_data)
            list_item.setText("Wavelength = {}:  NDF Position = {}".format(transition_wavelength, sens))
            list_item.set_user_data(item_data)

            self.sequence_sr510_senstransitions_list.addItem(list_item)

    def _on_remove_sr510_sens_transition(self):
        """_on_remove_transition: remove a transition from the sr510 sensitivity transitions list
        """
        GuiTab.remove_item_from_list(self.sequence_sr510_senstransitions_list)

    def _on_remove_all_sr510_sens_transitions(self):
        """_on_remove_all_transitions: remove all transitions from the sr510 sensitivity transitions list
        """
        GuiTab.remove_all_items_from_list(self.sequence_sr510_senstransitions_list)

    def _on_add_sr830_sens_transition(self):

        valid_input = True
        try:
            sens = int(self.sequence_sr830_sens_ledit.text())
        except ValueError as e:
            print(e)
            valid_input = False
        try:
            transition_wavelength = float(self.sequence_sr830_wave_ledit.text())
        except ValueError as e:
            print(e)
            valid_input = False

        if valid_input:
            item_data = {"Position": sens, "Wavelength": transition_wavelength}
            item_text = "Wavelength = {};  Sensitivity = {}".format(transition_wavelength, sens)
            GuiTab.add_item_to_list(self.sequence_sr830_senstransitions_list, item_text, item_data)

    def _on_remove_sr830_sens_transition(self):
        """_on_remove_transition: remove a transition from the ndf transitions list
        """
        rem_trans = self.sequence_sr830_senstransitions_list.currentItem()
        if rem_trans is not None:
            rem_row = self.sequence_sr830_senstransitions_list.currentRow()
            self.sequence_sr830_senstransitions_list.takeItem(rem_row)

    def _on_remove_all_sr830_sens_transitions(self):
        """_on_remove_all_transitions: remove all transitions from the ndf transitions list
        """
        self.sequence_sr830_senstransitions_list.clear()
    ####################################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LockinAutoWindow()
    window.form.show()
    sys.exit(app.exec_())
