"""seriesconstructionWindowDialogWrapper:

    This module provides a wrapper class, SeriesConstructionWindow, around the seriesconstructionWindowDialog class
    created using QT-Designer.

Sam Condon, 08/02/2021
"""
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.SeriesConstruction.seriesconstructionWindowDialog import Ui_Form
from pylablib.utils.parameters import get_params_dict, write_config_file
from pylablib.QListWigetSubclass import QListWidgetItemCustom

# CONSTANTS ################################
QtUNCHECKED = QtCore.Qt.Unchecked
QtCHECKED = QtCore.Qt.Checked
QtFULL_MATCH = QtCore.Qt.MatchExactly
SEQUENCE_ROLE = 0
###########################################


class SeriesConstructionWindow(Ui_Form, GuiTab):

    def __init__(self, root_path, seq_config_path="pylabcal\\config\\sequence\\", default_seq_name="default_seq",
                 button_queue_keys=None):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        super().__init__(self, button_queue_keys=button_queue_keys)

        # Configuration paths ###################################################################################
        self.default_seq_name = default_seq_name
        self.seq_config_path = seq_config_path
        self.root_path = root_path
        self.series_seq_list = {}
        #########################################################################################################

        # Configure parameters #######################################################################################
        self.add_parameter("Sequence Info", self.get_sequence_info, self.set_sequence_info)
        self.add_parameter("Data Configuration", self.get_data_configuration, self.set_data_configuration)
        self.add_parameter("Metadata Configuration", self.get_metadata_configuration, self.set_metadata_configuration)
        self.add_parameter("Sequence List", self.get_sequence_list, self.set_sequence_list)
        self.add_parameter("Current Sequence", self.get_current_sequence, self.set_current_sequence)
        self.add_parameter("Current Series Sequence", self.get_current_series_sequence, self.set_current_series_sequence)
        self.add_parameter("Series", self.get_series, self.set_series)
        ##############################################################################################################

        # Connect buttons to methods ###################################################################################
        self.auto_series_addsequencestoseries_button.clicked.connect(self._on_Add_Sequence_To_series)
        self.auto_series_removesequencefromseries_button.clicked.connect(self._on_Remove_Sequence_From_series)
        self.auto_series_removeallsequencesfromseries_button.clicked.connect(self._on_Remove_All_Sequences_From_series)
        self.auto_series_sequence_save_button.clicked.connect(self._on_Save_New_Sequence)
        self.auto_series_savedsequences_list.currentItemChanged.connect(self._on_Sequence_Select)
        self.auto_series_series_list.currentItemChanged.connect(self._on_Series_Sequence_Select)
        """
        self.auto_control_runseries_button.clicked.connect(self._on_Run_series)
        self.auto_control_pauseseries_button.clicked.connect(self._on_Pause_series)
        self.auto_control_abortseries_button.clicked.connect(self._on_Abort_series)

        self.auto_series_series_list.currentItemChanged.connect(self._on_Series_Sequence_Select)
        """
        ################################################################################################################

    # PARAMETER GETTER/SETTERS ########################################################################################
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
            "storage path": self.auto_data_storagepath_ledit.text(),
            "exposure duration": self.auto_data_exposure_duration_ledit.text()
        }

        return params

    def set_data_configuration(self, params_dict):
        for key in params_dict:
            if key == "storage path":
                self.auto_data_storagepath_ledit.setText(params_dict[key])
            elif key == "exposure duration":
                self.auto_data_exposure_duration_ledit.setText(params_dict[key])

    def get_metadata_configuration(self):
        params = {
            'monochromator wavelength': str(self.auto_data_metadata_wavelength_cbox.isChecked()),
            'monochromator grating': str(self.data_configuration_metadata_grating_cbox.isChecked()),
            'monochromator order sort filter': str(self.auto_data_metadata_osf_cbox.isChecked()),
            'monochromator shutter': str(self.data_configuration_metadata_shutter_cbox.isChecked()),
            'lock-in sample frequency': str(self.auto_data_metadata_lockinfs_cbox.isChecked()),
            'lock-in sample time': str(self.data_configuration_metadata_lockints_cbox.isChecked()),
            'lock-in time constant': str(self.auto_data_metadata_lockintimeconstant_cbox.isChecked()),
            'lock-in sensitivity': str(self.data_configuration_metadata_lockin_sensitivity_cbox.isChecked()),
            'labjack dio state': str(self.data_configuration_metadata_labjack_diostate_checkbox.isChecked()),
            'ndf-wheel position': str(self.data_configuration_metadata_ndfwheel_position_checkbox.isChecked())
        }

        return params

    def set_metadata_configuration(self, params_dict):

        for key in params_dict:
            if params_dict[key] == "True":
                check_state = QtCHECKED
            else:
                check_state = QtUNCHECKED

            if key == "monochromator wavelength":
                self.auto_data_metadata_wavelength_cbox.setCheckState(check_state)
            elif key == "monochromator grating":
                self.data_configuration_metadata_grating_cbox.setCheckState(check_state)
            elif key == "monochromator order sort filter":
                self.auto_data_metadata_osf_cbox.setCheckState(check_state)
            elif key == "monochromator shutter":
                self.data_configuration_metadata_shutter_cbox.setCheckState(check_state)
            elif key == "lock-in sample frequency":
                self.auto_data_metadata_lockinfs_cbox.setCheckState(check_state)
            elif key == "lock-in sample time":
                self.data_configuration_metadata_lockints_cbox.setCheckState(check_state)
            elif key == "lock-in time constant":
                self.auto_data_metadata_lockintimeconstant_cbox.setCheckState(check_state)
            elif key == "lock-in sensitivity":
                self.data_configuration_metadata_lockin_sensitivity_cbox.setCheckState(check_state)
            elif key == "labjack dio state":
                self.data_configuration_metadata_labjack_diostate_checkbox.setCheckState(check_state)
            elif key == "ndf-wheel position":
                self.data_configuration_metadata_ndfwheel_position_checkbox.setCheckState(check_state)

    def get_sequence_list(self):
        """get_sequence_list: Return a list of the names of sequences currently present in the Saved Sequences display
        """
        pass

    def set_sequence_list(self, sequences):
        """set_sequence_list: Set the Saved Sequences display
        """
        for seq in sequences:
            GuiTab.add_item_to_list(self.auto_series_savedsequences_list, seq, "")

    def get_current_sequence(self):
        """get_current_sequence: get the name of the currently selected sequence
        """
        return self.auto_series_savedsequences_list.currentItem().text()

    def set_current_sequence(self, seq_name):
        """set_current_sequence: set the currently selected sequence
        """
        seq_item = self.auto_series_savedsequences_list.findItems(seq_name, QtCore.Qt.MatchExactly)
        self.auto_series_savedsequences_list.setCurrentItem(seq_item[0])

    def get_current_series_sequence(self):
        """get_current_series_sequence: get the name of the currently selected series sequence.
        """
        return self.auto_series_series_list.currentItem().text()

    def set_current_series_sequence(self):
        pass

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

    def set_series(self):
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
        sequence_params = self.get_parameters(["Sequence Info"])
        seq_name = sequence_params['Sequence Info']['sequence name']
        GuiTab.add_item_to_list(self.auto_series_savedsequences_list, seq_name, "")

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
            #self.auto_series_series_list.currentItemChanged.disconnect(self._on_Series_Sequence_Select)
            self.auto_series_series_list.takeItem(self.auto_series_series_list.currentRow())
            #self.auto_series_series_list.currentItemChanged.connect(self._on_Series_Sequence_Select)

    def _on_Remove_All_Sequences_From_series(self):
        """on_Save_New_Sequence: add save new sequence button identifier to button queue
        """
        #self.auto_series_series_list.currentItemChanged.disconnect(self._on_Series_Sequence_Select)
        self.auto_series_series_list.clear()
        self.series_seq_list = {}
        #self.auto_series_series_list.currentItemChanged.connect(self._on_Series_Sequence_Select)

    def _on_Sequence_Select(self):
        """_on_Sequence_Select: Add the Sequence Select identifier to the appropriate button queues.

        :return: None
        """
        self.add_button_to_queues(button_text="Sequence Select")

    def _on_Series_Sequence_Select(self):
        """_on_Series_Sequence_Select: Add the Series Sequence Select identifier to the appropriate button queues.

        :return: None
        """
        self.add_button_to_queues(button_text="Series Sequence Select")
    #End button methods###########################################################################################
    #END PRIVATE METHODS################################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    root_path = "C:\\Users\\thoma\\Documents\\Github\\SPHEREx-lab-tools\\SPHEREx-Calibration-Automation\\pylab\\"
    window = SeriesConstructionWindow(root_path)
    window.form.show()
    sys.exit(app.exec_())
