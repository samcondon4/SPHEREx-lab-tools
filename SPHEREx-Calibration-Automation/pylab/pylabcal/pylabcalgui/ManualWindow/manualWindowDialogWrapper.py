"""manualWindowDialogWrapper:

    This module provides a wrapper class, ManualWindow, around the manualWindowDialog that was generated with
    QT-Designer. ManualWindow follows the SXTC-SWS GUI Tab API format.

Sam Condon, 06/21/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from manualWindowDialog import Ui_Form
from queue import SimpleQueue
from pylablib.pylablib_gui_tab import GuiTab


class ManualWindow(Ui_Form, GuiTab):

    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        ##Configure parameters###############################################################
        self.add_parameter("Monochromator", self.get_monochromator_parameters, self.set_monochromator_parameters)
        self.add_parameter("Lock-In", self.get_lockin_parameters, self.set_lockin_parameters)
        #####################################################################################

        ##Connect buttons to methods ########################################################
        self.manual_monochromator_setparams_button.clicked.connect(self._on_Set_Parameters)
        self.manual_monochromator_abort_button.clicked.connect(self._on_Abort)
        self.manual_lockin_startmeasurement_button.clicked.connect(self._on_Start_Measurement)
        ######################################################################################

    #PARAMETER GETTERS/SETTERS########################################################################################
    def get_monochromator_parameters(self):
        params = {
            'wavelength': self.manual_monochromator_wavelength_ledit.text(),
            'filter': self.manual_monochromator_filter_combobox.currentText(),
            'grating': self.manual_monochromator_grating_combobox.currentText(),
            'shutter': self.manual_monochromator_shutter_combobox.currentText()
        }

        return params

    def set_monochromator_parameters(self, params_dict):
        for key in params_dict:
            if key == "wavelength":
                self.manual_monochromator_wavelength_ledit.setText(params_dict[key])
            elif key == "filter":
                self.manual_monochromator_filter_combobox.setText(params_dict[key])
            elif key == "grating":
                self.manual_monochromator_grating_combobox.setCurrentText(params_dict[key])
            elif key == "shutter":
                self.manual_monochromator_shutter_combobox.setCurrentText(params_dict[key])

    def get_lockin_parameters(self):
        params = {
            'sensitivity value': self.manual_lockin_sensitivityvalue_cbox.currentText(),
            'sensitivity multiplier': self.manual_lockin_sensitivitymultiplier_cbox.currentText(),
            'sensitivity units': self.manual_lockin_sensitivityunit_cbox.currentText(),
            'time-constant value': self.manual_lockin_timeconstantvalue_cbox.currentText(),
            'time-constant multiplier': self.manual_lockin_timeconstantmultiplier_cbox.currentText(),
            'time-constant units': self.manual_lockin_timeconstantunit_cbox.currentText(),
            'sample rate': self.manual_lockin_samplerate_ledit.text(),
            'sample time': self.manual_lockin_sampletime_ledit.text(),
            'measurement storage path': self.manual_lockin_measurementstorage_ledit.text()
        }

        return params

    def set_lockin_parameters(self, params_dict):
        for key in params_dict:
            if key == "sensitivity value":
                self.manual_lockin_sensitivityvalue_cbox.setCurrentText(params_dict[key])
            elif key == "sensitivity multiplier":
                self.manual_lockin_sensitivitymultiplier_cbox.setCurrentText(params_dict[key])
            elif key == "sensitivity units":
                self.manual_lockin_sensitivityunit_cbox.setCurrentText(params_dict[key])
            elif key == "time-constant value":
                self.manual_lockin_timeconstantvalue_cbox.setCurrentText(params_dict[key])
            elif key == "time-constant multiplier":
                self.manual_lockin_timeconstantmultiplier_cbox.setCurrentText(params_dict[key])
            elif key == "time-constant units":
                self.manual_lockin_timeconstantunit_cbox.setCurrentText(params_dict[key])
            elif key == "sample rate":
                self.manual_lockin_samplerate_ledit.setText(params_dict[key])
            elif key == "sample time":
                self.manual_lockin_sampletime_ledit.setText(params_dict[key])
            elif key == "measurement storage path":
                self.manual_lockin_measurementstorage_ledit.setText(params_dict[key])
##################################################################################################################

##MAIN API METHODS################################################################################################
    #################################################################################################################

    ##PRIVATE METHODS################################################################################################
    #Button Methods#####
    def _on_Set_Parameters(self):
        """_on_Set_Parameters: Add the Set Parameters button identifier to button queue

        :return: None
        """
        self.button_queue.put("Monochromator Set Parameters")

    def _on_Abort(self):
        """_on_Abort: Add the Abort button identifier to button queue.

        :return: None
        """
        self.button_queue.put("Abort")

    def _on_Start_Measurement(self):
        """_on_Start_Measurement: Add the Start Measurement button identifier to button queue.

        :return: None
        """
        self.button_queue.put("Start Measurement")
    #################################################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ManualWindow()
    window.form.show()
    sys.exit(app.exec_())


