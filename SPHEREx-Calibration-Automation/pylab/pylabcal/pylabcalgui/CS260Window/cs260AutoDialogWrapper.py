"""cs260AutoDialogWrapper:

    This module provides a wrapper class, CS260AutoWindow, around the cs260AutoDialog class created using
    QT-Designer.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.CS260Window.CS260AutoDialog import Ui_Form


class CS260AutoWindow(Ui_Form, GuiTab):

    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        super().__init__(self)

        # Configure Parameters ###################################################################################
        self.add_parameter("Monochromator", self.get_monochromator_parameters, self.set_monochromator_parameters)
        ##########################################################################################################

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CS260AutoWindow()
    window.form.show()
    sys.exit(app.exec_())
