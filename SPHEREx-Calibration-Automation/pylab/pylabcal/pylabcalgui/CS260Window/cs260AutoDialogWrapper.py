"""cs260AutoDialogWrapper:

    This module provides a wrapper class, CS260AutoWindow, around the cs260AutoDialog class created using
    QT-Designer.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.CS260Window.CS260AutoDialog import Ui_Form


class CS260AutoWindow(Ui_Form, GuiTab):

    def __init__(self, button_queue_keys=None):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        super().__init__(self, button_queue_keys=button_queue_keys)

        # Configure Parameters ###################################################################################
        self.add_parameter("start wavelength", self.get_start_wavelength, self.set_start_wavelength)
        self.add_parameter("stop wavelength", self.get_stop_wavelength, self.set_stop_wavelength)
        self.add_parameter("step size", self.get_step_size, self.set_step_size)
        self.add_parameter("shutter", self.get_shutter, self.set_shutter)
        self.add_parameter("g1 to g2 transition wavelength", self.get_g1g2_transition, self.set_g1g2_transition)
        self.add_parameter("g2 to g3 transition wavelength", self.get_g2g3_transition, self.set_g2g3_transition)
        self.add_parameter("no osf to osf1 transition wavelength", self.get_noosfosf1_transition,
                           self.set_noosfosf1_transition)
        self.add_parameter("osf1 to osf2 transition wavelength", self.get_osf1osf2_transition,
                           self.set_osf1osf2_transition)
        self.add_parameter("osf2 to osf3 transition wavelength", self.get_osf2osf3_transition,
                           self.set_osf2osf3_transition)
        ##########################################################################################################

    # PARAMETER GETTER/SETTERS ###################################################################################
    def get_start_wavelength(self):
        """get_start_wavelength: Return the starting wavelength parameter.
        """
        return self.sequence_monochromator_startwave_ledit.text()

    def set_start_wavelength(self, wave):
        """set_start_wavelength: Set the starting wavelength parameter display.
        """
        self.sequence_monochromator_startwave_ledit.setText(wave)

    def get_stop_wavelength(self):
        return self.sequence_monochromator_endwave_ledit.text()

    def set_stop_wavelength(self, wave):
        self.sequence_monochromator_endwave_ledit.setText(wave)

    def get_step_size(self):
        return self.sequence_monochromator_stepsize_ledit.text()

    def set_step_size(self, step):
        self.sequence_monochromator_stepsize_ledit.setText(step)

    def get_shutter(self):
        return self.sequence_monochromator_shutter_combobox.currentText()

    def set_shutter(self, shutter):
        self.sequence_monochromator_shutter_combobox.setCurrentText(shutter)

    def get_g1g2_transition(self):
        return self.sequence_monochromator_g1g2_ledit.text()

    def set_g1g2_transition(self, trans):
        self.sequence_monochromator_g1g2_ledit.setText(trans)

    def get_g2g3_transition(self):
        return self.sequence_monochromator_g2g3_ledit.text()

    def set_g2g3_transition(self, trans):
        self.sequence_monochromator_g2g3_ledit.setText(trans)

    def get_noosfosf1_transition(self):
        return self.sequence_monochromator_noosfosf1_ledit.text()

    def set_noosfosf1_transition(self, trans):
        self.sequence_monochromator_noosfosf1_ledit.setText(trans)

    def get_osf1osf2_transition(self):
        return self.sequence_monochromator_osf1osf2_ledit.text()

    def set_osf1osf2_transition(self, trans):
        self.sequence_monochromator_osf1osf2_ledit.setText(trans)

    def get_osf2osf3_transition(self):
        return self.sequence_monochromator_osf2osf3_ledit.text()

    def set_osf2osf3_transition(self, trans):
        self.sequence_monochromator_osf2osf3_ledit.setText(trans)
    ##############################################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CS260AutoWindow()
    window.form.show()
    sys.exit(app.exec_())
