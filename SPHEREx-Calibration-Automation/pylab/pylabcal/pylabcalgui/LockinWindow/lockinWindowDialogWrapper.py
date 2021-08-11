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

    def __init__(self, button_queue_keys=None):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)
        super().__init__(self, button_queue_keys=button_queue_keys)

        # Configure parameters ##############################################################################
        self.add_parameter("cfgparams", self.get_cfg_params, self.set_cfg_params)
        self.add_parameter("measurementparams", self.get_measurement_params, self.set_measurement_params)
        self.add_parameter("current sensitivity", self.get_current_sensitivity, self.set_current_sensitivity)
        self.add_parameter("current tc", self.get_current_tc, self.set_current_tc)
        self.add_parameter("new sensitivity", self.get_new_sensitivity, self.set_new_sensitivity)
        self.add_parameter("new tc", self.get_new_tc, self.set_new_tc)
        self.add_parameter("sample rate", self.get_sample_rate, self.set_sample_rate)
        self.add_parameter("sample time", self.get_sample_time, self.set_sample_time)
        self.add_parameter("measurement storage path", self.get_storage_path, self.set_storage_path)
        #####################################################################################################

        # Connect buttons to methods #####################
        """
        self.manual_lockin_setparams_button.clicked.connect(self._on_Set_Lockin_Parameters)
        self.manual_lockin_startmeasurement_button.clicked.connect(self._on_Start_Measurement)
        """
        ##################################################

    # PARAMETER GETTER/SETTERS ############################
    def get_cfg_params(self):
        """get_cfg_params: return the current lockin configuration parameters. These include the time-constant and
                           sensitivity
        """
        tcs = self.get_new_tc()
        sens = self.get_new_sensitivity()
        params_dict = {"time constant": tcs, "sensitivity": sens}

        return params_dict

    def set_cfg_params(self, cfg_params):
        """set_cfg_params: set new lockin configuration parameters.
        """
        for key in cfg_params:
            if key == "time constant":
                self.set_new_tc(cfg_params[key])
            elif key == "sensitivity":
                self.set_new_tc(cfg_params[key])

    def get_measurement_params(self):
        """get_measurement_params: return the current measurement configuration parameters. These include the sample
                                   frequency, sample time, and measurement storage path.
        """
        sample_freq = self.get_sample_rate()
        sample_time = self.get_sample_time()
        storage = self.get_storage_path()
        params_dict = {"sample rate": sample_freq, "sample time": sample_time, "storage": storage}

        return params_dict

    def set_measurement_params(self, measurement_params):
        """set_measurement_params: set new lockin measurement parameters.
        """
        for key in measurement_params:
            params = measurement_params[key]
            if key == "sample rate":
                self.set_sample_rate(params)
            elif key == "sample time":
                self.set_sample_time(params)
            elif key == "storage":
                self.set_storage_path(params)

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
        return {"sr510": self.sr510_manual_lockin_timeconstant_ledit.text(),
                "sr830": self.sr830_manual_lockin_timeconstant_ledit.text()}

    def set_current_tc(self, tc_dict):
        """set_current_tc: set the value displayed in the current time constant view.
        """
        for key in tc_dict:
            tc = tc_dict[key]
            if type(tc) is float or type(tc) is int:
                tc = str(tc)
            if key == "sr510":
                self.sr510_manual_lockin_timeconstant_ledit.setText(tc)
            elif key == "sr830":
                self.sr830_manual_lockin_timeconstant_ledit.setText(tc)

    def get_new_sensitivity(self):
        """get_new_sensitivity: get the new sensitivity value specified.
        """
        sr510_sens_value = float(self.sr510_manual_lockin_sensitivityvalue_cbox.currentText())
        sr510_sens_multiplier = float(self.sr510_manual_lockin_sensitivitymultiplier_cbox.currentText().split('x')[1])
        sr510_sens_units = self.sr510_manual_lockin_sensitivityunit_cbox.currentText()
        sr510_sens_unit_mult = LOCKIN_UNIT_SENSITIVITY_MAP[sr510_sens_units]
        sr510_sens = sr510_sens_value*sr510_sens_multiplier*sr510_sens_unit_mult

        sr830_sens_value = float(self.sr830_manual_lockin_sensitivityvalue_cbox.currentText())
        sr830_sens_multiplier = float(self.sr830_manual_lockin_sensitivitymultiplier_cbox.currentText().split('x')[1])
        sr830_sens_units = self.sr830_manual_lockin_sensitivityunit_cbox.currentText()
        sr830_sens_unit_mult = LOCKIN_UNIT_SENSITIVITY_MAP[sr830_sens_units]
        sr830_sens = sr830_sens_value*sr830_sens_multiplier*sr830_sens_unit_mult

        return {"sr510": sr510_sens, "sr830": sr830_sens}

    def set_new_sensitivity(self, sens_dict):
        """set_new_sensitivity: set a new sensitivity value on the lockin combo-box displays
        """
        for key in sens_dict:
            sens = sens_dict[key]
            sens_value = LOCKIN_SENS_MOD_MAP[sens % 5]
            sens_multiplier, sens_units = LOCKIN_SENS_MULT_UNIT_MAP[sens/sens_value]
            if key == "sr510":
                self.sr510_manual_lockin_sensitivityvalue_cbox.setCurrentText(sens_value)
                self.sr510_manual_lockin_sensitivitymultiplier_cbox.setCurrentText(sens_multiplier)
                self.sr510_manual_lockin_sensitivityunit_cbox.setCurrentText(sens_units)
            elif key == "sr830":
                self.sr830_manual_lockin_sensitivityvalue_cbox.setCurrentText(sens_value)
                self.sr830_manual_lockin_sensitivitymultiplier_cbox.setCurrentText(sens_multiplier)
                self.sr830_manual_lockin_sensitivityunit_cbox.setCurrentText(sens_units)

    def get_new_tc(self):
        """get_new_tc: return the new time-constant value specified by the lockin combo-box inputs.
        """
        sr510_tc_value = float(self.sr510_manual_lockin_timeconstantvalue_cbox.currentText())
        sr510_tc_multiplier = float(self.sr510_manual_lockin_timeconstantmultiplier_cbox.currentText().split('x')[1:][0])
        sr510_tc_units = self.sr510_manual_lockin_timeconstantunit_cbox.currentText()
        sr510_tc_unit_multiplier = LOCKIN_UNIT_TC_MAP[sr510_tc_units]
        sr510_tc = sr510_tc_value*sr510_tc_multiplier*sr510_tc_unit_multiplier

        sr830_tc_value = float(self.sr830_manual_lockin_timeconstantvalue_cbox.currentText())
        sr830_tc_multiplier = float(self.sr830_manual_lockin_timeconstantmultiplier_cbox.currentText().split('x')[1:][0])
        sr830_tc_units = self.sr830_manual_lockin_timeconstantunit_cbox.currentText()
        sr830_tc_unit_multiplier = LOCKIN_UNIT_TC_MAP[sr830_tc_units]
        sr830_tc = sr830_tc_value*sr830_tc_multiplier*sr830_tc_unit_multiplier

        return {"sr510": sr510_tc, "sr830": sr830_tc}

    def set_new_tc(self, tc_dict):
        """set_new_tc: set the new time constant combo box displays
        """
        for key in tc_dict:
            tc = tc_dict[key]
            if type(tc) is str:
                tc = float(tc)
            tc_mod = tc % 3
            tc_value = tc_mod + LOCKIN_TC_MOD_MAP[tc_mod]
            tc_mult, tc_units = LOCKIN_TC_MULT_UNIT_MAP[tc/tc_value]
            if key == "sr510":
                self.sr510_manual_lockin_timeconstantvalue_cbox.setCurrentText(str(tc_value))
                self.sr510_manual_lockin_timeconstantmultiplier_cbox.setCurrentText(tc_mult)
                self.sr510_manual_lockin_timeconstantunit_cbox.setCurrentText(tc_units)
            elif key == "sr830":
                self.sr830_manual_lockin_sensitivityvalue_cbox.setCurrentText(tc_value)
                self.sr830_manual_lockin_timeconstantmultiplier_cbox.setCurrentText(tc_mult)
                self.sr830_manual_lockin_timeconstantunit_cbox.setCurrentText(tc_units)

    def get_sample_rate(self):
        """get_sample_rate: return the lockin sample rate from the ledit input.
        """
        return {"sr510": float(self.sr510_manual_lockin_samplerate_combobox.currentText()),
                "sr830": float(self.sr830_manual_lockin_samplerate_combobox.currentText())}

    def set_sample_rate(self, sr_dict):
        for key in sr_dict:
            sr = str(sr_dict[key])
            if key == "sr510":
                self.sr510_manual_lockin_samplerate_combobox.setCurrentText(sr)
            elif key == "sr830":
                self.sr830_manual_lockin_samplerate_combobox.setCurrentText(sr)

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

    # PRIVATE METHODS ######################################################################################
    #########################################################################################################

