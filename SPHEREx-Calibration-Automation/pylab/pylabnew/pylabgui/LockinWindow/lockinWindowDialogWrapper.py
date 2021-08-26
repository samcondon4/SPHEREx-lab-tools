"""lockinWindowDialogWrapper:

    This module provides a wrapper class, LockinWindow, around the lockinWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

import asyncio
from qasync import QEventLoop
from PyQt5 import QtWidgets
from pylabgui.LockinWindow.lockinWindowDialog import Ui_Form
from pylabgui.pylabgui_window_base import GuiWindow

# HELPER DICTIONARIES ###############################################################################
LOCKIN_UNIT_SENSITIVITY_MAP = {"V.": 1, "mV.": 1e-3, "uV.": 1e-6, "nV.": 1e-9}
LOCKIN_UNIT_TC_MAP = {"ks.": 1e3, "s.": 1, "ms.": 1e-3, "us.": 1e-6}
LOCKIN_TC_MOD_MAP = {1: 0, 0: 3}
LOCKIN_TC_MULT_UNIT_MAP = {1e-6: ("x1", "us."), 1e-5: ("x10", "us."), 1e-4: ("x100", "us."),
                           1e-3: ("x1", "ms."), 1e-2: ("x10", "ms."), 1e-1: ("x100", "ms."),
                           1: ("x1", "s."), 1e1: ("x10", "s."), 1e2: ("x100", "s."),
                           1e3: ("x1", "ks.")}
LOCKIN_SENS_MOD_MAP = {0: 5, 1: 1, 2: 2}
LOCKIN_SENS_MULT_UNIT_MAP = {1e-9: ("x1", "nV."), 1e-8: ("x10", "nV."), 1e-7: ("x100", "nV."),
                             1e-6: ("x1", "uV."), 1e-5: ("x10", "uV."), 1e-4: ("x100", "uV."),
                             1e-3: ("x1", "mV."), 1e-2: ("x10", "mV."), 1e-1: ("x100", "mV."),
                             1: ("x1", "V.")}
LOCKIN_FS = [float(2**i) for i in range(-4, 10)]
######################################################################################################


class LockinWindow(Ui_Form, GuiWindow):

    def __init__(self, data_queues=None):
        self.main_queues = data_queues
        self.proc_queue = asyncio.Queue()
        super().__init__(child=self, data_queues=[self.proc_queue])
        self.setupUi(self.form)
        if not self.configured:
            self.configure()

    async def run(self):
        while True:
            lockin_data = await self.proc_queue.get()
            lockin_param_key = str(list(lockin_data.keys())[0])
            if "config" in lockin_param_key:
                lockin_data = lockin_data[lockin_param_key]
                sensitivity_dict = {"value": None, "multiplier": None, "units": None}
                timeconstant_dict = {"value": None, "multiplier": None, "units": None}
                for key in lockin_data:
                    lockin_data_key_split = key.split(" ")
                    if "sensitivity" in key:
                        sensitivity_dict[lockin_data_key_split[-1]] = lockin_data[key]
                    elif "time constant" in key:
                        timeconstant_dict[lockin_data_key_split[-1]] = lockin_data[key]
                sensitivity = float(sensitivity_dict["value"]) * float(sensitivity_dict["multiplier"].split("x")[-1]) *\
                              float(LOCKIN_UNIT_SENSITIVITY_MAP[sensitivity_dict["units"]])
                tc = float(timeconstant_dict["value"]) * float(timeconstant_dict["multiplier"].split("x")[-1]) * \
                     float(LOCKIN_UNIT_TC_MAP[timeconstant_dict["units"]])
                queue_put = {lockin_param_key: {"sensitivity": sensitivity, "time-constant": tc}}
            else:
                queue_put = lockin_data

            for queue in self.main_queues:
                if type(queue) is asyncio.Queue:
                    queue.put_nowait(queue_put)
                else:
                    queue.put(queue_put)


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
