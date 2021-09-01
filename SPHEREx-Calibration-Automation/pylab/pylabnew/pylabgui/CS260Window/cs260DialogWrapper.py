"""cs260DialogWrapper:

    This module provides a wrapper class, CS260Window, around the cs260Dialog that
    was generated using QT-Designer.

Sam Condon, 08/12/2021
"""

from PyQt5 import QtWidgets
from pylabgui.CS260Window.cs260Dialog import Ui_Form
from pylabgui.pylabgui_window_base import GuiWindow


class CS260Window(Ui_Form, GuiWindow):

    GRATING_MAP = {"1": "G1", "2": "G2", "3": "G3"}
    OSF_MAP = {"1": "OSF1", "2": "OSF2", "3": "OSF3", "4": "No OSF"}
    SHUTTER_MAP = {"O": "Open", "C": "Close"}

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()

        self.WidgetGroups["current cs260"].set_setter_proc(self.setter_proc)

    def setter_proc(self, setter_dict):
        for key in setter_dict:
            if key == "current grating":
                setter_dict[key] = CS260Window.GRATING_MAP[setter_dict[key]]
            elif key == "current order sort filter":
                setter_dict[key] = CS260Window.OSF_MAP[setter_dict[key]]
            elif key == "current shutter":
                setter_dict[key] = CS260Window.SHUTTER_MAP[setter_dict[key]]

        return setter_dict


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CS260Window()
    window.form.show()
    sys.exit(app.exec_())
