"""powermaxLiveWindowDialogWrapper:

    This module provides a wrapper class, PowermaxWindow, around the powermaxLiveWindowDialog that was
    generated using Qt-Designer. This module also embeds the live updating Matplotlib plot of power read
    from the sensor

Sam Condon, 07/02/2021
"""
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from pylabcal.pylabcalgui.PowermaxWindow.powermaxLiveWindowDialog import Ui_Form
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

sys.path.append(r"..\\..\\..\\")
from pylablib.pylablib_gui_tab import GuiTab


class PowerPlot(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=200):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, xlabel="Time (a.u.)", ylabel="Watts")
        super(PowerPlot, self).__init__(self.fig)
        self.toolbar = NavigationToolbar2QT(self, self)


class PowermaxWindow(Ui_Form, GuiTab):

    def __init__(self):
        super(PowermaxWindow, self).__init__(self)
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        # Create plot and navigation toolbar ######################
        self.power_plot = PowerPlot()
        self.ydata = []
        self.xdata = []
        self._plot_ref = None
        ###########################################################

        # Add plot and toolbar to the layout ######################
        self.gridLayout_2.addWidget(self.power_plot.toolbar)
        self.gridLayout_2.addWidget(self.power_plot)
        ###########################################################

        # Configure parameters ##########################################################################
        self.add_parameter("active wavelength", self.get_active_wavelength, self.set_active_wavelength)
        self.add_parameter("data", self.get_data, self.set_data)
        self.add_parameter("data append", self.get_data_append, self.set_data_append)
        #################################################################################################

        # Connect buttons to methods ####################################################################
        self.powermax_livedisplay_startstop_button.clicked.connect(self._on_acquisition)
        self.powermax_zerosensor_button.clicked.connect(self._on_zero)
        #################################################################################################

    # PARAMETER GETTER/SETTERS #####################################################
    def set_active_wavelength(self, wave):
        self.powermax_livedisplay_activewavelength_ledit.setText(wave)

    def get_active_wavelength(self):
        return self.powermax_livedisplay_activewavelength_ledit.text()

    def set_data(self, data_arr):
        self.ydata = data_arr
        self.xdata = np.arange(len(data_arr))
        self.power_plot.axes.cla()
        self.power_plot.axes.plot(self.xdata, self.ydata)
        self.power_plot.axes.set_xlabel("Time (a.u.)")
        self.power_plot.axes.set_ylabel("Watts")
        #self.power_plot.draw()

    def get_data(self):
        return self.ydata

    def set_data_append(self, data_append, max_length=1500):
        self.ydata.append(data_append)
        if len(self.xdata) == 0:
            self.xdata.append(0)
        else:
            self.xdata.append(self.xdata[-1] + 1)

        if len(self.ydata) > max_length:
            self.ydata = self.ydata[1:]
            self.xdata = self.xdata[1:]

        self.power_plot.axes.cla()
        self.power_plot.axes.plot(self.xdata, self.ydata)
        self.power_plot.axes.set_ylim(bottom=-1*1e-3, top=1e-3)
        self.power_plot.axes.set_xlabel("Time (a.u.)")
        self.power_plot.axes.set_ylabel("Watts")

        # Attempt at creating an updating plot w/o redrawing the entire figure every time. Not working yet...
        """
        if self._plot_ref is None:
            self._plot_ref, = self.power_plot.axes.plot(self.xdata, self.ydata)
        else:
            if len(self.ydata) > max_length:
                self._plot_ref.set_ydata(self.ydata[-1*max_length:-1])
                self._plot_ref.set_xdata(self.xdata[-1*max_length:-1])
            else:
                self._plot_ref.set_ydata(self.ydata)
                self._plot_ref.set_xdata(self.xdata)
        """

        self.power_plot.draw()

    def get_data_append(self):
        return self.ydata[-1]
    ################################################################################

    # Button methods ###############################################################
    def _on_acquisition(self):
        acquisition_text = self.powermax_livedisplay_startstop_button.text()
        if acquisition_text == "Start Acquisition":
            self.powermax_livedisplay_startstop_button.setText("Stop Acquisition")
        elif acquisition_text == "Stop Acquisition":
            self.powermax_livedisplay_startstop_button.setText("Start Acquisition")
        self.button_queue.put(acquisition_text)

    def _on_zero(self):
        self.button_queue.put("Zero Sensor")
    ################################################################################


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PowermaxWindow()
    window.form.show()
    sys.exit(app.exec_())
