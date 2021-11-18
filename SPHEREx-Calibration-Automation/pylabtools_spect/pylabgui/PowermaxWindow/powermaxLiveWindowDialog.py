# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PowermaxLiveWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(485, 382)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.powermax_livedisplay_activewavelength_ledit = QtWidgets.QLineEdit(Form)
        self.powermax_livedisplay_activewavelength_ledit.setObjectName("powermax_livedisplay_activewavelength_ledit")
        self.gridLayout.addWidget(self.powermax_livedisplay_activewavelength_ledit, 1, 1, 1, 1)
        self.powermax_livedisplay_activewavelength_label = QtWidgets.QLabel(Form)
        self.powermax_livedisplay_activewavelength_label.setObjectName("powermax_livedisplay_activewavelength_label")
        self.gridLayout.addWidget(self.powermax_livedisplay_activewavelength_label, 1, 0, 1, 1)
        self.powermax_zerosensor_button = QtWidgets.QPushButton(Form)
        self.powermax_zerosensor_button.setObjectName("powermax_zerosensor_button")
        self.gridLayout.addWidget(self.powermax_zerosensor_button, 3, 0, 1, 2)
        self.powermax_livedisplay_startstop_button = QtWidgets.QPushButton(Form)
        self.powermax_livedisplay_startstop_button.setObjectName("powermax_livedisplay_startstop_button")
        self.gridLayout.addWidget(self.powermax_livedisplay_startstop_button, 2, 0, 1, 2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.powermax_livedisplay_activewavelength_label.setText(_translate("Form", "Active Wavelength (um.):"))
        self.powermax_zerosensor_button.setText(_translate("Form", "Zero Sensor"))
        self.powermax_livedisplay_startstop_button.setText(_translate("Form", "Start Acquisition"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
