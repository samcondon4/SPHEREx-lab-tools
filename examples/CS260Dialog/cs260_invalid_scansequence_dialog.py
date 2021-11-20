# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cs260_invalid_scansequence_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5.QtWidgets import *


class InvalidScanSequenceDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.dialog = QDialog()
        self.gridLayout_2 = QGridLayout()
        self.gridLayout = QGridLayout()
        self.dialog.setWindowTitle("Invalid Scan Sequence!")
        self.dialog.setMinimumSize(900, 500)

        self.error_browser = QTextBrowser(self)
        self.gridLayout.addWidget(self.error_browser, 0, 0, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.dialog.setLayout(self.gridLayout_2)

    def disp_errors(self, error_list):
        self.error_browser.clear()
        self.error_browser.append("Invalid scan sequence will not be added to the series.")
        self.error_browser.append("Fix the following errors:")
        for e in error_list:
            self.error_browser.append(e)
