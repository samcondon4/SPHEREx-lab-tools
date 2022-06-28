# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'top_interface.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SltTop(object):
    def setupUi(self, SltTop):
        SltTop.setObjectName("SltTop")
        SltTop.resize(708, 535)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../SPIE2022/spherex-2020logo_color_nobackground.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SltTop.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(SltTop)
        self.gridLayout.setObjectName("gridLayout")
        self.top_horizontal_layout = QtWidgets.QHBoxLayout()
        self.top_horizontal_layout.setObjectName("top_horizontal_layout")
        self.gridLayout.addLayout(self.top_horizontal_layout, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(SltTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.log_tab = QtWidgets.QWidget()
        self.log_tab.setObjectName("log_tab")
        self.tabWidget.addTab(self.log_tab, "")
        self.threads_tab = QtWidgets.QWidget()
        self.threads_tab.setObjectName("threads_tab")
        self.tabWidget.addTab(self.threads_tab, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.retranslateUi(SltTop)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SltTop)

    def retranslateUi(self, SltTop):
        _translate = QtCore.QCoreApplication.translate
        SltTop.setWindowTitle(_translate("SltTop", "SPHERExLabTools"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.log_tab), _translate("SltTop", "Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.threads_tab), _translate("SltTop", "Threads"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SltTop = QtWidgets.QWidget()
    ui = Ui_SltTop()
    ui.setupUi(SltTop)
    SltTop.show()
    sys.exit(app.exec_())
