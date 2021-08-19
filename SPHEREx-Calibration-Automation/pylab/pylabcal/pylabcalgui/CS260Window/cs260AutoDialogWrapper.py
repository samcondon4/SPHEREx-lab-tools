"""cs260AutoDialogWrapper:

    This module provides a wrapper class, CS260AutoWindow, around the cs260AutoDialog that
    was generated using QT-Designer.

Sam Condon, 08/16/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylabcal.pylabcalgui.CS260Window.cs260AutoDialog import Ui_Form
from pylablib.pylablibgui_window_base import GuiWindow


class CS260AutoWindow(Ui_Form, GuiWindow):

    def __init__(self, data_queues=None):
        super().__init__(child=self, data_queues=data_queues)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CS260AutoWindow()
    window.form.show()
    sys.exit(app.exec_())
