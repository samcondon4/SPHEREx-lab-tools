"""automationTab:

    This module ties together all of the automated instrument control windows into a single PyQt Widget.

Sam Condon, 08/16/2021
"""


import asyncio
import os
from configparser import ConfigParser
from qasync import QEventLoop
from PyQt5 import QtWidgets
from pylabgui.pylabgui_window_base import GuiCompositeWindow
from pylabgui.CS260Window.cs260AutoDialogWrapper import CS260AutoWindow
from pylabgui.LockinWindow.lockinAutoWindowDialogWrapper import LockinAutoWindow
from pylabgui.LockinWindow.lockinWindowHelper import Lockin
from pylabgui.NDFWheelWindow.ndfAutoWindowDialogWrapper import NDFAutoWindow
from pylabgui.NDFWheelWindow.ndfWindowHelper import NDF
from pylabgui.SeriesConstruction.seriesconstructionWindowDialogWrapper import SeriesConstructionWindow


class AutoTab(GuiCompositeWindow):

    def __init__(self, sequence_dir=None, **kwargs):
        super().__init__(child=self, window_type="stacked", **kwargs)
        self.sequence_dir = sequence_dir
        self.proc_queue = asyncio.Queue()
        self.form.setWindowTitle("Automation")
        self.cs260_sequence_window = CS260AutoWindow(identifier="Cs260 Auto")
        self.lockin_sequence_window = LockinAutoWindow(identifier="Lockin Auto")
        self.ndf_sequence_window = NDFAutoWindow(identifier="NDF Auto")
        self.series_window = SeriesConstructionWindow(identifier="Series Construction", **kwargs)
        self.add_window(self.series_window)
        self.add_window(self.cs260_sequence_window)
        self.add_window(self.lockin_sequence_window)
        self.add_window(self.ndf_sequence_window)
        if not self.configured:
            self.configure()
        self.WidgetGroups["saved sequences"].set_list_setter_proc(self.savedsequences_list_item_proc)
        self.WidgetGroups["saved sequences"].set_setter_proc(self.passive_sequence_setter_proc)
        self.WidgetGroups["series"].set_list_setter_proc(self.series_list_item_proc)
        self.WidgetGroups["series"].set_setter_proc(self.passive_series_setter_proc)
        if self.sequence_dir is not None:
            self.load_sequences()

    def load_sequences(self):
        for seq_file in os.listdir(self.sequence_dir):
            if seq_file.endswith(".ini"):
                seq_dict = self.get_sequence_dict(self.sequence_dir + seq_file)
                seq_dict["from ini"] = {}
                self.WidgetGroups["saved sequences"].set_list_item(external=seq_dict)

    # STATIC PROCESS METHODS AND HELPERS #############################################################################
    def savedsequences_list_item_proc(self, internal_sequence_dict, from_ini=False):
        if "from ini" not in list(internal_sequence_dict.keys()):
            text = internal_sequence_dict.pop("sequence name")
            sr510_tc = {}
            sr830_tc = {}
            isd_keys = list(internal_sequence_dict.keys())
            for key in isd_keys:
                tc_key = key.split(" ")[-1]
                if "sr510 time constant" in key:
                    sr510_tc[tc_key] = internal_sequence_dict.pop(key)
                elif "sr830 time constant" in key:
                    sr830_tc[tc_key] = internal_sequence_dict.pop(key)
            sr510_tc = Lockin.get_tc(sr510_tc)
            sr830_tc = Lockin.get_tc(sr830_tc)
            internal_sequence_dict["sr510 time constant"] = sr510_tc
            internal_sequence_dict["sr830 time constant"] = sr830_tc
            output_sequence_dict = self.save_ini(internal_sequence_dict, text)
            output_sequence_dict["from ini"] = {}
        else:
            text = internal_sequence_dict["sequence info"]["sequence name"]
            output_sequence_dict = internal_sequence_dict

        return text, output_sequence_dict

    def save_ini(self, seq_dict, seq_name):
        ini_seq_dict = {}
        for key in seq_dict:
            key_split = key.split(" ")
            ini_key1 = key_split[0]
            ini_key2 = ""
            for string in key_split[1:]:
                ini_key2 += string + " "
            if ini_key1 not in ini_seq_dict:
                ini_seq_dict[ini_key1] = {}
            ini_seq_dict[ini_key1][ini_key2[:-1]] = seq_dict[key]

        ini_seq_dict["sequence info"] = {"sequence name": seq_name}
        seq_file_name = self.sequence_dir + seq_name + ".ini"
        self.write_sequence_file(ini_seq_dict, seq_file_name)
        return ini_seq_dict

    @staticmethod
    def passive_sequence_setter_proc(ini_dict):
        proc_dict = {}
        for key1 in ini_dict:
            proc_dict[key1] = {}
            for key2 in ini_dict[key1]:
                proc_dict[key1][key2] = ini_dict[key1][key2]
        proc_dict_keys = list(proc_dict.keys())

        # Process lockin sensitivity transitions list ##########################
        if "sr510" in proc_dict_keys:
            proc_dict["sr510"] = Lockin.lockin_ini_dict_proc(proc_dict["sr510"])
        if "sr830" in proc_dict_keys:
            proc_dict["sr830"] = Lockin.lockin_ini_dict_proc(proc_dict["sr830"])
        if "ndf" in proc_dict_keys:
            proc_dict["ndf"] = NDF.ndf_ini_dict_proc(proc_dict["ndf"])
        #########################################################################

        proc_dict.pop("from ini")
        text = proc_dict["sequence info"]["sequence name"]
        proc_dict.pop("sequence info")
        output_dict = {"sequence name": text}
        for key1 in proc_dict:
            for key2 in proc_dict[key1]:
                new_key = key1 + " " + key2
                output_dict[new_key] = proc_dict[key1][key2]

        return text, output_dict

    @staticmethod
    def passive_series_setter_proc(ini_dict):
        text = ini_dict["sequence info"]["sequence name"]
        data = {"sequence": text}
        return text, data

    @staticmethod
    def series_list_item_proc(sequence_dict):
        sequence = sequence_dict["sequence"]
        text = sequence["sequence info"]["sequence name"]
        return text, sequence

    @staticmethod
    def get_sequence_dict(param_file_path):
        config = ConfigParser()
        config.read(param_file_path)

        dict_out = {}
        for section in config.sections():
            dict_sect = {}
            for (each_key, each_val) in config.items(section):
                dict_sect[each_key] = each_val

            dict_out[section] = dict_sect

        return dict_out

    @staticmethod
    def write_sequence_file(params_out, config_filename_out):
        config_out = ConfigParser()
        for ikey, idict in params_out.items():
            if not config_out.has_section(ikey):

                config_out.add_section(ikey)
                for isect, ivals in idict.items():
                    # pdb.set_trace()
                    # print(ikey, isect, ivals)
                    config_out.set(ikey, isect, str(ivals))

        with open(config_filename_out, 'w') as conf:
            config_out.write(conf)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    seq_dir = "..\\config\\sequence\\"
    window = AutoTab(sequence_dir=seq_dir)
    window.form.show()
    asyncio.create_task(window.run())
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())

