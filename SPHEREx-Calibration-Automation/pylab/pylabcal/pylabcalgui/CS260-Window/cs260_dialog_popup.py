# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cs260_invalid_scansequence_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5.QtWidgets import *


class Cs260PopupDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.dialog = QDialog()
        self.gridLayout_2 = QGridLayout()
        self.gridLayout = QGridLayout()
        self.dialog.setMinimumSize(900, 500)

        self.error_browser = QTextBrowser(self)
        self.gridLayout.addWidget(self.error_browser, 0, 0, 1, 2)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.dialog.setLayout(self.gridLayout_2)

    def disp_errors(self, error_list):
        self.dialog.setWindowTitle("Error!")
        self.error_browser.clear()
        for e in error_list:
            self.error_browser.append(e)

    def disp_msg(self, error_list):
        self.dialog.setWindowTitle("Notice")
        self.error_browser.clear()
        for e in error_list:
            self.error_browser.append(e)

    def popup(self):
        self.dialog.exec_()