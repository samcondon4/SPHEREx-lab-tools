"""lockinWindowDialogWrapper:

    This module provides a wrapper class, LockinWindow, around the lockinWindowDialog that
    was generated using QT-Designer. The LockinWindow follows the SXTC-SWS GUI Tab API
    format.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.LockinWindow.lockinWindowDialog import Ui_Form
from pylabcal.pylabcalgui.LockinWindow.lockin_window_helpers import *


class LockinWindow(Ui_Form, GuiTab):

    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)
        super().__init__(self)

        # Configure parameters ##############################################################################
        self.add_parameter("current sensitivity", self.get_current_sensitivity, self.set_current_sensitivity)
        self.add_parameter("current tc", self.get_current_tc, self.set_current_tc)
        self.add_parameter("new sensitivity", self.get_new_sensitivity, self.set_new_sensitivity)
        self.add_parameter("new tc", self.get_new_tc, self.set_new_tc)
        self.add_parameter("sample rate", self.get_sample_rate, self.set_sample_rate)
        self.add_parameter("sample time", self.get_sample_time, self.set_sample_time)
        self.add_parameter("measurement storage path", self.get_storage_path, self.set_storage_path)
        self.add_parameter("Lock-In", self.get_lockin_parameters, self.set_lockin_parameters)
        #####################################################################################################

        # Connect buttons to methods #####################
        """
        self.manual_lockin_setparams_button.clicked.connect(self._on_Set_Lockin_Parameters)
        self.manual_lockin_startmeasurement_button.clicked.connect(self._on_Start_Measurement)
        """
        ##################################################

    # PARAMETER GETTER/SETTERS ############################
    def get_current_sensitivity(self):
        """get_current_sensitivity: return the current lockin sensitivity display value.
        """
        sens_dict = {"sr510": self.sr510_manual_lockin_sensitivity_ledit.text(),
                     "sr830": self.sr830_manual_lockin_sensitivity_ledit.text()}
        return sens_dict

    def set_current_sensitivity(self, sens_dict):
        """set_current_sensitivity: set the current lockin sensitivity display value.
        """
        for key in sens_dict:
            sens_text = sens_dict[key]
            if key == "sr510":
                self.sr510_manual_lockin_sensitivity_ledit.setText(sens_text)
            elif key == "sr830":
                self.sr830_manual_lockin_sensitivity_ledit.setText(sens_text)

    def get_current_tc(self):
        """get_current_tc: return the current lockin sensitivity display value.
        """
        sr510_tc_value = float(self.sr510_manual_lockin_timeconstant_ledit.currentText())
        sr510_tc_multiplier = float(self.sr510_manual_lockin_timeconstantmultiplier_cbox.currentText().split('x')[1:][0])
        sr510_tc_units = self.sr510_manual_lockin_timeconstantunit_cbox.currentText()
        sr510_tc_unit_multiplier = LOCKIN_UNIT_TC_MAP[sr510_tc_units]
        sr510_tc = sr510_tc_value*sr510_tc_multiplier*sr510_tc_unit_multiplier

        sr830_tc_value = float(self.sr830_manual_lockin_timeconstant_ledit.currentText())
        sr830_tc_multiplier = float(self.sr830_manual_lockin_timeconstantmultiplier_cbox.currentText().split('x')[1:][0])
        sr830_tc_units = self.sr830_manual_lockin_timeconstantunit_cbox.currentText()
        sr830_tc_unit_multiplier = LOCKIN_UNIT_TC_MAP[sr830_tc_units]
        sr830_tc = sr830_tc_value*sr830_tc_multiplier*sr830_tc_unit_multiplier

        return {"sr510": sr510_tc, "sr830": sr830_tc}

    def set_current_tc(self, tc_dict):
        pass

    def get_new_sensitivity(self):
        pass

    def set_new_sensitivity(self, sens_dict):
        pass

    def get_new_tc(self):
        pass

    def set_new_tc(self, tc_dict):
        pass

    def get_sample_rate(self):
        pass

    def set_sample_rate(self, sr_dict):
        pass

    def get_sample_time(self):
        st_dict = {"sr510": self.sr510_manual_lockin_sampletime_ledit.text(),
                   "sr830": self.sr830_manual_lockin_sampletime_ledit.text()}
        return st_dict

    def set_sample_time(self, st_dict):
        for key in st_dict:
            st_text = st_dict[key]
            if key == "sr510":
                self.sr510_manual_lockin_sampletime_ledit.setText(st_text)
            elif key == "sr830":
                self.sr830_manual_lockin_sampletime_ledit.setText(st_text)

    def get_storage_path(self):
        sp_dict = {"sr510": self.sr510_manual_lockin_measurementstorage_ledit.text(),
                   "sr830": self.sr830_manual_lockin_measurementstorage_ledit.text()}
        return sp_dict

    def set_storage_path(self, sp_dict):
        for key in sp_dict:
            if key == "sr510":
                self.sr510_manual_lockin_measurementstorage_ledit.setText(sp_dict[key])
            elif key == "sr830":
                self.sr830_manual_lockin_measurementstorage_ledit.setText(sp_dict[key])

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

