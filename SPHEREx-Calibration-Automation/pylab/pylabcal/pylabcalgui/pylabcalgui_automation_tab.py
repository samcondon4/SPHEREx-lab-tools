"""pylabcalgui_automation_tab:

    This module ties together all of the automation tabs in the gui setup.

Sam Condon, 08/04/2021
"""


import os
import asyncio
from qasync import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab
from pylablib.utils.parameters import get_params_dict, write_config_file
from pylabcal.pylabcalgui.SeriesConstruction.seriesconstructionWindowDialogWrapper import SeriesConstructionWindow
from pylabcal.pylabcalgui.NDFWheelWindow.ndfAutoWindowDialogWrapper import NDFAutoWindow
from pylabcal.pylabcalgui.CS260Window.cs260AutoDialogWrapper import CS260AutoWindow
from pylabcal.pylabcalgui.LockinWindow.lockinAutoWindowDialogWrapper import LockinAutoWindow


class AutomationTab(GuiTab):

    def __init__(self, root_path, seq_config_path, instruments=None):
        self.root_path = root_path
        self.seq_config_path = seq_config_path
        if instruments is None:
            self.instruments = ["Monochromator", "Lockin", "NDF"]
        else:
            self.instruments = instruments
        self.form = QtWidgets.QStackedWidget()

        self.seq_files = []
        self.series = []

        self.auto_queue_key = "Auto"
        GuiTab.add_button_queue(self.auto_queue_key)
        self.series_window = SeriesConstructionWindow(root_path, seq_config_path, button_queue_keys=[self.auto_queue_key])
        self.form.addWidget(self.series_window.form)
        super().__init__(self, button_queue_keys=[self.auto_queue_key])

        # Configure parameters ############################################################################
        self.add_parameter("Series", self.get_series, self.set_series)
        ###################################################################################################

        # Add all specified instrument automation control windows #########################################
        if "Monochromator" in self.instruments:
            self.cs260_window = CS260AutoWindow()
            self.form.addWidget(self.cs260_window.form)
            self.add_parameter("Monochromator", self.get_auto_monochromator, self.set_auto_monochromator)

        if "Lockin" in self.instruments:
            self.lockin_window = LockinAutoWindow()
            self.form.addWidget(self.lockin_window.form)
            self.add_parameter("Lockin", self.get_auto_lockin, self.set_auto_lockin)

        if "NDF" in self.instruments:
            self.ndf_window = NDFAutoWindow()
            self.form.addWidget(self.ndf_window.form)
            self.add_parameter("NDF", self.get_auto_ndf, self.set_auto_ndf)
        ####################################################################################################

        self.configure_stacked_widget_switch()

        # Load saved sequence files and set initial instrument window states############################################
        for seq_file in os.listdir(self.root_path + self.seq_config_path):
            if seq_file.endswith(".ini"):
                seq_file_data = get_params_dict(self.root_path + self.seq_config_path + seq_file)
                self.seq_files.extend([seq_file_data])

        cur_seq = self.seq_files[0]
        self.series_window.set_parameters({"Sequence List": [s["Sequence Info"]["sequence name"]
                                                             for s in self.seq_files],
                                           "Current Sequence": cur_seq["Sequence Info"]["sequence name"]})
        ##############################################################################################################

    async def run(self):
        """run: Executes main functionality of the automation tab
        """
        while True:
            button_press = self.get_button(self.auto_queue_key)
            if button_press is not False:
                button_method_str = button_press.replace(" ", "_")
                try:
                    button_method = getattr(self, "_on_{}".format(button_method_str))
                except AttributeError as e:
                    pass
                else:
                    button_method()

            await asyncio.sleep(0)

    # BUTTON PRESS EXECUTION METHODS ########################################################################
    def _on_Save_New_Sequence(self):
        """_on_Save_New_Sequence: Executes when the "Save New Sequence" button is pressed. Gets sequence parameters
                                  from all instrument windows present and writes all parameters out to a new .ini
                                  sequence file.
        """
        sequence = {}
        seq_cfg_params = self.series_window.get_parameters(["Sequence Info", "Data Configuration",
                                                            "Metadata Configuration"])
        sequence["Sequence Info"] = seq_cfg_params["Sequence Info"]
        sequence["Data Configuration"] = seq_cfg_params["Data Configuration"]
        sequence["Metadata Configuration"] = seq_cfg_params["Metadata Configuration"]
        if "Monochromator" in self.instruments:
            mono_params = self.cs260_window.get_parameters("All")
            sequence["Monochromator"] = mono_params
        if "Lockin" in self.instruments:
            lockin_params = self.lockin_window.get_parameters("All")
            lockin_params.pop("sr830 sensitivity")
            lockin_params.pop("sr510 sensitivity")
            sequence["Lock-In"] = lockin_params
        if "NDF" in self.instruments:
            ndf_params = self.ndf_window.get_parameters("All")
            sequence["NDF"] = ndf_params

        seq_file_name = seq_cfg_params["Sequence Info"]["sequence name"] + ".ini"
        write_config_file(sequence, self.root_path + self.seq_config_path + seq_file_name)

    def _on_Run_Series(self):
        print("_on_Run_Series")

    def _on_Pause_Series(self):
        print("_on_Pause_Series")

    def _on_Abort_Series(self):
        print("_on_Abort_Series")

    def _on_Sequence_Select(self):
        cur_seq = self.series_window.get_parameters(["Current Sequence"])["Current Sequence"]
        cur_seq_params = get_params_dict(self.root_path + self.seq_config_path + cur_seq + ".ini")
        self.series_window.set_parameters({"Sequence Info": cur_seq_params["Sequence Info"],
                                           "Data Configuration": cur_seq_params["Data Configuration"],
                                           "Metadata Configuration": cur_seq_params["Metadata Configuration"]})
        self.cs260_window.set_parameters(cur_seq_params["Monochromator"])
        self.lockin_window.set_parameters(cur_seq_params["Lock-In"])
        self.ndf_window.set_parameters(cur_seq_params["NDF"])

    def _on_Series_Sequence_Select(self):
        cur_ser_seq = self.series_window.get_parameters(["Current Series Sequence"])["Current Series Sequence"]
        print("_on_Series_Sequence_Selection")
    #########################################################################################################

    # PARAMETER GETTER/SETTERS ##############################################################################
    def get_series(self):
        pass

    def set_series(self):
        pass

    def get_auto_monochromator(self):
        return self.cs260_window.get_parameters("All")

    def set_auto_monochromator(self, params_dict):
        self.cs260_window.set_parameters(params_dict)

    def get_auto_lockin(self):
        return self.lockin_window.get_parameters("All")

    def set_auto_lockin(self, params_dict):
        self.lockin_window.set_parameters(params_dict)

    def get_auto_ndf(self):
        return self.ndf_window.get_parameters("All")

    def set_auto_ndf(self, params_dict):
        self.ndf_window.set_parameters(params_dict)
    #########################################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    root_dir = "C:\\Users\\thoma\\Documents\\Github\\SPHEREx-lab-tools\\SPHEREx-Calibration-Automation\\pylab\\"
    seq_cfg_dir = "\\pylabcal\\config\\sequence\\"
    window = AutomationTab(root_dir, seq_cfg_dir)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    window.form.show()
    asyncio.create_task(window.run())
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())


