"""lockinWindowDialogWrapper:

    This module provides a wrapper class, LockinWindow, around the lockinWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

import asyncio
from qasync import QEventLoop
from PyQt5 import QtWidgets
from .sr510Dialog import Ui_Sr510Dialog
from .sr830Dialog import Ui_Sr830Dialog
from .lockinWindowHelper import Lockin
from spherexlabtools.ui.windows import GuiWindow, GuiCompositeWindow


def lockin_getter_proc(lockin_input):
    lockin_keys = list(lockin_input.keys())
    sensitivity_dict = {"value": None, "multiplier": None, "units": None}
    timeconstant_dict = {"value": None, "multiplier": None, "units": None}
    inst = None
    if "sr510" in lockin_keys[0]:
        inst = "sr510"
        sensitivity_dict["value"] = lockin_input["sr510_new_sensitivity_value"]
        sensitivity_dict["multiplier"] = lockin_input["sr510_new_sensitivity_multiplier"]
        sensitivity_dict["units"] = lockin_input["sr510_new_sensitivity_units"]
        timeconstant_dict["value"] = lockin_input["sr510_new_time_constant_value"]
        timeconstant_dict["multiplier"] = lockin_input["sr510_new_time_constant_multiplier"]
        timeconstant_dict["units"] = lockin_input["sr510_new_time_constant_units"]
    elif "sr830" in lockin_keys[0]:
        inst = "sr830"
        sensitivity_dict["value"] = lockin_input["sr830_new_sensitivity_value"]
        sensitivity_dict["multiplier"] = lockin_input["sr830_new_sensitivity_multiplier"]
        sensitivity_dict["units"] = lockin_input["sr830_new_sensitivity_units"]
        timeconstant_dict["value"] = lockin_input["sr830_new_time_constant_value"]
        timeconstant_dict["multiplier"] = lockin_input["sr830_new_time_constant_multiplier"]
        timeconstant_dict["units"] = lockin_input["sr830_new_time_constant_units"]

    sensitivity = float(sensitivity_dict["value"]) * float(sensitivity_dict["multiplier"].split("x")[-1]) * \
                  float(Lockin.UNIT_SENSITIVITY_MAP[sensitivity_dict["units"]])
    tc = float(timeconstant_dict["value"]) * float(timeconstant_dict["multiplier"].split("x")[-1]) * \
         float(Lockin.UNIT_TC_MAP[timeconstant_dict["units"]])

    lockin_output = {"sensitivity": sensitivity, "time_constant": tc}
    return lockin_output


def lockin_measurement_setter_proc(in_dict):
    out_dict = {}
    for key in in_dict:
        key_str = ""
        key_split = key.split(GuiWindow.Delimiter)[1:]
        for string in key_split:
            key_str += string + GuiWindow.Delimiter
        key_str = key_str[:-1]
        if key_str == "sample_rate":
            sample_rate = float(in_dict[key])
            if sample_rate >= 1:
                sample_rate = int(sample_rate)
            out_dict[key] = str(sample_rate)
    return out_dict


class Sr510Window(Ui_Sr510Dialog, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()

        self.WidgetGroups["new_sr510_state"].set_getter_proc(lockin_getter_proc)
        self.WidgetGroups["new_sr510_measurement"].set_setter_proc(lockin_measurement_setter_proc)


class Sr830Window(Ui_Sr830Dialog, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()

        self.WidgetGroups["new_sr830_state"].set_getter_proc(lockin_getter_proc)
        self.WidgetGroups["new_sr830_measurement"].set_setter_proc(lockin_measurement_setter_proc)


class LockinWindow(GuiCompositeWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, window_type="tab", **kwargs)
        if "identifier" in list(kwargs.keys()):
            kwargs.pop("identifier")
        self.sr510_window = Sr510Window(rx_identifier="SR510", **kwargs)
        self.sr830_window = Sr830Window(rx_identifier="SR830", **kwargs)
        self.add_window(self.sr510_window)
        self.add_window(self.sr830_window)
        self.form.setWindowTitle("Lock-in Amplifiers")
        if not self.configured:
            self.configure()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    window = LockinWindow()
    window.form.show()
    asyncio.create_task(window.run())
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
