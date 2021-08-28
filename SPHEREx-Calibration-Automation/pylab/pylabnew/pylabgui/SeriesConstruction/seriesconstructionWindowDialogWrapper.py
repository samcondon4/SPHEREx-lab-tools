"""seriesConstructionWindowDialogWrapper:

    This module provides a wrapper class, SeriesConstructionWindow, around the seriesConstructionWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

from PyQt5 import QtWidgets
from pylabgui.SeriesConstruction.seriesconstructionWindowDialog import Ui_Form
from pylabgui.pylabgui_window_base import GuiWindow


class SeriesConstructionWindow(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()
    #################################################################################################################


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    sequence_dir = ".\\sequences\\seriesConstructionWindowTest\\"
    window = SeriesConstructionWindow()
    window.form.show()
    sys.exit(app.exec_())
