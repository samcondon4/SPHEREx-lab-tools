# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ndfWheelDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1003, 850)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.manual_ndf_newpos_cbox = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_ndf_newpos_cbox.sizePolicy().hasHeightForWidth())
        self.manual_ndf_newpos_cbox.setSizePolicy(sizePolicy)
        self.manual_ndf_newpos_cbox.setObjectName("manual_ndf_newpos_cbox")
        self.manual_ndf_newpos_cbox.addItem("")
        self.manual_ndf_newpos_cbox.addItem("")
        self.manual_ndf_newpos_cbox.addItem("")
        self.manual_ndf_newpos_cbox.addItem("")
        self.manual_ndf_newpos_cbox.addItem("")
        self.manual_ndf_newpos_cbox.addItem("")
        self.manual_ndf_newpos_cbox.addItem("")
        self.manual_ndf_newpos_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_ndf_newpos_cbox, 2, 1, 1, 1)
        self.manual_ndf_curpos_ledit = QtWidgets.QLineEdit(Form)
        self.manual_ndf_curpos_ledit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_ndf_curpos_ledit.sizePolicy().hasHeightForWidth())
        self.manual_ndf_curpos_ledit.setSizePolicy(sizePolicy)
        self.manual_ndf_curpos_ledit.setObjectName("manual_ndf_curpos_ledit")
        self.gridLayout.addWidget(self.manual_ndf_curpos_ledit, 2, 0, 1, 1)
        self.manual_ndf_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_ndf_label.sizePolicy().hasHeightForWidth())
        self.manual_ndf_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.manual_ndf_label.setFont(font)
        self.manual_ndf_label.setObjectName("manual_ndf_label")
        self.gridLayout.addWidget(self.manual_ndf_label, 0, 0, 1, 1)
        self.manual_ndf_newpos_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_ndf_newpos_label.sizePolicy().hasHeightForWidth())
        self.manual_ndf_newpos_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.manual_ndf_newpos_label.setFont(font)
        self.manual_ndf_newpos_label.setObjectName("manual_ndf_newpos_label")
        self.gridLayout.addWidget(self.manual_ndf_newpos_label, 1, 1, 1, 1)
        self.manual_ndf_curpos_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_ndf_curpos_label.sizePolicy().hasHeightForWidth())
        self.manual_ndf_curpos_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.manual_ndf_curpos_label.setFont(font)
        self.manual_ndf_curpos_label.setObjectName("manual_ndf_curpos_label")
        self.gridLayout.addWidget(self.manual_ndf_curpos_label, 1, 0, 1, 1)
        self.manual_get_ndf_newposition_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_get_ndf_newposition_button.sizePolicy().hasHeightForWidth())
        self.manual_get_ndf_newposition_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.manual_get_ndf_newposition_button.setFont(font)
        self.manual_get_ndf_newposition_button.setObjectName("manual_get_ndf_newposition_button")
        self.gridLayout.addWidget(self.manual_get_ndf_newposition_button, 3, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "NDF Wheel"))
        self.manual_ndf_newpos_cbox.setItemText(0, _translate("Form", "1"))
        self.manual_ndf_newpos_cbox.setItemText(1, _translate("Form", "2"))
        self.manual_ndf_newpos_cbox.setItemText(2, _translate("Form", "3"))
        self.manual_ndf_newpos_cbox.setItemText(3, _translate("Form", "4"))
        self.manual_ndf_newpos_cbox.setItemText(4, _translate("Form", "5"))
        self.manual_ndf_newpos_cbox.setItemText(5, _translate("Form", "6"))
        self.manual_ndf_newpos_cbox.setItemText(6, _translate("Form", "7"))
        self.manual_ndf_newpos_cbox.setItemText(7, _translate("Form", "8"))
        self.manual_ndf_label.setText(_translate("Form", "NDF Wheel:"))
        self.manual_ndf_newpos_label.setText(_translate("Form", "New Position"))
        self.manual_ndf_curpos_label.setText(_translate("Form", "Current Position:"))
        self.manual_get_ndf_newposition_button.setText(_translate("Form", "Set New NDF Position"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

