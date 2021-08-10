"""cs260DialogWrapper:

    This module provides a wrapper class, CS260Window, around the cs260Dialog that
    was generated using QT-Designer. The CS260Window follows the SXTC-SWS GUI Tab API
    format.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
import pylabcal.pylabcalgui.CS260Window.cs260Dialog as MonoDialog


class CS260Window(MonoDialog.Ui_Form, GuiTab):

    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)
        super().__init__(self)

        # Configure parameters ####################################################################################
        self.add_parameter("current wavelength", self.get_current_wavelength, self.set_current_wavelength)
        self.add_parameter("current osf", self.get_current_osf, self.set_current_osf)
        self.add_parameter("current grating", self.get_current_grating, self.set_current_grating)
        self.add_parameter("current shutter", self.get_current_shutter, self.set_current_shutter)
        self.add_parameter("new wavelength", self.get_new_wavelength, self.set_new_wavelength)
        self.add_parameter("new osf", self.get_new_osf, self.set_new_osf)
        self.add_parameter("new grating", self.get_new_grating, self.set_new_grating)
        self.add_parameter("new shutter", self.get_new_shutter, self.set_new_shutter)
        ###########################################################################################################

        # Connect buttons to methods ##############################################################################
        #self.manual_monochromator_setparams_button.clicked.connect(self._on_Set_Monochromator_Parameters)
        ###########################################################################################################

    # PARAMETER GETTERS/SETTERS########################################################################################
    def get_current_wavelength(self):
        return self.manual_monochromator_currentwavelength_ledit.text()

    def set_current_wavelength(self, wave):
        twave = type(wave)
        if twave is float or twave is int:
            self.manual_monochromator_currentwavelength_ledit.setText(str(wave))
        elif twave is str:
            self.manual_monochromator_currentwavelength_ledit.setText(wave)

    def get_current_osf(self):
        return self.manual_monochromator_currentfilter_combobox.currentText()

    def set_current_osf(self, osf):
        if type(osf) is str:
            self.manual_monochromator_currentfilter_combobox.setCurrentText(osf)

    def get_current_grating(self):
        return self.manual_monochromator_currentgrating_combobox.currentText()

    def set_current_grating(self, cg):
        if type(cg) is str:
            self.manual_monochromator_currentgrating_combobox.setCurrentText(cg)

    def get_current_shutter(self):
        return self.manual_monochromator_currentshutter_combobox.currentText()

    def set_current_shutter(self, shutter):
        if type(shutter) is str:
            self.manual_monochromator_currentshutter_combobox.setCurrentText(shutter)

    def get_new_wavelength(self):
        return self.manual_monochromator_newwavelength_ledit.text()

    def set_new_wavelength(self, wave):
        twave = type(wave)
        if twave is float or twave is int:
            self.manual_monochromator_newwavelength_ledit.setText(str(wave))
        elif twave is str:
            self.manual_monochromator_newwavelength_ledit.setText(wave)

    def get_new_osf(self):
        return self.manual_monochromator_newfilter_combobox.currentText()

    def set_new_osf(self, osf):
        if type(osf) is str:
            self.manual_monochromator_newfilter_combobox.setCurrentText(osf)

    def get_new_grating(self):
        return self.manual_monochromator_currentgrating_combobox.currentText()

    def set_new_grating(self, grat):
        if type(grat) is str:
            self.manual_monochromator_currentgrating_combobox.setCurrentText(grat)

    def get_new_shutter(self):
        return self.manual_monochromator_newshutter_combobox.currentText()

    def set_new_shutter(self, shutter):
        if type(shutter) is str:
            self.manual_monochromator_newshutter_combobox.setCurrentText(shutter)

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

    ######################################################################################

    ##PRIVATE METHODS ##################################################################
    # Button Methods ###########################
    def _on_Set_Monochromator_Parameters(self):
        """_on_Set_Parameters: Add the Set Parameters button identifier to button queue

        :return: None
        """
        set_string = "Monochromator Set Parameters"
        self.button_queue.put(set_string)
        GuiTab.GlobalButtonQueue.put(set_string)
    #####################################################################################
