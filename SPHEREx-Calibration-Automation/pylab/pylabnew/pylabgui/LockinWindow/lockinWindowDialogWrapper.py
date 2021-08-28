"""lockinWindowDialogWrapper:

    This module provides a wrapper class, LockinWindow, around the lockinWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

import asyncio
from qasync import QEventLoop
from PyQt5 import QtWidgets
from pylabgui.LockinWindow.lockinWindowDialog import Ui_Form
from pylabgui.LockinWindow.lockinWindowHelper import Lockin
from pylabgui.pylabgui_window_base import GuiWindow


class LockinWindow(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()

        # add passive getter proc methods #
        self.WidgetGroups["sr510 new config parameters"].set_getter_proc(self.lockin_getter_proc)
        self.WidgetGroups["sr830 new config parameters"].set_getter_proc(self.lockin_getter_proc)

    def lockin_getter_proc(self, lockin_input):

        lockin_keys = list(lockin_input.keys())
        sensitivity_dict = {"value": None, "multiplier": None, "units": None}
        timeconstant_dict = {"value": None, "multiplier": None, "units": None}
        if "sr510" in lockin_keys[0]:
            sensitivity_dict["value"] = lockin_input["sr510 new sensitivity value"]
            sensitivity_dict["multiplier"] = lockin_input["sr510 new sensitivity multiplier"]
            sensitivity_dict["units"] = lockin_input["sr510 new sensitivity units"]
            timeconstant_dict["value"] = lockin_input["sr510 new time constant value"]
            timeconstant_dict["multiplier"] = lockin_input["sr510 new time constant multiplier"]
            timeconstant_dict["units"] = lockin_input["sr510 new time constant units"]
        elif "sr830" in lockin_keys[0]:
            sensitivity_dict["value"] = lockin_input["sr830 new sensitivity value"]
            sensitivity_dict["multiplier"] = lockin_input["sr830 new sensitivity multiplier"]
            sensitivity_dict["units"] = lockin_input["sr830 new sensitivity units"]
            timeconstant_dict["value"] = lockin_input["sr830 new time constant value"]
            timeconstant_dict["multiplier"] = lockin_input["sr830 new time constant multiplier"]
            timeconstant_dict["units"] = lockin_input["sr830 new time constant units"]

        sensitivity = float(sensitivity_dict["value"]) * float(sensitivity_dict["multiplier"].split("x")[-1]) * \
                      float(Lockin.UNIT_SENSITIVITY_MAP[sensitivity_dict["units"]])
        tc = float(timeconstant_dict["value"]) * float(timeconstant_dict["multiplier"].split("x")[-1]) * \
             float(Lockin.UNIT_TC_MAP[timeconstant_dict["units"]])
        lockin_output = {"sensitivity": sensitivity, "time-constant": tc}

        return lockin_output


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
