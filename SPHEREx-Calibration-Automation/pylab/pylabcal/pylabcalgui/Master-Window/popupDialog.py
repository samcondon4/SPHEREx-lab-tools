from PyQt5.QtWidgets import *


class PopupDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.dialog = QDialog()
        self.gridLayout_2 = QGridLayout()
        self.gridLayout = QGridLayout()
        self.dialog.setMinimumSize(900, 500)

        self.msg_browser = QTextBrowser(self)
        self.gridLayout.addWidget(self.msg_browser, 0, 0, 1, 2)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.dialog.setLayout(self.gridLayout_2)

    def disp_errors(self, error_list):
        self.dialog.setWindowTitle("Error!")
        self.msg_browser.clear()
        for e in error_list:
            self.msg_browser.append(e)

    def disp_msg(self, msg_list):
        self.dialog.setWindowTitle("Notice")
        self.msg_browser.clear()
        for msg in msg_list:
            self.msg_browser.append(msg)

    def popup(self):
        self.dialog.exec_()