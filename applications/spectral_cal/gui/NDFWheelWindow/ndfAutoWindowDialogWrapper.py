"""ndfAutoWheelDialogWrapper:

    This module provides a wrapper class, NDFAutoWindow, around the ndfAutoWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

from PyQt5 import QtWidgets
from .ndfAutoWindowDialog import Ui_Form
from spherexlabtools.ui.windows import GuiWindow


class NDFAutoWindow(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = NDFAutoWindow()
    window.form.show()
    sys.exit(app.exec_())
