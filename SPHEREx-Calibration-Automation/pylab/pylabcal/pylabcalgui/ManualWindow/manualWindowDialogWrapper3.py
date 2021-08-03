"""manualWindowDialogWrapper:

    This module provides a wrapper class, ManualWindow, that ties together all of the instrument manual control windows.

Sam Condon, 08/02/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.CS260Window.cs260DialogWrapper import CS260Window
from pylabcal.pylabcalgui.LockinWindow.lockinWindowDialogWrapper import LockinWindow
from pylabcal.pylabcalgui.LabJackWindow.labjackWindowDialogWrapper import LabjackWindow
from pylabcal.pylabcalgui.NDFWheelWindow.ndfWheelDialogWrapper import NDFWindow


class ManualWindow(GuiTab):

    def __init__(self):
        self.is_stacked_widget = True
        # instantiate all manual instrument control windows ############
        self.form = QtWidgets.QStackedWidget()
        self.cs260_tab = CS260Window()
        self.lockin_tab = LockinWindow()
        self.labjack_tab = LabjackWindow()
        self.ndf_tab = NDFWindow()
        ################################################################

        # setup stacked widget #########################################
        self.form.addWidget(self.cs260_tab.form)
        self.form.addWidget(self.lockin_tab.form)
        self.form.addWidget(self.labjack_tab.form)
        self.form.addWidget(self.ndf_tab.form)
        ###############################################################

        super().__init__(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Window = ManualWindow()
    Window.form.show()
    sys.exit(app.exec_())
