"""pylabcalgui_automation_tab:

    This module ties together all of the automation tabs in the gui setup.

Sam Condon, 08/04/2021
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.SeriesConstruction.seriesconstructionWindowDialogWrapper import SeriesConstructionWindow
from pylabcal.pylabcalgui.NDFWheelWindow.ndfAutoWindowDialogWrapper import NDFAutoWindow
from pylabcal.pylabcalgui.CS260Window.cs260AutoDialogWrapper import CS260AutoWindow
from pylabcal.pylabcalgui.LockinWindow.lockinAutoWindowDialogWrapper import LockinAutoWindow


class AutomationTab(GuiTab):

    def __init__(self, root_path):
        super().__init__(self)
        self.form = QtWidgets.QStackedWidget()
        self.series_window = SeriesConstructionWindow(root_path)
        self.ndf_window = NDFAutoWindow()
        self.cs260_window = CS260AutoWindow()
        self.lockin_window = LockinAutoWindow()
        self.form.addWidget(self.series_window.form)
        self.form.addWidget(self.ndf_window.form)
        self.form.addWidget(self.cs260_window.form)
        self.form.addWidget(self.lockin_window.form)
        self.configure_stacked_widget_switch()
        self.configure_button_queues(use_local=True, use_global=False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    root_dir = "C:\\Users\\thoma\\Documents\\Github\\SPHEREx-lab-tools\\SPHEREx-Calibration-Automation\\pylab\\"
    window = AutomationTab(root_dir)
    window.form.show()
    sys.exit(app.exec_())


