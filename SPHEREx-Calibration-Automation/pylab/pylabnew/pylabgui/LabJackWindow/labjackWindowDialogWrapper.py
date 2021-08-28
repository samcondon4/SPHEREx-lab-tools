"""labjackWindowDialogWrapper:

    This module provides a wrapper class, LabjackWindow, around the LabjackWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

from PyQt5 import QtWidgets
from pylabgui.LabJackWindow.labjackWindowDialog import Ui_Form
from pylabgui.pylabgui_window_base import GuiWindow


class LabjackWindow(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LabjackWindow()
    window.form.show()
    sys.exit(app.exec_())
