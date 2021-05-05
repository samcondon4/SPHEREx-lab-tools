# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Transmission.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TransmissionTab(object):
    def setupUi(self, TransmissionTab):
        TransmissionTab.setObjectName("TransmissionTab")
        TransmissionTab.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(TransmissionTab)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.power_measure_scan_series = QtWidgets.QPushButton(TransmissionTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_measure_scan_series.sizePolicy().hasHeightForWidth())
        self.power_measure_scan_series.setSizePolicy(sizePolicy)
        self.power_measure_scan_series.setObjectName("power_measure_scan_series")
        self.verticalLayout.addWidget(self.power_measure_scan_series)
        self.power_measure_single = QtWidgets.QPushButton(TransmissionTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_measure_single.sizePolicy().hasHeightForWidth())
        self.power_measure_single.setSizePolicy(sizePolicy)
        self.power_measure_single.setObjectName("power_measure_single")
        self.verticalLayout.addWidget(self.power_measure_single)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(TransmissionTab)
        QtCore.QMetaObject.connectSlotsByName(TransmissionTab)

    def retranslateUi(self, TransmissionTab):
        _translate = QtCore.QCoreApplication.translate
        TransmissionTab.setWindowTitle(_translate("TransmissionTab", "Dialog"))
        self.power_measure_scan_series.setText(_translate("TransmissionTab", "Run Power Measurements over Scan Series"))
        self.power_measure_single.setText(_translate("TransmissionTab", "Run Single Power Measurement"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TransmissionTab = QtWidgets.QDialog()
    ui = Ui_TransmissionTab()
    ui.setupUi(TransmissionTab)
    TransmissionTab.show()
    sys.exit(app.exec_())
