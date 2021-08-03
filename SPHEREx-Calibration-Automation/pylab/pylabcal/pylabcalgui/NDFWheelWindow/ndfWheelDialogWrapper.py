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

    def __init__(self):
        super().__init__(self)
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        # Configure parameters ####################################################
        self.add_parameter("NDF", self.get_ndf_parameters, self.set_ndf_parameters)
        ############################################################################

    # PARAMETER GETTER/SETTERS ########################
    def get_ndf_parameters(self):
        params = {
            "Current Position": self.manual_ndf_curpos_ledit.text(),
            "New Position": float(self.manual_ndf_newpos_cbox.currentText())
        }

        return params

    def set_ndf_parameters(self, set_dict):
        for p in set_dict:
            set_data = set_dict[p]
            if p == "Current Position":
                self.manual_ndf_curpos_ledit.setText(set_data)
            elif p == "New Position":
                self.manual_ndf_newpos_cbox.setCurrentText(set_data)
    ###################################################
