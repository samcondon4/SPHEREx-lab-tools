"""sequenceWindowDialogWrapper:

    This module provides a wrapper class, SequenceWindow, around the sequenceWindowDialog that was generated with
    QT-Designer. SequenceWindow follows the SXTC-SWS GUI Tab API format. Note that the current implementation of
    this window does not have any buttons, thus the get_button() and clear_button() methods are not included.

Sam Condon, 06/21/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from sequenceWindowDialog import Ui_Form
from queue import SimpleQueue


class SequenceWindow(Ui_Form):

    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)

        self.button_queue = SimpleQueue()
        self.params = {
            "Monochromator": {"start wavelength": None,
                              "stop wavelength": None,
                              "step size": None,
                              "g1 to g2 transition wavelength": None,
                              "no osf to osf1 transition wavelength": None,
                              "osf1 to osf2 transition wavelength": None,
                              "osf2 to osf3 transition wavelength": None},
            "Lock-In": {"sample frequency": None,
                        "sample time": None,
                        "time constant": None,
                        "sensitivity string": None}
        }

    ##MAIN API METHODS################################################################################################
    def get_params(self, params):
        """get_params: return the specified parameters as a dictionary

        :param:
            params: string, list of strings, or all to specify which parameters
                    should be returned.

        :return: dictionary of the desired parameters.
        """
        return_dict = {}

        self._update_params()
        if params == 'All':
            return_dict = self.params
        elif type(params) is str:
            return_dict = self.params[params]
        elif type(params) is list:
            for p in params:
                return_dict[p] = self.params[p]

        return return_dict

    def set_params(self, params_dict):
        """set_params: set the specified parameters in the display and parameters dictionary

        :param params_dict: dictionary with keys and values of parameters to update
        :return: None
        """
        for key1 in params_dict:
            for key2 in params_dict[key1]:
                try:
                    self.params[key1][key2] = params_dict[key1][key2]
                except KeyError as e:
                    print(e)
                else:
                    if key1 == "Monochromator" and key2 == "start wavelength":
                        self.sequence_monochromator_startwave_ledit.setText(self.params[key1][key2])
                    elif key1 == "Monochromator" and key2 == "stop wavelength":
                        self.sequence_monochromator_endwave_ledit.setText(self.params[key1][key2])
                    elif key1 == "Monochromator" and key2 == "step size":
                        self.sequence_monochromator_stepsize_ledit.setText(self.params[key1][key2])
                    elif key1 == "Monochromator" and key2 == "g1 to g2 transition wavelength":
                        self.sequence_monochromator_g1g2_ledit.setText(self.params[key1][key2])
                    elif key1 == "Monochromator" and key2 == "g2 to g3 transition wavelength":
                        self.sequence_monochromator_g2g3_ledit.setText(self.params[key1][key2])
                    elif key1 == "Monochromator" and key2 == "no osf to osf1 transition wavelength":
                        self.sequence_monochromator_noosfosf1_ledit.setText(self.params[key1][key2])
                    elif key1 == "Monochromator" and key2 == "osf1 to osf2 transition wavelength":
                        self.sequence_monochromator_osf1osf2_ledit.setText(self.params[key1][key2])
                    elif key1 == "Monochromator" and key2 == "osf2 to osf3 transition wavelength":
                        self.sequence_monochromator_osf2osf3_ledit.setText(self.params[key1][key2])
                    elif key1 == "Lock-In" and key2 == "sample frequency":
                        self.sequence_lockin_samplefreq_ledit.setText(self.params[key1][key2])
                    elif key1 == "Lock-In" and key2 == "sample time":
                        self.sequence_lockin_sampletime_ledit.setText(self.params[key1][key2])
                    elif key1 == "Lock-In" and key2 == "time constant":
                        self.sequence_lockin_timeconstant_ledit.setText(self.params[key1][key2])
                    elif key1 == "Lock-In" and key2 == "sensitivity string":
                        self.sequence_lockin_sensitivity_ledit.setText(self.params[key1][key2])

    def place(self, tab_widget):
        """place: places the dialog specified by this class into a tab widget.

        :param tab_widget: QTabWidget
        :return: None
        """
        tab_widget.addTab(self.form)

    #################################################################################################################

    ##PRIVATE METHODS################################################################################################
    def _update_params(self):
        """_update_params: update internal parameters dictionary

        :return: None
        """
        self.params['Monochromator']['start wavelength'] = self.sequence_monochromator_startwave_ledit.text()
        self.params['Monochromator']['stop wavelength'] = self.sequence_monochromator_endwave_ledit.text()
        self.params['Monochromator']['step size'] = self.sequence_monochromator_stepsize_ledit.text()
        self.params['Monochromator']['g1 to g2 transition wavelength'] = self.sequence_monochromator_g1g2_ledit.text()
        self.params['Monochromator']['G2 to G3 Transition Wavelength'] = self.sequence_monochromator_g2g3_ledit.text()
        self.params['Monochromator']['no osf to osf1 transition wavelength'] = self.sequence_monochromator_noosfosf1_ledit\
                                                                               .text()
        self.params['Monochromator']['osf2 to osf3 transition wavelength'] = self.sequence_monochromator_osf2osf3_ledit\
                                                                             .text()
        self.params['Lock-In']['sample frequency'] = self.sequence_lockin_samplefreq_ledit.text()
        self.params['Lock-In']['sample time'] = self.sequence_lockin_sampletime_ledit.text()
        self.params['Lock-In']['time constant'] = self.sequence_lockin_timeconstant_ledit.text()
        self.params['Lock-In']['sensitivity string'] = self.sequence_lockin_sensitivity_ledit.text()
    #################################################################################################################
