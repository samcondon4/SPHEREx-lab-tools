"""automationWindowDialogWrapper:

    This module provides a wrapper class, AutomationWindow, around the automationWindowDialog2 that was generated with
    QT-Designer. AutomationWindow follows the SXTC-SWS GUI Tab API format.

Sam Condon, 06/21/2021
"""
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

# add package root directory to search path
sys.path.append("..\\..\\..\\")
from pylablib.utils.parameters import get_params_dict, write_config_file
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.AutomationWindow.automationWindowDialog import Ui_Form
from pylabcal.pylabcalgui.AutomationWindow.QListWigetSubclass import QListWidgetItemCustom

# CONSTANTS ################################
QtUNCHECKED = QtCore.Qt.Unchecked
QtCHECKED = QtCore.Qt.Checked
QtFULL_MATCH = QtCore.Qt.MatchExactly
SEQUENCE_ROLE = 0
###########################################


class AutomationWindow(Ui_Form, GuiTab):

    def __init__(self, seq_config_path="pylabcal\\config\\sequence\\", default_seq_name="default_seq"):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.is_stacked_widget = True
        super().__init__(self)

        # Configuration paths######################################################################
        self.default_seq_name = default_seq_name
        self.seq_config_path = seq_config_path
        ##########################################################################################

        # Configure Parameters #####################################################################################
        self.add_parameter('Sequence Info', self.get_sequence_info, self.set_sequence_info)
        self.add_parameter('Data Configuration', self.get_data_configuration, self.set_data_configuration)
        self.add_parameter('Metadata Configuration', self.get_metadata_configuration, self.set_metadata_configuration)
        self.add_parameter('Monochromator', self.get_monochromator_parameters, self.set_monochromator_parameters)
        self.add_parameter('Lock-In', self.get_lockin_parameters, self.set_lockin_parameters)
        # Note that the series parameter is not saved to sequence files
        self.add_parameter('Series', self.get_series, self.set_series)

        self.series_seq_list = {}
        #############################################################################################################

        # Connect user input to functions##############################################################################
        self.auto_series_sequence_save_button.clicked.connect(self._on_Save_New_Sequence)
        self.auto_series_addsequencestoseries_button.clicked.connect(self._on_Add_Sequence_To_series)
        self.auto_series_removesequencefromseries_button.clicked.connect(self._on_Remove_Sequence_From_series)
        self.auto_series_removeallsequencesfromseries_button.clicked.connect(self._on_Remove_All_Sequences_From_series)
        self.auto_control_runseries_button.clicked.connect(self._on_Run_series)
        self.auto_control_pauseseries_button.clicked.connect(self._on_Pause_series)
        self.auto_control_abortseries_button.clicked.connect(self._on_Abort_series)

        self.auto_series_savedsequences_list.currentItemChanged.connect(self._on_Sequence_Select)
        self.auto_series_series_list.currentItemChanged.connect(self._on_Series_Sequence_Select)
        ###############################################################################################################

        # Load saved sequence files and default sequence parameters###################################################
        for seq_file in os.listdir(self.seq_config_path):
            if seq_file.endswith(".ini"):
                seq_file_name = seq_file.split('.')[0]
                seq_file_data = get_params_dict(self.seq_config_path + seq_file)
                self.add_list_item("savedsequences", seq_file_name, seq_file_data)

        default_seq_dict = get_params_dict(self.seq_config_path + self.default_seq_name + ".ini")
        self.set_parameters(default_seq_dict)
        default_seq_item = self.auto_series_savedsequences_list.findItems(self.default_seq_name, QtCore.Qt.MatchExactly)
        self.auto_series_savedsequences_list.setCurrentItem(default_seq_item[0])
        ##############################################################################################################

    # PARAMETER GETTERS/SETTERS########################################################################################
    def get_sequence_info(self):

        params = {
            'sequence name': self.auto_series_sequence_name_ledit.text()
        }

        return params

    def set_sequence_info(self, params_dict):
        for key in params_dict:
            if key == "sequence name":
                self.auto_series_sequence_name_ledit.setText(params_dict[key])

    def get_data_configuration(self):
        params = {
            'storage path': self.auto_data_storagepath_ledit.text()
        }

        return params

    def set_data_configuration(self, params_dict):
        for key in params_dict:
            if key == "storage path":
                self.auto_data_storagepath_ledit.setText(params_dict[key])

    def get_metadata_configuration(self):
        params = {
            'wavelength': str(self.auto_data_metadata_wavelength_cbox.isChecked()),
            'grating': str(self.data_configuration_metadata_grating_cbox.isChecked()),
            'order sort filter': str(self.auto_data_metadata_osf_cbox.isChecked()),
            'shutter': str(self.data_configuration_metadata_shutter_cbox.isChecked()),
            'lock-in sample frequency': str(self.auto_data_metadata_lockinfs_cbox.isChecked()),
            'lock-in sample time': str(self.data_configuration_metadata_lockints_cbox.isChecked()),
            'lock-in time constant': str(self.auto_data_metadata_lockintimeconstant_cbox.isChecked()),
            'lock-in sensitivity': str(self.data_configuration_metadata_lockin_sensitivity_cbox.isChecked())
        }

        return params

    def set_metadata_configuration(self, params_dict):

        for key in params_dict:
            if params_dict[key] == "True":
                check_state = QtCHECKED
            else:
                check_state = QtUNCHECKED

            if key == "wavelength":
                self.auto_data_metadata_wavelength_cbox.setCheckState(check_state)
            elif key == "grating":
                self.data_configuration_metadata_grating_cbox.setCheckState(check_state)
            elif key == "order sort filter":
                self.auto_data_metadata_osf_cbox.setCheckState(check_state)
            elif key == "shutter":
                self.data_configuration_metadata_shutter_cbox.setCheckState(check_state)
            elif key == "lock-in sample frequency":
                self.auto_data_metadata_lockinfs_cbox.setCheckState(check_state)
            elif key == "lock-in sample time":
                self.data_configuration_metadata_lockints_cbox.setCheckState(check_state)
            elif key == "lock-in time constant":
                self.auto_data_metadata_lockintimeconstant_cbox.setCheckState(check_state)
            elif key == "lock-in sensitivity":
                self.data_configuration_metadata_lockin_sensitivity_cbox.setCheckState(check_state)

    def get_monochromator_parameters(self):
        params = {
            'start wavelength': self.sequence_monochromator_startwave_ledit.text(),
            'stop wavelength': self.sequence_monochromator_endwave_ledit.text(),
            'step size': self.sequence_monochromator_stepsize_ledit.text(),
            'shutter': self.sequence_monochromator_shutter_combobox.currentText(),
            'g1 to g2 transition wavelength': self.sequence_monochromator_g1g2_ledit.text(),
            'g2 to g3 transition wavelength': self.sequence_monochromator_g2g3_ledit.text(),
            'no osf to osf1 transition wavelength': self.sequence_monochromator_noosfosf1_ledit.text(),
            'osf1 to osf2 transition wavelength': self.sequence_monochromator_osf1osf2_ledit.text(),
            'osf2 to osf3 transition wavelength': self.sequence_monochromator_osf2osf3_ledit.text()
        }

        return params

    def set_monochromator_parameters(self, params_dict):
        for key in params_dict:
            value = params_dict[key]
            if key == "start wavelength":
                self.sequence_monochromator_startwave_ledit.setText(value)
            elif key == "stop wavelength":
                self.sequence_monochromator_endwave_ledit.setText(value)
            elif key == "step size":
                self.sequence_monochromator_stepsize_ledit.setText(value)
            elif key == "shutter":
                self.sequence_monochromator_shutter_combobox.setCurrentText(value)
            elif key == "g1 to g2 transition wavelength":
                self.sequence_monochromator_g1g2_ledit.setText(value)
            elif key == "g2 to g3 transition wavelength":
                self.sequence_monochromator_g2g3_ledit.setText(value)
            elif key == "no osf to osf1 transition wavelength":
                self.sequence_monochromator_noosfosf1_ledit.setText(value)
            elif key == "osf1 to osf2 transition wavelength":
                self.sequence_monochromator_osf1osf2_ledit.setText(value)
            elif key == "osf2 to osf3 transition wavelength":
                self.sequence_monochromator_osf2osf3_ledit.setText(value)

    def get_lockin_parameters(self):
        params = {
                    'sample frequency': self.sequence_lockin_samplerate_combobox.currentText(),
                    'sample time': self.sequence_lockin_sampletime_ledit.text(),
                    'time constant': self.sequence_lockin_timeconstant_ledit.text(),
                    'sensitivity string': self.sequence_lockin_sensitivity_ledit.text()
                 }

        return params

    def set_lockin_parameters(self, params_dict):
        for key in params_dict:
            value = params_dict[key]
            if key == "sample frequency":
                self.sequence_lockin_samplerate_combobox.setCurrentText(value)
            elif key == "sample time":
                self.sequence_lockin_sampletime_ledit.setText(value)
            elif key == "time constant":
                self.sequence_lockin_timeconstant_ledit.setText(value)
            elif key == "sensitivity string":
                self.sequence_lockin_sensitivity_ledit.setText(value)

    def get_series(self):
        seq_params_list = [0 for i in range(len(self.series_seq_list))]
        #iterator
        i = 0
        for seq_name in self.series_seq_list:
            seq_item = self.auto_series_series_list.findItems(seq_name, QtFULL_MATCH)[0]
            self.auto_series_series_list.setCurrentItem(seq_item)
            seq_params_list[i] = self.get_parameters(["Sequence Info", "Data Configuration", "Metadata Configuration",
                                                      "Monochromator", "Lock-In"])
            i += 1

        return seq_params_list

    def set_series(self, params_dict):
        pass
    ###################################################################################################################

    ##PRIVATE METHODS##################################################################################################
    #Start list methods################################################################
    def add_list_item(self, list_str, item_text, item_data):
        """add_list_item: add an item to the specified list

        :param list: string specifying which list the item should be added to
        :param item_text: item text string
        :param item_data: item data dictionary
        :return: None
        """
        seq_item = QListWidgetItemCustom()
        seq_item.setData(SEQUENCE_ROLE, item_text)
        seq_item.setText(item_text)
        seq_item.set_user_data(item_data)
        if list_str == "savedsequences":
            self.auto_series_savedsequences_list.addItem(seq_item)
        elif list_str == "series":
            self.auto_series_series_list.addItem(seq_item)

    def remove_list_item(self, item_dict):
        """remove_list_item: remove an item from the specified list

        :param

        :return:
        """
        pass

    def clear_list(self):
        pass
    #End list methods###############################################################################

    #Start button methods##########################################################################
    def _on_Save_New_Sequence(self):
        """on_Save_New_Sequence: add save new sequence button identifier to button queue
        """
        sequence_params = self.get_parameters(["Sequence Info", "Data Configuration", "Metadata Configuration",
                                                      "Monochromator", "Lock-In"])
        seq_name = sequence_params['Sequence Info']['sequence name']
        seq_item = QListWidgetItemCustom()
        seq_item.setData(SEQUENCE_ROLE, seq_name)
        seq_item.setText(seq_name)
        seq_item.set_user_data(sequence_params)
        write_config_file(sequence_params, self.seq_config_path + seq_name + ".ini")
        self.auto_series_savedsequences_list.addItem(seq_item)

    def _on_Add_Sequence_To_series(self):
        """on_Save_New_Sequence: add save new sequence button identifier to button queue
        """
        seq_item = self.auto_series_savedsequences_list.currentItem()
        self.series_seq_list[seq_item.text()] = seq_item.text()
        self.add_list_item("series", seq_item.text(), seq_item.user_data)

    def _on_Remove_Sequence_From_series(self):
        """on_Save_New_Sequence: add save new sequence button identifier to button queue
        """
        rem_seq = self.auto_series_series_list.currentItem()
        if rem_seq is not None:
            self.series_seq_list.pop(rem_seq.text())
            self.auto_series_series_list.currentItemChanged.disconnect(self._on_Series_Sequence_Select)
            self.auto_series_series_list.takeItem(self.auto_series_series_list.currentRow())
            self.auto_series_series_list.currentItemChanged.connect(self._on_Series_Sequence_Select)

    def _on_Remove_All_Sequences_From_series(self):
        """on_Save_New_Sequence: add save new sequence button identifier to button queue
        """
        self.auto_series_series_list.currentItemChanged.disconnect(self._on_Series_Sequence_Select)
        self.auto_series_series_list.clear()
        self.series_seq_list = {}
        self.auto_series_series_list.currentItemChanged.connect(self._on_Series_Sequence_Select)

    def _on_Run_series(self):
        """on_Save_New_Sequence: add save new sequence button identifier to button queue
        """
        self.button_queue.put("Run Series")

    def _on_Pause_series(self):
        """on_Save_New_Sequence: add save new sequence button identifier to button queue
        """

        self.button_queue.put("Pause Series")

    def _on_Abort_series(self):
        """on_Save_New_Sequence: add save new sequence button identifier to button queue
        """

        self.button_queue.put("Abort Series")

    def _on_Sequence_Select(self):
        """_on_Sequence_Select: update display with parameters specified by currently selected sequence in saved sequences
                                list.

        :return: None
        """
        seq_item = self.auto_series_savedsequences_list.currentItem()
        self.set_parameters(seq_item.user_data)

    def _on_Series_Sequence_Select(self):
        """_on_Series_Sequence_Select: update display with parameters specified by currently selected sequence in
                                       series list.

        :return: None
        """
        seq_item = self.auto_series_series_list.currentItem()
        self.set_parameters(seq_item.user_data)

    def _on_Switch_Window_0(self):
        """_on_Switch_Window_0: switch from the Series Construction and Control Window to the Sequence Parameters
                                window.
        """
        self.auto_window_select_combobox_1.setCurrentIndex(self.auto_window_select_combobox_0.currentIndex())
        self.automation_window.setCurrentIndex(self.auto_window_select_combobox_0.currentIndex())

    def _on_Switch_Window_1(self):
        """_on_Switch_Window_1: switch from the Sequence Parameters Window to the Series Construction and Control
                                Window.
        """
        self.auto_window_select_combobox_0.setCurrentIndex(self.auto_window_select_combobox_1.currentIndex())
        self.automation_window.setCurrentIndex(self.auto_window_select_combobox_1.currentIndex())
    #End button methods###########################################################################################
    #END PRIVATE METHODS################################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AutomationWindow()
    window.form.show()
    sys.exit(app.exec_())
