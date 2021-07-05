import sys
import os
import asyncio
from qasync import QEventLoop
import datetime
import time
from PyQt5 import QtWidgets, QtCore
from pylablib.housekeeping import Housekeeping
from pylablib.instruments.powermaxusb2 import Powermax
from pylabcal.pylabcalgui.PowermaxWindow.powermaxLiveWindowDialogWrapper import PowermaxWindow

# Configure housekeeping time synchronization ##############
Housekeeping.time_sync_method = datetime.datetime.now


class HousekeepingTester:

    def __init__(self, dialog):
        self.gridLayout = QtWidgets.QGridLayout(dialog)
        self.tabWidget = QtWidgets.QTabWidget(dialog)
        self.powermax_gui = PowermaxWindow()
        self.powermax = Powermax()
        self.powermax.open()

        self.tabWidget.addTab(self.powermax_gui.form, "Powermax")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        # Initialize gui display #######################
        active_wave = self.powermax.get_parameters("wavelength")
        self.powermax_gui.powermax_livedisplay_activewavelength_ledit.setText(str(active_wave["wavelength"]))
        ################################################

        asyncio.create_task(self.run_gui())

    async def run_gui(self):
        Housekeeping.start()
        powermax_logging = False
        while True:
            button = self.powermax_gui.get_button()
            if button == "Start Acquisition":
                await self.powermax.on_data_log()
                powermax_logging = True
            elif button == "Stop Acquisition":
                await self.powermax.off_data_log()
                powermax_logging = False

            if powermax_logging:
                get_log_task = asyncio.create_task(self.powermax.get_log(final_val=True))
                await get_log_task
                data = get_log_task.result()
                data = float(data["Watts"])
                self.powermax_gui.set_parameters({"data append": data})

            await asyncio.sleep(0.001)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    HK = HousekeepingTester(Dialog)
    Dialog.show()
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
