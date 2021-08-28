"""cs260DialogWrapper:

    This module provides a wrapper class, CS260Window, around the cs260Dialog that
    was generated using QT-Designer.

Sam Condon, 08/12/2021
"""

from PyQt5 import QtWidgets
from pylabgui.CS260Window.cs260Dialog import Ui_Form
from pylabgui.pylabgui_window_base import GuiWindow


class CS260Window(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CS260Window()
    window.form.show()
    sys.exit(app.exec_())
