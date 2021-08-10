"""lockinAutoWindowDialogWrapper:

    This module provides a wrapper class, LockinAutoWindow, around the lockinAutoWindowDialog class created using
    QT-Designer.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.LockinWindow.lockinAutoWindowDialog import Ui_Form
from pylabcal.pylabcalgui.LockinWindow.lockin_window_helpers import *
from pylablib.QListWigetSubclass import QListWidgetItemCustom


class LockinAutoWindow(Ui_Form, GuiTab):

    def __init__(self, button_queue_keys=None):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        super().__init__(self, button_queue_keys=button_queue_keys)

        # Configure Parameters ################################################################################
        self.add_parameter("sr510 sample frequency", self.get_sr510_fs, self.set_sr510_fs)
        self.add_parameter("sr510 time constant", self.get_sr510_tc, self.set_sr510_tc)
        self.add_parameter("sr510 sensitivity transition list", self.get_sr510_transition_list,
                           self.set_sr510_transition_list)
        #self.add_parameter("SR510 Sensitivity Transition Wavelength", self.get_sr510_transition_wavelength,
        #                   self.set_sr510_transition_wavelength)
        self.add_parameter("sr510 sensitivity", self.get_sr510_sensitivity, self.set_sr510_sensitivity)
        self.add_parameter("sr830 sample frequency", self.get_sr830_fs, self.set_sr830_fs)
        self.add_parameter("sr830 time constant", self.get_sr830_tc, self.set_sr830_tc)
        self.add_parameter("sr830 sensitivity transition list", self.get_sr830_transition_list,
                           self.set_sr830_transition_list)
        #self.add_parameter("SR830 Sensitivity Transition Wavelength", self.get_sr830_transition_wavelength,
        #                   self.set_sr830_transition_wavelength)
        self.add_parameter("sr830 sensitivity", self.get_sr830_sensitivity, self.set_sr830_sensitivity)
        ########################################################################################################

        # Configure button methods #####################################################################################
        self.sequence_sr510_senstransition_add_button.clicked.connect(self._on_add_sr510_sens_transition)
        self.sequence_sr510_senstransition_remove_button.clicked.connect(self._on_remove_sr510_sens_transition)
        self.sequence_sr510_senstransition_removeall_button.clicked.connect(self._on_remove_all_sr510_sens_transitions)
        self.sequence_sr830_senstransition_add_button.clicked.connect(self._on_add_sr830_sens_transition)
        self.sequence_sr830_sens_transition_remove_button.clicked.connect(self._on_remove_sr830_sens_transition)
        self.sequence_sr830_sens_transition_removeall_button.clicked.connect(self._on_remove_all_sr830_sens_transitions)
        ################################################################################################################

    # PARAMETER GETTER/SETTERS #######################################################################
    def get_sr510_fs(self):
        """get_sr510_fs: get the sample rate for the sr510 lockin
        """
        return float(self.sequence_sr510_samplerate_combobox.currentText())

    def set_sr510_fs(self, fs):
        """set_sr510_fs: set the sample rate for the sr510 lockin
        """
        if type(fs) is str:
            fs = float(fs)
            if fs >= 1.0:
                fs = int(fs)
        if fs in LOCKIN_FS:
            self.sequence_sr510_samplerate_combobox.setCurrentText(str(fs))
        else:
            raise ValueError("Sample frequency must be one of the following values: {}!".format(LOCKIN_FS))

    def get_sr510_tc(self):
        """get_sr510_tc: return the time constant value and string for the sr510
        """
        tc_value = float(self.sequence_sr510_timeconstant_value_cbox.currentText())
        tc_multiplier = float(self.sequence_sr510_timeconstant_multiplier_cbox.currentText().split('x')[1:][0])
        tc_units = self.sequence_sr510_timeconstant_units_cbox.currentText()
        tc_unit_multiplier = LOCKIN_UNIT_TC_MAP[tc_units]
        tc = tc_value*tc_multiplier*tc_unit_multiplier

        return tc

    def set_sr510_tc(self, tc):
        """set_sr510_tc: set the sr510 display time-constant combo boxes
        """

        if type(tc) is str:
            tc = float(tc)

        tc_mod = tc % 3
        tc_value = tc_mod + LOCKIN_TC_MOD_MAP[tc_mod]
        tc_mult, tc_units = LOCKIN_TC_MULT_UNIT_MAP[tc/tc_value]
        self.sequence_sr510_timeconstant_value_cbox.setCurrentText(str(tc_value))
        self.sequence_sr510_timeconstant_multiplier_cbox.setCurrentText(tc_mult)
        self.sequence_sr510_timeconstant_units_cbox.setCurrentText(tc_units)

    def get_sr510_transition_list(self):
        """get_sr510_transition_list: get the sr510 transition list text and data.
        """
        item_count = self.sequence_sr510_senstransitions_list.count()
        transition_list_str = ""
        for i in range(item_count):
            self.sequence_sr510_senstransitions_list.setCurrentRow(i)
            item = self.sequence_sr510_senstransitions_list.currentItem()
            item_str = item.text().replace("; ", ",")
            if transition_list_str == "":
                transition_list_str += item_str
            else:
                transition_list_str += item_str.replace("W", ";W")
        return transition_list_str

    def set_sr510_transition_list(self, transition_list):
        """set_sr510_transition_list: set the sr510 transition list text and data.
        """
        self.sequence_sr510_senstransitions_list.clear()
        transition_list = transition_list.split(";")
        for trans in transition_list:
            trans_text = trans.replace(",", "; ")
            GuiTab.add_item_to_list(self.sequence_sr510_senstransitions_list, trans_text, "")

    def get_sr510_transition_wavelength(self):
        """get_sr510_transition_wavelength: get the wavelength entry for a new sr510 sensitivity transition.
        """
        return float(self.sequence_sr510_wave_ledit.text())

    def set_sr510_transition_wavelength(self, wave):
        """set_sr510_transition_wavelength: set the wavelength entry for a new sr510 sensitivity transition.
        """
        self.sequence_sr510_wave_ledit.setText(wave)

    def get_sr510_sensitivity(self):
        """get_sr510_sensitivity: get the sensitivity entry for a new sr510 sensitivity transition.
        """
        sens_value = float(self.sequence_sr510_sensitivity_value_cbox.currentText())
        sens_multiplier = float(self.sequence_sr510_sensitivity_multiplier_cbox.currentText().split('x')[1])
        sens_units = self.sequence_sr510_sensitivity_units_cbox.currentText()
        sens_unit_multiplier = LOCKIN_UNIT_SENSITIVITY_MAP[sens_units]
        sens = sens_value*sens_multiplier*sens_unit_multiplier

        return {"value": sens, "string": "{} {}".format(sens_value*sens_multiplier, sens_units)}

    def set_sr510_sensitivity(self, sens):
        """set_sr510_sensitivity: set the sensitivity entry for a new sr510 sensitivity transition.
        """
        sens_value = LOCKIN_SENS_MOD_MAP[sens % 5]
        sens_multiplier, sens_units = LOCKIN_SENS_MULT_UNIT_MAP[sens/sens_value]
        self.sequence_sr510_sensitivity_value_cbox.setCurrentText(sens_value)
        self.sequence_sr510_sensitivity_multiplier_cbox.setCurrentText(sens_multiplier)
        self.sequence_sr510_sensitivity_units_cbox.setCurrentText(sens_units)

    def get_sr830_fs(self):
        """get_sr830_fs: get the sample rate for the sr830 lockin
        """
        return float(self.sequence_sr830_samplerate_combobox.currentText())

    def set_sr830_fs(self, fs):
        """set_sr830_fs: set the sample rate for the sr830 lockin
        """
        if type(fs) is str:
            fs = float(fs)
            if fs >= 1.0:
                fs = int(fs)
        if fs in LOCKIN_FS:
            self.sequence_sr830_samplerate_combobox.setCurrentText(str(fs))
        else:
            raise ValueError("Sample frequency must be one of the following values: {}!".format(LOCKIN_FS))

    def get_sr830_tc(self):
        """get_sr830_tc: return the time constant value and string for the sr830
        """
        tc_value = float(self.sequence_sr830_timeconstant_value_cbox.currentText())
        tc_multiplier = float(self.sequence_sr830_timeconstant_multiplier_cbox.currentText().split('x')[1:][0])
        tc_units = self.sequence_sr830_timeconstant_units_cbox.currentText()
        tc_unit_multiplier = LOCKIN_UNIT_TC_MAP[tc_units]
        tc = tc_value*tc_multiplier*tc_unit_multiplier

        return tc

    def set_sr830_tc(self, tc):
        """set_sr830_tc: set the sr830 display time-constant combo boxes
        """
        if type(tc) is str:
            tc = float(tc)
        tc_mod = tc % 3
        tc_value = tc_mod + LOCKIN_TC_MOD_MAP[tc_mod]
        tc_mult, tc_units = LOCKIN_TC_MULT_UNIT_MAP[tc/tc_value]
        self.sequence_sr830_timeconstant_value_cbox.setCurrentText(str(tc_value))
        self.sequence_sr830_timeconstant_multiplier_cbox.setCurrentText(str(tc_mult))
        self.sequence_sr830_timeconstant_units_cbox.setCurrentText(str(tc_units))

    def get_sr830_transition_list(self):
        """get_sr830_transition_list: get the sr830 transition list text and data.
        """
        item_count = self.sequence_sr830_senstransitions_list.count()
        transition_list_str = ""
        for i in range(item_count):
            self.sequence_sr830_senstransitions_list.setCurrentRow(i)
            item = self.sequence_sr830_senstransitions_list.currentItem()
            item_str = item.text().replace("; ", ",")
            if transition_list_str == "":
                transition_list_str += item_str
            else:
                transition_list_str += item_str.replace("W", ";W")
        return transition_list_str

    def set_sr830_transition_list(self, transition_list):
        """set_sr830_transition_list: set the sr830 transition list text and data.
        """
        self.sequence_sr830_senstransitions_list.clear()
        transition_list = transition_list.split(";")
        for trans in transition_list:
            trans_text = trans.replace(",", "; ")
            GuiTab.add_item_to_list(self.sequence_sr830_senstransitions_list, trans_text, "")

    def get_sr830_transition_wavelength(self):
        """get_sr830_transition_wavelength: get the wavelength entry for a new sr830 sensitivity transition.
        """
        return float(self.sequence_sr830_wave_ledit.text())

    def set_sr830_transition_wavelength(self, wave):
        """set_sr830_transition_wavelength: set the wavelength entry for a new sr830 sensitivity transition.
        """
        self.sequence_sr830_wave_ledit.setText(wave)

    def get_sr830_sensitivity(self):
        """get_sr830_sensitivity: get the sensitivity entry for a new sr830 sensitivity transition.
        """
        sens_value = float(self.sequence_sr830_sensitivity_value_cbox.currentText())
        sens_multiplier = float(self.sequence_sr830_sensitivity_multiplier_cbox.currentText().split('x')[1])
        sens_units = self.sequence_sr830_sensitivity_units_cbox.currentText()
        sens_unit_multiplier = LOCKIN_UNIT_SENSITIVITY_MAP[sens_units]
        sens = sens_value*sens_multiplier*sens_unit_multiplier

        return {"value": sens, "string": "{} {}".format(sens_value*sens_multiplier, sens_units)}

    def set_sr830_sensitivity(self, sens):
        """set_sr830_sensitivity: set the sensitivity entry for a new sr830 sensitivity transition.
        """

        sens_value = LOCKIN_SENS_MOD_MAP[sens % 5]
        sens_multiplier, sens_units = LOCKIN_SENS_MULT_UNIT_MAP[sens / sens_value]
        self.sequence_sr830_sensitivity_value_cbox.setCurrentText(sens_value)
        self.sequence_sr830_sensitivity_multiplier_cbox.setCurrentText(sens_multiplier)
        self.sequence_sr830_sensitivity_units_cbox.setCurrentText(sens_units)

    ####################################################################################################

    # PRIVATE METHODS #################################################################################################
    # Button methods #########################
    def _on_add_sr510_sens_transition(self):
        """_on_add_sr510_sens_transition: add a transition to the sr510 sensitivity transitions list
        """

        try:
            # Get sensitivity value for transition ################
            sens_value = float(self.sequence_sr510_sensitivity_value_cbox.currentText())
            sens_multiplier = float(self.sequence_sr510_sensitivity_multiplier_cbox.currentText().split('x')[1:][0])
            sens_units = self.sequence_sr510_sensitivity_units_cbox.currentText()
            sens_unit_multiplier = LOCKIN_UNIT_SENSITIVITY_MAP[sens_units]
            sens = sens_value*sens_multiplier*sens_unit_multiplier
            # Get wavelength value for transition #################
            wave = float(self.sequence_sr510_wave_ledit.text())
        except ValueError as e:
            print(e)
        else:
            transition_text = "Wavelength = {}; Sensitivity = {}{}".format(wave, sens_value*sens_multiplier, sens_units)
            transition_data = {"Wavelength": wave, "Sensitivity": sens}

            GuiTab.add_item_to_list(self.sequence_sr510_senstransitions_list, transition_text, transition_data)

    def _on_remove_sr510_sens_transition(self):
        """_on_remove_transition: remove a transition from the sr510 sensitivity transitions list
        """
        GuiTab.remove_item_from_list(self.sequence_sr510_senstransitions_list)

    def _on_remove_all_sr510_sens_transitions(self):
        """_on_remove_all_transitions: remove all transitions from the sr510 sensitivity transitions list
        """
        GuiTab.remove_all_items_from_list(self.sequence_sr510_senstransitions_list)

    def _on_add_sr830_sens_transition(self):
        """_on_add_sr830_sens_transition: add a transition to the sr830 sensitivity transitions list
        """
        try:
            # Get sensitivity value for transition ################
            sens_value = float(self.sequence_sr830_sensitivity_value_cbox.currentText())
            sens_multiplier = float(self.sequence_sr830_sensitivity_multiplier_cbox.currentText().split('x')[1:][0])
            sens_units = self.sequence_sr830_sensitivity_units_cbox.currentText()
            sens_unit_multiplier = LOCKIN_UNIT_SENSITIVITY_MAP[sens_units]
            sens = sens_value*sens_multiplier*sens_unit_multiplier
            # Get wavelength value for transition #################
            wave = float(self.sequence_sr830_wave_ledit.text())
        except ValueError as e:
            print(e)
        else:
            transition_text = "Wavelength = {}; Sensitivity = {}{}".format(wave, sens_value * sens_multiplier,
                                                                            sens_units)
            transition_data = {"Wavelength": wave, "Sensitivity": sens}
            GuiTab.add_item_to_list(self.sequence_sr830_senstransitions_list, transition_text, transition_data)

    def _on_remove_sr830_sens_transition(self):
        """_on_remove_transition: remove a transition from the sr830 sensitivity transitions list
        """
        GuiTab.remove_item_from_list(self.sequence_sr830_senstransitions_list)

    def _on_remove_all_sr830_sens_transitions(self):
        """_on_remove_all_transitions: remove all transitions from the sr830 sensitivity transitions list
        """
        GuiTab.remove_all_items_from_list(self.sequence_sr830_senstransitions_list)
    ###################################################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LockinAutoWindow()
    window.form.show()
    sys.exit(app.exec_())
