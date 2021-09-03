"""labjackWindowDialogWrapper:

    This module provides a wrapper class, LabjackWindow, around the LabjackWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

from PyQt5 import QtWidgets, QtCore
from pylabgui.LabJackWindow.labjackWindowDialog import Ui_Form
from pylabgui.pylabgui_window_base import GuiWindow


DIO_STATE_CHECK_MAP = {0: QtCore.Qt.Unchecked, 1: QtCore.Qt.Checked}


class LabjackWindow(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()
        GuiWindow.WidgetGroups["newcur labjack state"].set_setter_proc(self.set_dio_proc)

    def set_dio_proc(self, in_dict):
        config_str = "dio{} config"
        state_str = "dio{} state"
        out_dict = {}
        for key in in_dict["dio config"]:
            out_dict[config_str.format(key)] = in_dict["dio config"][key]
        for key in in_dict["dio state"]:
            out_dict[state_str.format(key)] = str(in_dict["dio state"][key] > 0)

        return out_dict


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LabjackWindow()
    window.form.show()
    sys.exit(app.exec_())
