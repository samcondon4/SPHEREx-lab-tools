""" This module provides the class SltTop, which provides the main SPHERExLabTools gui interface.
"""
from PyQt5 import QtCore
from ._top_interface import Ui_SltTop


class SltTop(Ui_SltTop):

    ui_log_signal = QtCore.pyqtSignal(object)

    def __init__(self, top_widget):
        super().__init__()
        self.setupUi(top_widget)
        self.ver_scrollbar = self.logBrowser.verticalScrollBar()
        self.hor_scrollbar = self.logBrowser.horizontalScrollBar()
        #self.ui_log_signal.connect(self.log)

    def log(self, msg):
        """ This method allows logging of formatted log messaged created by the logging package to the log
        interface.

        :param msg: String message to write to the log window.
        """
        self.logBrowser.append(msg)
        scroll = self.ver_scrollbar.maximum() - self.ver_scrollbar.value() <= 10
        if scroll:
            self.ver_scrollbar.setValue(self.ver_scrollbar.maximum())
            self.hor_scrollbar.setValue(0)

