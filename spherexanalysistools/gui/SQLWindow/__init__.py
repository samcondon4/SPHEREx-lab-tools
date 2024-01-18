import sys
from PyQt5 import QtWidgets
from .mySQLQueryWindowWrapper import SQLQueryWindow


def run_query_window():
    app = QtWidgets.QApplication(sys.argv)
    window = SQLQueryWindow()
    window.mainwindow.show()
    sys.exit(app.exec_())
