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
        Form.resize(746, 603)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.combobox_base_NewNdf_passive_NewPosition = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combobox_base_NewNdf_passive_NewPosition.sizePolicy().hasHeightForWidth())
        self.combobox_base_NewNdf_passive_NewPosition.setSizePolicy(sizePolicy)
        self.combobox_base_NewNdf_passive_NewPosition.setObjectName("combobox_base_NewNdf_passive_NewPosition")
        self.combobox_base_NewNdf_passive_NewPosition.addItem("")
        self.combobox_base_NewNdf_passive_NewPosition.addItem("")
        self.combobox_base_NewNdf_passive_NewPosition.addItem("")
        self.combobox_base_NewNdf_passive_NewPosition.addItem("")
        self.combobox_base_NewNdf_passive_NewPosition.addItem("")
        self.combobox_base_NewNdf_passive_NewPosition.addItem("")
        self.combobox_base_NewNdf_passive_NewPosition.addItem("")
        self.combobox_base_NewNdf_passive_NewPosition.addItem("")
        self.gridLayout.addWidget(self.combobox_base_NewNdf_passive_NewPosition, 2, 1, 1, 1)
        self.lineedit_base_CurrentNdfPosition_passive_CurrentPosition = QtWidgets.QLineEdit(Form)
        self.lineedit_base_CurrentNdfPosition_passive_CurrentPosition.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_base_CurrentNdfPosition_passive_CurrentPosition.sizePolicy().hasHeightForWidth())
        self.lineedit_base_CurrentNdfPosition_passive_CurrentPosition.setSizePolicy(sizePolicy)
        self.lineedit_base_CurrentNdfPosition_passive_CurrentPosition.setObjectName("lineedit_base_CurrentNdfPosition_passive_CurrentPosition")
        self.gridLayout.addWidget(self.lineedit_base_CurrentNdfPosition_passive_CurrentPosition, 2, 0, 1, 1)
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
        self.button_base_NewNdf_getter_NewNdfButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_base_NewNdf_getter_NewNdfButton.sizePolicy().hasHeightForWidth())
        self.button_base_NewNdf_getter_NewNdfButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.button_base_NewNdf_getter_NewNdfButton.setFont(font)
        self.button_base_NewNdf_getter_NewNdfButton.setObjectName("button_base_NewNdf_getter_NewNdfButton")
        self.gridLayout.addWidget(self.button_base_NewNdf_getter_NewNdfButton, 3, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "NDF Wheel"))
        self.combobox_base_NewNdf_passive_NewPosition.setItemText(0, _translate("Form", "1"))
        self.combobox_base_NewNdf_passive_NewPosition.setItemText(1, _translate("Form", "2"))
        self.combobox_base_NewNdf_passive_NewPosition.setItemText(2, _translate("Form", "3"))
        self.combobox_base_NewNdf_passive_NewPosition.setItemText(3, _translate("Form", "4"))
        self.combobox_base_NewNdf_passive_NewPosition.setItemText(4, _translate("Form", "5"))
        self.combobox_base_NewNdf_passive_NewPosition.setItemText(5, _translate("Form", "6"))
        self.combobox_base_NewNdf_passive_NewPosition.setItemText(6, _translate("Form", "7"))
        self.combobox_base_NewNdf_passive_NewPosition.setItemText(7, _translate("Form", "8"))
        self.manual_ndf_label.setText(_translate("Form", "NDF Wheel:"))
        self.manual_ndf_newpos_label.setText(_translate("Form", "New Position"))
        self.manual_ndf_curpos_label.setText(_translate("Form", "Current Position:"))
        self.button_base_NewNdf_getter_NewNdfButton.setText(_translate("Form", "Set New NDF Position"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

