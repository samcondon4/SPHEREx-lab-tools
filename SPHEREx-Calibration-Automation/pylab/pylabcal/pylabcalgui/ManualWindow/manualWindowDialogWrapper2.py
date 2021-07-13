"""manualWindowDialogWrapper:

    This module provides a wrapper class, ManualWindow, around the manualWindowDialog that was generated with
    QT-Designer. ManualWindow follows the SXTC-SWS GUI Tab API format.

Sam Condon, 06/21/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylabcal.pylabcalgui.ManualWindow.manualWindowDialog2 import Ui_Form
from pylablib.pylablib_gui_tab import GuiTab


class ManualWindow(Ui_Form, GuiTab):

    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)
        self.is_stacked_widget = True
        super().__init__(self)

        ##Configure parameters#####################################################################################
        self.add_parameter("Monochromator", self.get_monochromator_parameters, self.set_monochromator_parameters)
        self.add_parameter("Lock-In", self.get_lockin_parameters, self.set_lockin_parameters)
        self.add_parameter("LabJack", self.get_labjack_parameters, self.set_labjack_parameters)
        ###########################################################################################################

        ##Connect buttons to methods #######################################################################
        self.manual_monochromator_setparams_button.clicked.connect(self._on_Set_Monochromator_Parameters)
        self.manual_lockin_setparams_button.clicked.connect(self._on_Set_Lockin_Parameters)
        self.manual_lockin_startmeasurement_button.clicked.connect(self._on_Start_Measurement)
        self.manual_labjack_dio0state_check.stateChanged.connect(self._on_dio0state_Changed)
        self.manual_labjack_dio1state_check.stateChanged.connect(self._on_dio1state_Changed)
        self.manual_labjack_dio2state_check.stateChanged.connect(self._on_dio2state_Changed)
        self.manual_labjack_dio0config_cbox.currentIndexChanged.connect(self._on_dio0config_Changed)
        self.manual_labjack_dio1config_cbox.currentIndexChanged.connect(self._on_dio1config_Changed)
        self.manual_labjack_dio2config_cbox.currentIndexChanged.connect(self._on_dio2config_Changed)
        #####################################################################################################

    # PARAMETER GETTERS/SETTERS########################################################################################
    def get_monochromator_parameters(self):
        params = {
            'wavelength': self.manual_monochromator_newwavelength_ledit.text(),
            'filter': self.manual_monochromator_newfilter_combobox.currentText(),
            'grating': self.manual_monochromator_newgrating_combobox.currentText(),
            'shutter': self.manual_monochromator_newshutter_combobox.currentText()
        }

        return params

    def set_monochromator_parameters(self, params_dict):
        for key in params_dict:
            param = str(params_dict[key])
            if key == "wavelength":
                self.manual_monochromator_currentwavelength_ledit.setText(param)
                self.manual_monochromator_newwavelength_ledit.setText(param)
            elif key == "filter":
                if param == "1":
                    param = "OSF1"
                elif param == "2":
                    param = "OSF2"
                elif param == "3":
                    param = "OSF3"
                elif param == "4":
                    param = "No OSF"
                self.manual_monochromator_currentfilter_combobox.setCurrentText(param)
                self.manual_monochromator_newfilter_combobox.setCurrentText(param)
            elif key == "grating":
                if param == "1":
                    param = "G1"
                elif param == "2":
                    param = "G2"
                elif param == "3":
                    param = "G3"
                self.manual_monochromator_currentgrating_combobox.setCurrentText(param)
                self.manual_monochromator_newgrating_combobox.setCurrentText(param)
            elif key == "shutter":
                if param == "O":
                    param = "Open"
                elif param == "C":
                    param = "Close"
                self.manual_monochromator_currentshutter_combobox.setCurrentText(param)
                self.manual_monochromator_newshutter_combobox.setCurrentText(param)

    def get_lockin_parameters(self):
        params = {
            'sensitivity value': self.manual_lockin_sensitivityvalue_cbox.currentText(),
            'sensitivity multiplier': self.manual_lockin_sensitivitymultiplier_cbox.currentText(),
            'sensitivity units': self.manual_lockin_sensitivityunit_cbox.currentText(),
            'time-constant value': self.manual_lockin_timeconstantvalue_cbox.currentText(),
            'time-constant multiplier': self.manual_lockin_timeconstantmultiplier_cbox.currentText(),
            'time-constant units': self.manual_lockin_timeconstantunit_cbox.currentText(),
            'sample rate': self.manual_lockin_samplerate_combobox.currentText(),
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
                self.manual_lockin_samplerate_combobox.setCurrentText(params_dict[key])
            elif key == "sample time":
                self.manual_lockin_sampletime_ledit.setText(params_dict[key])
            elif key == "measurement storage path":
                self.manual_lockin_measurementstorage_ledit.setText(params_dict[key])

    def get_labjack_parameters(self):
        params = {
            0: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            1: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            2: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            3: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            4: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            5: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            6: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            7: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            8: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            9: {"State": self.manual_labjack_dio0state_check.checkState(),
                "Config": self.manual_labjack_dio0config_cbox.currentText()},
            10: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            11: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            12: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            13: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            14: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            15: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            16: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            17: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            18: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            19: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            20: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()},
            21: {"State": self.manual_labjack_dio0state_check.checkState(),
                 "Config": self.manual_labjack_dio0config_cbox.currentText()}
        }

        return params

    def set_labjack_parameters(self, params_dict):
        for dio in params_dict:
            if dio == 0:
                self.manual_labjack_dio0config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio0state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 1:
                self.manual_labjack_dio1config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio1state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 2:
                self.manual_labjack_dio2config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio2state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 3:
                self.manual_labjack_dio3config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio3state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 4:
                self.manual_labjack_dio4config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio4state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 5:
                self.manual_labjack_dio5config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio5state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 6:
                self.manual_labjack_dio6config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio6state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 7:
                self.manual_labjack_dio7config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio7state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 8:
                self.manual_labjack_dio8config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio8state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 9:
                self.manual_labjack_dio9config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio9state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 10:
                self.manual_labjack_dio10config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio10state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 11:
                self.manual_labjack_dio11config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio11state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 12:
                self.manual_labjack_dio12config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio12state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 13:
                self.manual_labjack_dio13config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio13state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 14:
                self.manual_labjack_dio14config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio14state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 15:
                self.manual_labjack_dio15config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio15state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 16:
                self.manual_labjack_dio16config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio16state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 17:
                self.manual_labjack_dio17config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio17state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 18:
                self.manual_labjack_dio18config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio18state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 19:
                self.manual_labjack_dio19config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio19state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 20:
                self.manual_labjack_dio20config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio20state_check.setCheckState(params_dict[dio]["State"])
            elif dio == 21:
                self.manual_labjack_dio21config_cbox.setCurrentText(params_dict[dio]["Config"])
                self.manual_labjack_dio21state_check.setCheckState(params_dict[dio]["State"])

    ##################################################################################################################

    ##PRIVATE METHODS################################################################################################
    # Button Methods#####
    def _on_Set_Monochromator_Parameters(self):
        """_on_Set_Parameters: Add the Set Parameters button identifier to button queue

        :return: None
        """
        self.button_queue.put("Monochromator Set Parameters")

    def _on_Abort(self):
        """_on_Abort: Add the Abort button identifier to button queue.

        :return: None
        """
        self.button_queue.put("Abort")

    def _on_Set_Lockin_Parameters(self):
        """_on_Set_Lockin_Parameters: Add the lockin set parameters button identifier to the button queue.

        :return: None
        """
        self.button_queue.put("Lock-In Set Parameters")

    def _on_Start_Measurement(self):
        """_on_Start_Measurement: Add the Start Measurement button identifier to button queue.

        :return: None
        """
        self.button_queue.put("Start Measurement")

    def _on_dio0state_Changed(self):
        """_on_dio0state_Changed: Execute when the dio0 check state changes. Place "Checked" or "Unchecked" on the
           button queue depending on the new checkbox state.

        :return: None
        """
        if self.manual_labjack_dio0state_check.checkState():
            self.button_queue.put("Labjack Dio0 Checked")
        else:
            self.button_queue.put("Labjack Dio0 Unchecked")

    def _on_dio1state_Changed(self):
        """_on_dio1state_Changed: Execute when the dio0 check state changes. Place "Checked" or "Unchecked" on the
           button queue depending on the new checkbox state.

        :return: None
        """
        if self.manual_labjack_dio1state_check.checkState():
            self.button_queue.put("Labjack Dio1 Checked")
        else:
            self.button_queue.put("Labjack Dio1 Unchecked")

    def _on_dio2state_Changed(self):
        """_on_dio2state_Changed: Execute when the dio0 check state changes. Place "Checked" or "Unchecked" on the
           button queue depending on the new checkbox state.

        :return: None
        """
        if self.manual_labjack_dio2state_check.checkState():
            self.button_queue.put("Labjack Dio2 Checked")
        else:
            self.button_queue.put("Labjack Dio2 Unchecked")

    def _on_dio0config_Changed(self):
        """_on_dio0config_Changed: Set labjack dio 0 to either input or output depending on user gui input.

        """
        self.button_queue.put("Labjack Config Dio0 {}".format(self.manual_labjack_dio0config_cbox.currentText()))

    def _on_dio1config_Changed(self):
        """_on_dio1config_Changed: Set labjack dio 1 to either input or output depending on user gui input.

        """
        self.button_queue.put("Labjack Config Dio1 {}".format(self.manual_labjack_dio1config_cbox.currentText()))

    def _on_dio2config_Changed(self):
        """_on_dio2config_Changed: Set labjack dio 0 to either input or output depending on user gui input.

        """
        self.button_queue.put("Labjack Config Dio2 {}".format(self.manual_labjack_dio2config_cbox.currentText()))

    #################################################################################################################


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ManualWindow()
    window.form.show()
    sys.exit(app.exec_())
