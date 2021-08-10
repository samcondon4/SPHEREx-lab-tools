"""ndfAutoWindowDialogWrapper:

    This module provides a wrapper class, NDFAutoWindow, around the ndfAutoWindowDialog class created using
    QT-Designer.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.NDFWheelWindow.ndfAutoWindowDialog import Ui_Form
from pylablib.QListWigetSubclass import QListWidgetItemCustom

# CONSTANTS ################################
QtUNCHECKED = QtCore.Qt.Unchecked
QtCHECKED = QtCore.Qt.Checked
QtFULL_MATCH = QtCore.Qt.MatchExactly
SEQUENCE_ROLE = 0
###########################################


class NDFAutoWindow(Ui_Form, GuiTab):

    def __init__(self, button_queue_keys=None):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        super().__init__(self, button_queue_keys=button_queue_keys)

        # Configure parameters #############################################################################
        self.add_parameter("position transition list", self.get_ndf_transitions, self.set_ndf_transitions)
        ####################################################################################################

        # Configure button methods #####################################################################
        self.sequence_ndfaddtransition_button.clicked.connect(self._on_add_transition)
        self.sequence_ndfremovetransition_button.clicked.connect(self._on_remove_transition)
        self.sequence_ndf_removealltransitions_button.clicked.connect(self._on_remove_all_transitions)
        ################################################################################################

    # PARAMETER GETTER/SETTERS #############################################################
    def get_ndf_transitions(self):
        transition_count = self.sequence_ndftransitions_list.count()
        transition_list_str = ""
        for i in range(transition_count):
            item = self.sequence_ndftransitions_list.item(i)
            item_text = item.text().replace("; ", ",")
            if transition_list_str == "":
                transition_list_str += item_text
            else:
                transition_list_str += item_text.replace("W", ";W")
        return transition_list_str

    def set_ndf_transitions(self, transition_list):
        self.sequence_ndftransitions_list.clear()
        transition_list = transition_list.split(";")
        for trans in transition_list:
            trans_text = trans.replace(",", "; ")
            GuiTab.add_item_to_list(self.sequence_ndftransitions_list, trans_text, "")

    ########################################################################################

    # PRIVATE METHODS ######################################################################
    def _on_add_transition(self):
        """_on_add_transition: add a transition to the ndf transitions list
        """
        list_item = QListWidgetItemCustom()

        valid_input = True
        try:
            ndf_position = int(self.sequence_ndfpos_ledit.text())
        except ValueError as e:
            print(e)
            valid_input = False
        try:
            transition_wavelength = float(self.sequence_ndfwave_ledit.text())
        except ValueError as e:
            print(e)
            valid_input = False

        if valid_input:
            item_data = {"Position": ndf_position, "Wavelength": transition_wavelength}
            list_item.setData(SEQUENCE_ROLE, item_data)
            list_item.setText("Wavelength = {}; Position = {}".format(transition_wavelength, ndf_position))
            list_item.set_user_data(item_data)

            self.sequence_ndftransitions_list.addItem(list_item)

    def _on_remove_transition(self):
        """_on_remove_transition: remove a transition from the ndf transitions list
        """
        rem_trans = self.sequence_ndftransitions_list.currentItem()
        if rem_trans is not None:
            rem_row = self.sequence_ndftransitions_list.currentRow()
            self.sequence_ndftransitions_list.takeItem(rem_row)

    def _on_remove_all_transitions(self):
        """_on_remove_all_transitions: remove all transitions from the ndf transitions list
        """
        self.sequence_ndftransitions_list.clear()
    ########################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = NDFAutoWindow()
    window.form.show()
    sys.exit(app.exec_())