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
        Form.resize(1706, 1506)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
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
        self.gridLayout.addWidget(self.label_14, 0, 0, 1, 4)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 1, 0, 1, 4)
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
        self.manual_get_labjack_dio0state_check = QtWidgets.QCheckBox(Form)
        self.manual_get_labjack_dio0state_check.setObjectName("manual_get_labjack_dio0state_check")
        self.gridLayout.addWidget(self.manual_get_labjack_dio0state_check, 3, 0, 1, 1)
        self.manual_get_labjack_dio0config_cbox = QtWidgets.QComboBox(Form)
        self.manual_get_labjack_dio0config_cbox.setObjectName("manual_get_labjack_dio0config_cbox")
        self.manual_get_labjack_dio0config_cbox.addItem("")
        self.manual_get_labjack_dio0config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_get_labjack_dio0config_cbox, 3, 1, 1, 1)
        self.manual_labjack_dio11state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio11state_check.setObjectName("manual_labjack_dio11state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio11state_check, 3, 2, 1, 1)
        self.manual_labjack_dio11config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio11config_cbox.setObjectName("manual_labjack_dio11config_cbox")
        self.manual_labjack_dio11config_cbox.addItem("")
        self.manual_labjack_dio11config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio11config_cbox, 3, 3, 1, 1)
        self.manual_get_labjack_dio1state_check = QtWidgets.QCheckBox(Form)
        self.manual_get_labjack_dio1state_check.setObjectName("manual_get_labjack_dio1state_check")
        self.gridLayout.addWidget(self.manual_get_labjack_dio1state_check, 4, 0, 1, 1)
        self.manual_get_labjack_dio1config_cbox = QtWidgets.QComboBox(Form)
        self.manual_get_labjack_dio1config_cbox.setObjectName("manual_get_labjack_dio1config_cbox")
        self.manual_get_labjack_dio1config_cbox.addItem("")
        self.manual_get_labjack_dio1config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_get_labjack_dio1config_cbox, 4, 1, 1, 1)
        self.manual_labjack_dio12state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio12state_check.setObjectName("manual_labjack_dio12state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio12state_check, 4, 2, 1, 1)
        self.manual_labjack_dio12config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio12config_cbox.setObjectName("manual_labjack_dio12config_cbox")
        self.manual_labjack_dio12config_cbox.addItem("")
        self.manual_labjack_dio12config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio12config_cbox, 4, 3, 1, 1)
        self.manual_get_labjack_dio2state_check = QtWidgets.QCheckBox(Form)
        self.manual_get_labjack_dio2state_check.setObjectName("manual_get_labjack_dio2state_check")
        self.gridLayout.addWidget(self.manual_get_labjack_dio2state_check, 5, 0, 1, 1)
        self.manual_get_labjack_dio2config_cbox = QtWidgets.QComboBox(Form)
        self.manual_get_labjack_dio2config_cbox.setObjectName("manual_get_labjack_dio2config_cbox")
        self.manual_get_labjack_dio2config_cbox.addItem("")
        self.manual_get_labjack_dio2config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_get_labjack_dio2config_cbox, 5, 1, 1, 1)
        self.manual_labjack_dio13state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio13state_check.setObjectName("manual_labjack_dio13state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio13state_check, 5, 2, 1, 1)
        self.manual_labjack_dio13config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio13config_cbox.setObjectName("manual_labjack_dio13config_cbox")
        self.manual_labjack_dio13config_cbox.addItem("")
        self.manual_labjack_dio13config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio13config_cbox, 5, 3, 1, 1)
        self.manual_labjack_dio3state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio3state_check.setObjectName("manual_labjack_dio3state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio3state_check, 6, 0, 1, 1)
        self.manual_labjack_dio3config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio3config_cbox.setObjectName("manual_labjack_dio3config_cbox")
        self.manual_labjack_dio3config_cbox.addItem("")
        self.manual_labjack_dio3config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio3config_cbox, 6, 1, 1, 1)
        self.manual_labjack_dio14state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio14state_check.setObjectName("manual_labjack_dio14state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio14state_check, 6, 2, 1, 1)
        self.manual_labjack_dio14config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio14config_cbox.setObjectName("manual_labjack_dio14config_cbox")
        self.manual_labjack_dio14config_cbox.addItem("")
        self.manual_labjack_dio14config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio14config_cbox, 6, 3, 1, 1)
        self.manual_labjack_dio4state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio4state_check.setObjectName("manual_labjack_dio4state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio4state_check, 7, 0, 1, 1)
        self.manual_labjack_dio4config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio4config_cbox.setObjectName("manual_labjack_dio4config_cbox")
        self.manual_labjack_dio4config_cbox.addItem("")
        self.manual_labjack_dio4config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio4config_cbox, 7, 1, 1, 1)
        self.manual_labjack_dio15state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio15state_check.setObjectName("manual_labjack_dio15state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio15state_check, 7, 2, 1, 1)
        self.manual_labjack_dio15config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio15config_cbox.setObjectName("manual_labjack_dio15config_cbox")
        self.manual_labjack_dio15config_cbox.addItem("")
        self.manual_labjack_dio15config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio15config_cbox, 7, 3, 1, 1)
        self.manual_labjack_dio5state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio5state_check.setObjectName("manual_labjack_dio5state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio5state_check, 8, 0, 1, 1)
        self.manual_labjack_dio5config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio5config_cbox.setObjectName("manual_labjack_dio5config_cbox")
        self.manual_labjack_dio5config_cbox.addItem("")
        self.manual_labjack_dio5config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio5config_cbox, 8, 1, 1, 1)
        self.manual_labjack_dio16state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio16state_check.setObjectName("manual_labjack_dio16state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio16state_check, 8, 2, 1, 1)
        self.manual_labjack_dio16config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio16config_cbox.setObjectName("manual_labjack_dio16config_cbox")
        self.manual_labjack_dio16config_cbox.addItem("")
        self.manual_labjack_dio16config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio16config_cbox, 8, 3, 1, 1)
        self.manual_labjack_dio6state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio6state_check.setObjectName("manual_labjack_dio6state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio6state_check, 9, 0, 1, 1)
        self.manual_labjack_dio6config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio6config_cbox.setObjectName("manual_labjack_dio6config_cbox")
        self.manual_labjack_dio6config_cbox.addItem("")
        self.manual_labjack_dio6config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio6config_cbox, 9, 1, 1, 1)
        self.manual_labjack_dio17state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio17state_check.setObjectName("manual_labjack_dio17state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio17state_check, 9, 2, 1, 1)
        self.manual_labjack_dio17config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio17config_cbox.setObjectName("manual_labjack_dio17config_cbox")
        self.manual_labjack_dio17config_cbox.addItem("")
        self.manual_labjack_dio17config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio17config_cbox, 9, 3, 1, 1)
        self.manual_labjack_dio7state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio7state_check.setObjectName("manual_labjack_dio7state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio7state_check, 10, 0, 1, 1)
        self.manual_labjack_dio7config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio7config_cbox.setObjectName("manual_labjack_dio7config_cbox")
        self.manual_labjack_dio7config_cbox.addItem("")
        self.manual_labjack_dio7config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio7config_cbox, 10, 1, 1, 1)
        self.manual_labjack_dio18state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio18state_check.setObjectName("manual_labjack_dio18state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio18state_check, 10, 2, 1, 1)
        self.manual_labjack_dio18config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio18config_cbox.setObjectName("manual_labjack_dio18config_cbox")
        self.manual_labjack_dio18config_cbox.addItem("")
        self.manual_labjack_dio18config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio18config_cbox, 10, 3, 1, 1)
        self.manual_labjack_dio8state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio8state_check.setObjectName("manual_labjack_dio8state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio8state_check, 11, 0, 1, 1)
        self.manual_labjack_dio8config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio8config_cbox.setObjectName("manual_labjack_dio8config_cbox")
        self.manual_labjack_dio8config_cbox.addItem("")
        self.manual_labjack_dio8config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio8config_cbox, 11, 1, 1, 1)
        self.manual_labjack_dio19state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio19state_check.setObjectName("manual_labjack_dio19state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio19state_check, 11, 2, 1, 1)
        self.manual_labjack_dio19config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio19config_cbox.setObjectName("manual_labjack_dio19config_cbox")
        self.manual_labjack_dio19config_cbox.addItem("")
        self.manual_labjack_dio19config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio19config_cbox, 11, 3, 1, 1)
        self.manual_labjack_dio9state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio9state_check.setObjectName("manual_labjack_dio9state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio9state_check, 12, 0, 1, 1)
        self.manual_labjack_dio9config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio9config_cbox.setObjectName("manual_labjack_dio9config_cbox")
        self.manual_labjack_dio9config_cbox.addItem("")
        self.manual_labjack_dio9config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio9config_cbox, 12, 1, 1, 1)
        self.manual_labjack_dio20state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio20state_check.setObjectName("manual_labjack_dio20state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio20state_check, 12, 2, 1, 1)
        self.manual_labjack_dio20config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio20config_cbox.setObjectName("manual_labjack_dio20config_cbox")
        self.manual_labjack_dio20config_cbox.addItem("")
        self.manual_labjack_dio20config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio20config_cbox, 12, 3, 1, 1)
        self.manual_labjack_dio10state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio10state_check.setObjectName("manual_labjack_dio10state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio10state_check, 13, 0, 1, 1)
        self.manual_labjack_dio10config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio10config_cbox.setObjectName("manual_labjack_dio10config_cbox")
        self.manual_labjack_dio10config_cbox.addItem("")
        self.manual_labjack_dio10config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio10config_cbox, 13, 1, 1, 1)
        self.manual_labjack_dio21state_check = QtWidgets.QCheckBox(Form)
        self.manual_labjack_dio21state_check.setObjectName("manual_labjack_dio21state_check")
        self.gridLayout.addWidget(self.manual_labjack_dio21state_check, 13, 2, 1, 1)
        self.manual_labjack_dio21config_cbox = QtWidgets.QComboBox(Form)
        self.manual_labjack_dio21config_cbox.setObjectName("manual_labjack_dio21config_cbox")
        self.manual_labjack_dio21config_cbox.addItem("")
        self.manual_labjack_dio21config_cbox.addItem("")
        self.gridLayout.addWidget(self.manual_labjack_dio21config_cbox, 13, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "LabJack"))
        self.label_14.setText(_translate("Form", "LabJack:"))
        self.label_15.setText(_translate("Form", "Digital I/O:"))
        self.manual_get_labjack_dio0state_check.setText(_translate("Form", "DIO0"))
        self.manual_get_labjack_dio0config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_get_labjack_dio0config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio11state_check.setText(_translate("Form", "DIO11"))
        self.manual_labjack_dio11config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio11config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_get_labjack_dio1state_check.setText(_translate("Form", "DIO1"))
        self.manual_get_labjack_dio1config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_get_labjack_dio1config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio12state_check.setText(_translate("Form", "DIO12"))
        self.manual_labjack_dio12config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio12config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_get_labjack_dio2state_check.setText(_translate("Form", "DIO2"))
        self.manual_get_labjack_dio2config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_get_labjack_dio2config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio13state_check.setText(_translate("Form", "DIO13"))
        self.manual_labjack_dio13config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio13config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio3state_check.setText(_translate("Form", "DIO3"))
        self.manual_labjack_dio3config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio3config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio14state_check.setText(_translate("Form", "DIO14"))
        self.manual_labjack_dio14config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio14config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio4state_check.setText(_translate("Form", "DIO4"))
        self.manual_labjack_dio4config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio4config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio15state_check.setText(_translate("Form", "DIO15"))
        self.manual_labjack_dio15config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio15config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio5state_check.setText(_translate("Form", "DIO5"))
        self.manual_labjack_dio5config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio5config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio16state_check.setText(_translate("Form", "DIO16"))
        self.manual_labjack_dio16config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio16config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio6state_check.setText(_translate("Form", "DIO6"))
        self.manual_labjack_dio6config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio6config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio17state_check.setText(_translate("Form", "DIO17"))
        self.manual_labjack_dio17config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio17config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio7state_check.setText(_translate("Form", "DIO7"))
        self.manual_labjack_dio7config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio7config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio18state_check.setText(_translate("Form", "DIO18"))
        self.manual_labjack_dio18config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio18config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio8state_check.setText(_translate("Form", "DIO8"))
        self.manual_labjack_dio8config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio8config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio19state_check.setText(_translate("Form", "DIO19"))
        self.manual_labjack_dio19config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio19config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio9state_check.setText(_translate("Form", "DIO9"))
        self.manual_labjack_dio9config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio9config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio20state_check.setText(_translate("Form", "DIO20"))
        self.manual_labjack_dio20config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio20config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio10state_check.setText(_translate("Form", "DIO10"))
        self.manual_labjack_dio10config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio10config_cbox.setItemText(1, _translate("Form", "Output"))
        self.manual_labjack_dio21state_check.setText(_translate("Form", "DIO21"))
        self.manual_labjack_dio21config_cbox.setItemText(0, _translate("Form", "Input"))
        self.manual_labjack_dio21config_cbox.setItemText(1, _translate("Form", "Output"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

