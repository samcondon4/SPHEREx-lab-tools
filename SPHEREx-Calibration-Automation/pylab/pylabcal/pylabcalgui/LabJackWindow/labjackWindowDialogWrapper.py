"""labjackWindowDialogWrapper:

    This module provides a wrapper class, LabjackWindow, around the labjackWindowDialog created
    using QT-Designer. LabjackWindow follows the SXTC-SWS GUI Tab API format.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.LabJackWindow.labjackWindowDialog import Ui_Form


class LabjackWindow(Ui_Form, GuiTab):

    def __init__(self):
        super().__init__(self)
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        # Configure parameters ######################################################
        self.add_parameter("LabJack", self.get_labjack_parameters, self.set_labjack_parameters)
        #############################################################################

        ##Connect buttons to methods #######################################################################
        self.manual_labjack_dio0state_check.stateChanged.connect(self._on_dio0state_Changed)
        self.manual_labjack_dio1state_check.stateChanged.connect(self._on_dio1state_Changed)
        self.manual_labjack_dio2state_check.stateChanged.connect(self._on_dio2state_Changed)
        self.manual_labjack_dio0config_cbox.currentIndexChanged.connect(self._on_dio0config_Changed)
        self.manual_labjack_dio1config_cbox.currentIndexChanged.connect(self._on_dio1config_Changed)
        self.manual_labjack_dio2config_cbox.currentIndexChanged.connect(self._on_dio2config_Changed)
        #####################################################################################################

    # PARAMETER GETTERS/SETTERS #################################################
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

    #############################################################################

    ##PRIVATE METHODS################################################################################################
    # Button Methods#####
    def _on_dio0state_Changed(self):
        """_on_dio0state_Changed: Execute when the dio0 check state changes. Place "Checked" or "Unchecked" on the
           button queue depending on the new checkbox state.

        :return: None
        """
        if self.manual_labjack_dio0state_check.checkState():
            put_string = "Labjack Dio0 Checked"
        else:
            put_string = "Labjack Dio0 Unchecked"
        self.button_queue.put(put_string)
        GuiTab.GlobalButtonQueue.put(put_string)

    def _on_dio1state_Changed(self):
        """_on_dio1state_Changed: Execute when the dio0 check state changes. Place "Checked" or "Unchecked" on the
           button queue depending on the new checkbox state.

        :return: None
        """
        if self.manual_labjack_dio1state_check.checkState():
            put_string = "Labjack Dio1 Checked"
        else:
            put_string = "Labjack Dio1 Unchecked"
        self.button_queue.put(put_string)
        GuiTab.GlobalButtonQueue.put(put_string)

    def _on_dio2state_Changed(self):
        """_on_dio2state_Changed: Execute when the dio0 check state changes. Place "Checked" or "Unchecked" on the
           button queue depending on the new checkbox state.

        :return: None
        """
        if self.manual_labjack_dio2state_check.checkState():
            put_string = "Labjack Dio2 Checked"
        else:
            put_string = "Labjack Dio2 Unchecked"
        self.button_queue.put(put_string)
        GuiTab.GlobalButtonQueue.put(put_string)

    def _on_dio0config_Changed(self):
        """_on_dio0config_Changed: Set labjack dio 0 to either input or output depending on user gui input.

        """
        put_string = "Labjack Config Dio0 {}".format(self.manual_labjack_dio0config_cbox.currentText())
        self.button_queue.put(put_string)
        GuiTab.GlobalButtonQueue.put(put_string)

    def _on_dio1config_Changed(self):
        """_on_dio1config_Changed: Set labjack dio 1 to either input or output depending on user gui input.

        """
        put_string = "Labjack Config Dio1 {}".format(self.manual_labjack_dio1config_cbox.currentText())
        self.button_queue.put(put_string)
        GuiTab.GlobalButtonQueue.put(put_string)

    def _on_dio2config_Changed(self):
        """_on_dio2config_Changed: Set labjack dio 0 to either input or output depending on user gui input.

        """
        put_string = "Labjack Config Dio2 {}".format(self.manual_labjack_dio2config_cbox.currentText())
        self.button_queue.put(put_string)
        GuiTab.GlobalButtonQueue.put(put_string)

    #################################################################################################################

