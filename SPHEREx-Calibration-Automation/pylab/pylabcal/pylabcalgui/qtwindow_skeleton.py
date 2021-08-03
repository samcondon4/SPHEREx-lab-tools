"""qtwindow_skeleton:

    This module provides a skeleton for creating PyQt5 window wrappers

Sam Condon, 08/03/2021
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pylablib.pylablib_gui_tab import GuiTab


class QTWindow(GuiTab):

    def __init__(self):
        super().__init__(self)
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)

        # Configure parameters ###########################################################

        ##################################################################################

        # Configure button methods #######################################################

        ##################################################################################

    # PARAMETER GETTER/SETTERS #######################################################

    ##################################################################################

    # PRIVATE METHODS ################################################################

    ##################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QTWindow()
    window.form.show()
    sys.exit(app.exec_())
