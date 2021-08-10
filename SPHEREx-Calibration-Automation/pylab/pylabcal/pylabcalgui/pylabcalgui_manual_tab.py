"""pylabcalgui_manual_tab:

    This module ties together all of the manual instrument control windows into a single QtWidget

Sam Condon, 08/09/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.CS260Window.cs260DialogWrapper import CS260Window
from pylabcal.pylabcalgui.LockinWindow.lockinWindowDialogWrapper import LockinWindow
from pylabcal.pylabcalgui.NDFWheelWindow.ndfWheelDialogWrapper import NDFWindow
from pylabcal.pylabcalgui.LabJackWindow.labjackWindowDialogWrapper import LabjackWindow


class ManualTab(GuiTab):

    def __init__(self, instruments=None):
        self.form = QtWidgets.QStackedWidget()
        if instruments is None:
            self.instruments = ["Monochromator", "Lockin", "NDF", "Labjack"]
        super().__init__(self)
        # Configure parameters ###########################################################

        ##################################################################################

        # Configure button methods #######################################################

        ##################################################################################

        # Add all specified instrument manual control windows ############################
        if "Monochromator" in self.instruments:
            self.cs260_window = CS260Window()
            self.form.addWidget(self.cs260_window.form)
        if "Lockin" in self.instruments:
            self.lockin_window = LockinWindow()
            self.form.addWidget(self.lockin_window.form)
        if "NDF" in self.instruments:
            self.ndf_window = NDFWindow()
            self.form.addWidget(self.ndf_window.form)
        if "Labjack" in self.instruments:
            self.labjack_window = LabjackWindow()
            self.form.addWidget(self.labjack_window.form)
        ##################################################################################

        self.configure_stacked_widget_switch()

    # PARAMETER GETTER/SETTERS #######################################################

    ##################################################################################

    # PRIVATE METHODS ################################################################

    ##################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ManualTab()
    window.form.show()
    sys.exit(app.exec_())
