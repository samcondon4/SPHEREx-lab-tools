"""cs260DialogWrapper:

    This module provides a wrapper class, CS260Window, around the cs260Dialog that
    was generated using QT-Designer.

Sam Condon, 08/12/2021
"""

from PyQt5 import QtWidgets
from .cs260Dialog import Ui_Form
from spherexlabtools.ui.windows import GuiWindow


class CS260Window(Ui_Form, GuiWindow):

    GRATING_MAP = {"1": "G1", "2": "G2", "3": "G3"}
    SHUTTER_MAP = {"O": "Open", "C": "Close"}

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()

        self.WidgetGroups["current_cs260_state"].set_setter_proc(self.setter_proc)

    def setter_proc(self, setter_dict):
        for key in setter_dict:
            if key == "grating":
                setter_dict[key] = CS260Window.GRATING_MAP[setter_dict[key]]
            elif key == "shutter":
                setter_dict[key] = CS260Window.SHUTTER_MAP[setter_dict[key]]

        return setter_dict


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CS260Window()
    window.form.show()
    sys.exit(app.exec_())
