"""lockinWindowDialogWrapper:

    This module provides a wrapper class, LockinWindow, around the lockinWindowDialog that
    was generated using QT-Designer. The LockinWindow follows the SXTC-SWS GUI Tab API
    format.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.LockinWindow.lockinWindowDialog import Ui_Form


class LockinWindow(Ui_Form, GuiTab):

    def __init__(self):
        super().__init__(self)
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        # Configure parameters ###########################
        self.add_parameter("Lock-In", self.get_lockin_parameters, self.set_lockin_parameters)
        ##################################################

        # Connect buttons to methods #####################
        self.manual_lockin_setparams_button.clicked.connect(self._on_Set_Lockin_Parameters)
        self.manual_lockin_startmeasurement_button.clicked.connect(self._on_Start_Measurement)
        ##################################################

    # PARAMETER GETTER/SETTERS ############################
    def get_lockin_parameters(self):
        sens_units = self.manual_lockin_sensitivityunit_cbox.currentText()
        sens_mult = float(self.manual_lockin_sensitivitymultiplier_cbox.currentText().split('x')[1])
        sens_val = float(self.manual_lockin_sensitivityvalue_cbox.currentText())
        sens = None
        if sens_units == "V.":
            sens = sens_val*sens_mult
        elif sens_units == "mV.":
            sens = sens_val*sens_mult * 1e-3
        elif sens_units == "uV.":
            sens = sens_val*sens_mult * 1e-6
        elif sens_units == "nV.":
            sens = sens_val*sens_mult * 1e-9

        sens = round(sens, 10)

        tc_units = self.manual_lockin_timeconstantunit_cbox.currentText()
        tc_mult = float(self.manual_lockin_timeconstantmultiplier_cbox.currentText().split('x')[1])
        tc_val = float(self.manual_lockin_timeconstantvalue_cbox.currentText())
        tc = None
        if tc_units == "ks.":
            tc = tc_val*tc_mult * 1e3
        elif tc_units == "s.":
            tc = tc_val*tc_mult
        elif tc_units == "ms.":
            tc = tc_val*tc_mult * 1e-3
        elif tc_units == "us.":
            tc = tc_val*tc_mult * 1e-6
        elif tc_units == "ns.":
            tc = tc_val*tc_mult * 1e-9

        tc = round(tc, 7)

        params = {
            'sensitivity value': float(self.manual_lockin_sensitivityvalue_cbox.currentText()),
            'sensitivity multiplier': float(self.manual_lockin_sensitivitymultiplier_cbox.currentText().split('x')[1]),
            'sensitivity units': self.manual_lockin_sensitivityunit_cbox.currentText(),
            'sensitivity': sens,
            'time-constant value': float(self.manual_lockin_timeconstantvalue_cbox.currentText()),
            'time-constant multiplier': float(self.manual_lockin_timeconstantmultiplier_cbox.currentText().split('x')[1]),
            'time-constant units': self.manual_lockin_timeconstantunit_cbox.currentText(),
            'time-constant': tc,
            'sample rate': float(self.manual_lockin_samplerate_combobox.currentText()),
            'sample time': float(self.manual_lockin_sampletime_ledit.text()),
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
            elif key == "sensitivity":
                self.manual_lockin_sensitivity_ledit.setText(params_dict[key])
            elif key == "time-constant value":
                self.manual_lockin_timeconstantvalue_cbox.setCurrentText(params_dict[key])
            elif key == "time-constant multiplier":
                self.manual_lockin_timeconstantmultiplier_cbox.setCurrentText(params_dict[key])
            elif key == "time-constant units":
                self.manual_lockin_timeconstantunit_cbox.setCurrentText(params_dict[key])
            elif key == "time-constant":
                self.manual_lockin_timeconstant_ledit.setText(params_dict[key])
            elif key == "sample rate":
                self.manual_lockin_samplerate_combobox.setCurrentText(params_dict[key])
            elif key == "sample time":
                self.manual_lockin_sampletime_ledit.setText(params_dict[key])
            elif key == "measurement storage path":
                self.manual_lockin_measurementstorage_ledit.setText(params_dict[key])

    #######################################################

    # PRIVATE METHODS ######################################################################################
    # button methods ###############
    def _on_Set_Lockin_Parameters(self):
        """_on_Set_Lockin_Parameters: Add the lockin set parameters button identifier to the button queue.

        :return: None
        """
        put_string = "Lock-In Set Parameters"
        self.button_queue.put(put_string)
        GuiTab.GlobalButtonQueue.put(put_string)

    def _on_Start_Measurement(self):
        """_on_Start_Measurement: Add the Start Measurement button identifier to button queue.

        :return: None
        """
        put_string = "Start Measurement"
        self.button_queue.put(put_string)
        GuiTab.GlobalButtonQueue.put(put_string)
    #########################################################################################################

