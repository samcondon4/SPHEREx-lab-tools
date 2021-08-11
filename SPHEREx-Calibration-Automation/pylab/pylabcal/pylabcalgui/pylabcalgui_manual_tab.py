"""pylabcalgui_manual_tab:

    This module ties together all of the manual instrument control windows into a single QtWidget

Sam Condon, 08/09/2021
"""

import asyncio
from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.CS260Window.cs260DialogWrapper import CS260Window
from pylabcal.pylabcalgui.LockinWindow.lockinWindowDialogWrapper import LockinWindow
from pylabcal.pylabcalgui.NDFWheelWindow.ndfWheelDialogWrapper import NDFWindow
from pylabcal.pylabcalgui.LabJackWindow.labjackWindowDialogWrapper import LabjackWindow


class ManualTab(GuiTab):

    def __init__(self, instruments=None, button_queue_keys=None):
        self.form = QtWidgets.QStackedWidget()
        self.form.setWindowTitle("Manual")
        if instruments is None:
            self.instruments = ["Monochromator", "Lockin", "NDF", "Labjack"]
        else:
            self.instruments = instruments
        self.button_queue_keys = button_queue_keys
        if type(self.button_queue_keys) is str:
            self.button_queue_keys = [button_queue_keys]
        super().__init__(self, button_queue_keys=button_queue_keys)
        # Configure parameters ###########################################################
        self.add_parameter("monochromator", self.get_mono_params, self.set_mono_params)
        self.add_parameter("sr510", self.get_sr510_params, self.set_sr510_params)
        self.add_parameter("sr830", self.get_sr830_params, self.set_sr830_params)
        self.add_parameter("ndf", self.get_ndf_params, self.set_ndf_params)
        self.add_parameter("labjack", self.get_labjack_params, self.set_labjack_params)
        ##################################################################################

        # Configure button methods #######################################################

        ##################################################################################

        # Add all specified instrument manual control windows ############################
        if "Monochromator" in self.instruments:
            self.cs260_window = CS260Window(button_queue_keys=self.button_queue_keys)
            self.form.addWidget(self.cs260_window.form)
        if "Lockin" in self.instruments:
            self.lockin_window = LockinWindow(button_queue_keys=self.button_queue_keys)
            self.form.addWidget(self.lockin_window.form)
        if "NDF" in self.instruments:
            self.ndf_window = NDFWindow(button_queue_keys=self.button_queue_keys)
            self.form.addWidget(self.ndf_window.form)
        if "Labjack" in self.instruments:
            self.labjack_window = LabjackWindow(button_queue_keys=self.button_queue_keys)
            self.form.addWidget(self.labjack_window.form)
        ##################################################################################

        self.configure_stacked_widget_switch()

    # PARAMETER GETTER/SETTERS #######################################################
    def get_mono_params(self, params):
        return self.cs260_window.get_parameters(params)

    def set_mono_params(self, mono_dict):
        self.cs260_window.set_parameters(mono_dict)

    def get_sr510_params(self, params):
        lockin_params = self.lockin_window.get_parameters(params)[params]
        sr510_dict = {}
        for key in lockin_params:
            sr510_dict[key] = lockin_params[key]["sr510"]
        return sr510_dict

    def set_sr510_params(self, sr510_dict):
        pass

    def get_sr830_params(self, params):
        lockin_params = self.lockin_window.get_parameters(params)[params]
        sr830_dict = {}
        for key in lockin_params:
            sr830_dict[key] = lockin_params[key]["sr830"]
        return sr830_dict

    def set_sr830_params(self, sr830_dict):
        pass

    def get_labjack_params(self, params):
        return self.labjack_window.get_parameters(params)

    def set_labjack_params(self, labjack_dict):
        self.labjack_window.set_parameters(labjack_dict)

    def get_ndf_params(self, params):
        return self.ndf_window.get_parameters(params)

    def set_ndf_params(self, ndf_dict):
        self.ndf_window.set_parameters(ndf_dict)
    ##################################################################################

    # PRIVATE METHODS ################################################################

    ##################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ManualTab()
    window.form.show()
    sys.exit(app.exec_())
