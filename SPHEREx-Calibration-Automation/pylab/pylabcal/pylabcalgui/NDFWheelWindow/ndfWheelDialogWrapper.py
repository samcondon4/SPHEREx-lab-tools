"""ndfWheelDialogWrapper:

    This module provides a wrapper class, NDFWindow, around the ndfWheelDialog that
    was generated using QT-Designer. The NDFWindow follows the SXTC-SWS GUI Tab API
    format.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.NDFWheelWindow.ndfWheelDialog import Ui_Form


class NDFWindow(Ui_Form, GuiTab):

    def __init__(self, button_queue_keys=None):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)
        super().__init__(self, button_queue_keys=button_queue_keys)

        # Configure parameters ######################################################################
        self.add_parameter("currentposition", self.get_current_position, self.set_current_position)
        self.add_parameter("newposition", self.get_new_position, self.set_new_position)
        ##############################################################################################

    # PARAMETER GETTER/SETTERS ###########################################
    def get_current_position(self):
        """get_current_position: return the current ndf display position.
        """
        return float(self.manual_ndf_curpos_ledit.text())

    def set_current_position(self, cur_pos):
        """set_current_position: set the current ndf display position.
        """
        cur_pos = str(cur_pos)
        self.manual_ndf_curpos_ledit.setText(cur_pos)

    def get_new_position(self):
        """get_new_position: return the ndw new position display.
        """
        return float(self.manual_ndf_newpos_cbox.currentText())

    def set_new_position(self, new_pos):
        """set_new_position: set the ndf new position display.
        """
        new_pos = str(new_pos)
        self.manual_ndf_newpos_cbox.setCurrentText(new_pos)
    ########################################################################
