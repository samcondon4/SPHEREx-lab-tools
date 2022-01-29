"""automationTab:

    This module ties together all of the automated instrument control windows into a single PyQt Widget.

Sam Condon, 08/16/2021
"""


import os
import json
import asyncio
from qasync import QEventLoop
from configparser import ConfigParser
from .NDFWheelWindow.ndfWindowHelper import NDF
from .LockinWindow.lockinWindowHelper import Lockin
from spherexlabtools.ui.windows import GuiCompositeWindow
from .LockinWindow.lockinAutoWindowDialogWrapper import *
from .CS260Window.cs260AutoDialogWrapper import CS260AutoWindow
from .NDFWheelWindow.ndfAutoWindowDialogWrapper import NDFAutoWindow
from .SeriesConstruction.seriesconstructionWindowDialogWrapper import SeriesConstructionWindow


class AutoTab(GuiCompositeWindow):

    def __init__(self, sequence_dir=None, **kwargs):
        super().__init__(child=self, window_type="stacked", **kwargs)
        self.sequence_dir = sequence_dir
        self.proc_queue = asyncio.Queue()
        self.form.setWindowTitle("Automation")
        self.cs260_sequence_window = CS260AutoWindow(rx_identifier="Cs260 Auto")
        self.lockin_sequence_window = LockinAutoWindow(rx_identifier="Sr830 Auto")
        self.ndf_sequence_window = NDFAutoWindow(rx_identifier="NDF Auto")
        self.series_window = SeriesConstructionWindow(rx_identifier="Series Construction", **kwargs)
        self.add_window(self.series_window)
        self.add_window(self.cs260_sequence_window)
        self.add_window(self.lockin_sequence_window)
        self.add_window(self.ndf_sequence_window)
        if not self.configured:
            self.configure()
        self.WidgetGroups["saved_sequences"].set_list_setter_proc(self.savedsequences_list_item_proc)
        self.WidgetGroups["saved_sequences"].set_setter_proc(self.passive_sequence_setter_proc)
        self.WidgetGroups["series"].set_list_setter_proc(self.series_list_item_proc)
        self.WidgetGroups["series"].set_setter_proc(self.passive_series_setter_proc)
        if self.sequence_dir is not None:
            self.load_sequences()

    def load_sequences(self):
        for seq_file in os.listdir(self.sequence_dir):
            if seq_file.endswith(".ini"):
                seq_dict = self.get_sequence_dict(self.sequence_dir + seq_file)
                seq_dict["from ini"] = {}
                self.WidgetGroups["saved_sequences"].set_list_item(external=seq_dict)

    # STATIC PROCESS METHODS AND HELPERS #############################################################################
    def savedsequences_list_item_proc(self, internal_sequence_dict, from_ini=False):
        if "from ini" not in list(internal_sequence_dict.keys()):
            text = internal_sequence_dict.pop("sequence_name")
            sr510_tc = {}
            sr830_tc = {}
            isd_keys = list(internal_sequence_dict.keys())
            for key in isd_keys:
                tc_key = key.split(self.Delimiter)[-1]
                if "sr510_time_constant" in key:
                    sr510_tc[tc_key] = internal_sequence_dict.pop(key)
                elif "sr830_time_constant" in key:
                    sr830_tc[tc_key] = internal_sequence_dict.pop(key)
            if not sr510_tc == {}:
                sr510_tc = Lockin.get_tc(sr510_tc)
                internal_sequence_dict["sr510_time_constant"] = sr510_tc
            if not sr830_tc == {}:
                sr830_tc = Lockin.get_tc(sr830_tc)
                internal_sequence_dict["sr830_time_constant"] = sr830_tc

            # set the thorlabs detectors sample rate to the fixed value of 1 Hz.
            # TODO: MOVE ALL THORLABS DETECTORS TO THEIR OWN WINDOW. THIS IS A HORRIBLE WAY OF DOING THIS...
            internal_sequence_dict["s401c_sample_rate"] = 1
            internal_sequence_dict["s122c_sample_rate"] = 1
            internal_sequence_dict["s120vc_sample_rate"] = 1

            output_sequence_dict = self.save_ini(internal_sequence_dict, text)
            output_sequence_dict["from ini"] = {}
        else:
            text = internal_sequence_dict["sequence info"]["sequence name"]
            output_sequence_dict = internal_sequence_dict

        return text, output_sequence_dict

    def save_ini(self, seq_dict, seq_name):
        ini_seq_dict = {}
        for key in seq_dict:
            key_split = key.split(self.Delimiter)
            ini_key1 = key_split[0]
            ini_key2 = ""
            for string in key_split[1:]:
                ini_key2 += string + " "
            if ini_key1 not in ini_seq_dict:
                ini_seq_dict[ini_key1] = {}
            ini_seq_dict[ini_key1][ini_key2[:-1]] = str(seq_dict[key])

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

        # Process cs260 grating and osf transitions list ########################
        if "cs260" in proc_dict_keys:
            cs260 = proc_dict["cs260"]
            grat = cs260["grating transitions"].replace("'", '"')
            grat = json.loads(grat)
            filt = cs260["osf transitions"].replace("'", '"')
            filt = json.loads(filt)
            new_grat = [0 for _ in grat]
            for i in range(len(grat)):
                trans = grat[i]
                new_trans = {"data": trans, "text": "wavelength = %s, grating = %s" % (trans["wavelength"],
                                                                                       trans["grating"])}
                new_grat[i] = new_trans
            new_filt = [0 for _ in filt]
            for i in range(len(filt)):
                trans = filt[i]
                new_trans = {"data": trans, "text": "wavelength = %s, osf = %s" % (trans["wavelength"],
                                                                                   trans["osf"])}
                new_filt[i] = new_trans
            proc_dict["cs260"]["grating transitions"] = new_grat
            proc_dict["cs260"]["osf transitions"] = new_filt
        #########################################################################

            proc_dict.pop("from ini")
            text = proc_dict["sequence info"]["sequence name"]
            proc_dict.pop("sequence info")
            output_dict = {"sequence_name": text}
            for key1 in proc_dict:
                for key2 in proc_dict[key1]:
                    new_key = key1 + " " + key2
                    output_dict[new_key.replace(" ", "_")] = proc_dict[key1][key2]

            return output_dict


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
                    config_out.set(ikey, isect, str(ivals))

        with open(config_filename_out, 'w') as conf:
            config_out.write(conf)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    if len(sys.argv) > 1: 
        seq_dir = sys.argv[1]
    else:
        raise RuntimeError("No valid sequence configuration directory specified!")
    data_queue_tx = asyncio.Queue()
    window = AutoTab(sequence_dir=seq_dir, data_queue_tx=data_queue_tx)
    window.form.show()
    asyncio.create_task(window.run())
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())

