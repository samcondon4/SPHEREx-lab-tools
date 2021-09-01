# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'labjackWindowDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(780, 724)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio2State = QtWidgets.QCheckBox(Form)
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio2State.setObjectName("checkbox_base_NewcurLabjackDioParameters_passive_Dio2State")
        self.gridLayout.addWidget(self.checkbox_base_NewcurLabjackDioParameters_passive_Dio2State, 5, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 2, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 1, 0, 1, 3)
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio0State = QtWidgets.QCheckBox(Form)
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio0State.setObjectName("checkbox_base_NewcurLabjackDioParameters_passive_Dio0State")
        self.gridLayout.addWidget(self.checkbox_base_NewcurLabjackDioParameters_passive_Dio0State, 3, 0, 1, 1)
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio1State = QtWidgets.QCheckBox(Form)
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio1State.setObjectName("checkbox_base_NewcurLabjackDioParameters_passive_Dio1State")
        self.gridLayout.addWidget(self.checkbox_base_NewcurLabjackDioParameters_passive_Dio1State, 4, 0, 1, 1)
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio2Config = QtWidgets.QComboBox(Form)
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio2Config.setObjectName("combobox_base_NewcurLabjackDioParameters_passive_Dio2Config")
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio2Config.addItem("")
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio2Config.addItem("")
        self.gridLayout.addWidget(self.combobox_base_NewcurLabjackDioParameters_passive_Dio2Config, 5, 1, 1, 2)
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio0Config = QtWidgets.QComboBox(Form)
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio0Config.setObjectName("combobox_base_NewcurLabjackDioParameters_passive_Dio0Config")
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio0Config.addItem("")
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio0Config.addItem("")
        self.gridLayout.addWidget(self.combobox_base_NewcurLabjackDioParameters_passive_Dio0Config, 3, 1, 1, 2)
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio1Config = QtWidgets.QComboBox(Form)
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio1Config.setObjectName("combobox_base_NewcurLabjackDioParameters_passive_Dio1Config")
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio1Config.addItem("")
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio1Config.addItem("")
        self.gridLayout.addWidget(self.combobox_base_NewcurLabjackDioParameters_passive_Dio1Config, 4, 1, 1, 2)
        self.button_base_NewcurLabjackDioParameters_getter_DioSetParametersButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_base_NewcurLabjackDioParameters_getter_DioSetParametersButton.sizePolicy().hasHeightForWidth())
        self.button_base_NewcurLabjackDioParameters_getter_DioSetParametersButton.setSizePolicy(sizePolicy)
        self.button_base_NewcurLabjackDioParameters_getter_DioSetParametersButton.setObjectName("button_base_NewcurLabjackDioParameters_getter_DioSetParametersButton")
        self.gridLayout.addWidget(self.button_base_NewcurLabjackDioParameters_getter_DioSetParametersButton, 6, 0, 1, 3)
        self.label_14 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 0, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "LabJack"))
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio2State.setText(_translate("Form", "DIO2"))
        self.label_15.setText(_translate("Form", "Digital I/O:"))
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio0State.setText(_translate("Form", "DIO0"))
        self.checkbox_base_NewcurLabjackDioParameters_passive_Dio1State.setText(_translate("Form", "DIO1"))
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio2Config.setItemText(0, _translate("Form", "Input"))
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio2Config.setItemText(1, _translate("Form", "Output"))
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio0Config.setItemText(0, _translate("Form", "Input"))
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio0Config.setItemText(1, _translate("Form", "Output"))
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio1Config.setItemText(0, _translate("Form", "Input"))
        self.combobox_base_NewcurLabjackDioParameters_passive_Dio1Config.setItemText(1, _translate("Form", "Output"))
        self.button_base_NewcurLabjackDioParameters_getter_DioSetParametersButton.setText(_translate("Form", "Set Dio Parameters"))
        self.label_14.setText(_translate("Form", "LabJack:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

