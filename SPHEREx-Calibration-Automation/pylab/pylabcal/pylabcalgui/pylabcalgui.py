"""qtwindow_skeleton:

    This module provides a skeleton for creating PyQt5 window wrappers

Sam Condon, 08/03/2021
"""

import asyncio
from qasync import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylabcal.pylabcalgui.pylabcalgui_manual_tab import ManualTab
from pylabcal.pylabcalgui.pylabcalgui_automation_tab import AutomationTab


class GUI(GuiTab):

    def __init__(self, root_path, seq_config_path, instruments=None):
        # initialize attributes ##################################################
        self.root_path = root_path
        self.seq_config_path = seq_config_path
        if instruments is None:
            self.instruments = ["Monochromator", "Lockin", "NDF", "Labjack"]
        else:
            self.instruments = instruments
        ##########################################################################

        # Configure main button queue ################
        self.main_queue_key = "Main"
        GuiTab.add_button_queue(self.main_queue_key)
        ##############################################

        # Instantiate manual and automation windows ###############################################
        self.form = QtWidgets.QTabWidget()
        self.manual = ManualTab(instruments=self.instruments, button_queue_keys=[self.main_queue_key],)
        #self.auto = AutomationTab(root_path=self.root_path, seq_config_path=self.seq_config_path,
        #                          instruments=self.instruments, button_queue_keys=[self.main_queue_key])
        #self.timestream
        #self.status
        #self.form.addTab(self.auto.form, self.auto.form.windowTitle())
        self.form.addTab(self.manual.form, self.manual.form.windowTitle())
        self.layout = QtWidgets.QGridLayout(self.form)
        ###########################################################################################

        super().__init__(self, button_queue_keys=[self.main_queue_key])

        # Configure parameters ###########################################################

        ##################################################################################

        # Configure button methods #######################################################

        ##################################################################################

    async def run(self):
        """run: Begins GUI execution.
        """
        # initiate tab execution #
        #asyncio.create_task(self.auto.run())
        #await self.manual.run() #manual tab has no run function right now (not needed so far)
        while True:
            main_button_press = self.get_button(self.main_queue_key)
            if main_button_press is not False:
                tab = main_button_press["Tab"]
                getset = main_button_press["Get/Set"]
                instrument = main_button_press["Instrument"]
                param = main_button_press["Parameter"]
                if tab == "manual" and getset == "get":
                    get_params = self.manual.get_parameters(instrument, arg=param)
                    print(get_params)
            await asyncio.sleep(0)

    # PARAMETER GETTER/SETTERS #######################################################

    ##################################################################################

    # PRIVATE METHODS ################################################################

    ##################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    event_loop = QEventLoop()
    asyncio.set_event_loop(event_loop)
    root_dir = "C:\\Users\\thoma\\Documents\\Github\\SPHEREx-lab-tools\\SPHEREx-Calibration-Automation\\pylab\\"
    seq_cfg_dir = "\\pylabcal\\config\\sequence\\"
    window = GUI(root_path=root_dir, seq_config_path=seq_cfg_dir)
    window.form.show()
    asyncio.create_task(window.run())
    with event_loop:
        event_loop.run_forever()
        event_loop.close()
    sys.exit(app.exec_())
