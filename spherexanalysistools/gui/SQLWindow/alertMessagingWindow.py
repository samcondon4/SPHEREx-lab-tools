# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/viero/Repositories/SPHEREx-lab-tools-09012020/spherexanalysistools/gui/QTDesigner/alertMessagingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1144, 808)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setObjectName("tab_main")
        self.widget = QtWidgets.QWidget(self.tab_main)
        self.widget.setGeometry(QtCore.QRect(10, 20, 971, 641))
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3.addLayout(self.verticalLayout_4, 1, 0, 1, 4)
        self.label_Name = QtWidgets.QLabel(self.widget)
        self.label_Name.setMinimumSize(QtCore.QSize(0, 30))
        self.label_Name.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_Name.setFont(font)
        self.label_Name.setObjectName("label_Name")
        self.gridLayout_3.addWidget(self.label_Name, 0, 0, 1, 1)
        self.label_SMS = QtWidgets.QLabel(self.widget)
        self.label_SMS.setMinimumSize(QtCore.QSize(0, 30))
        self.label_SMS.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_SMS.setFont(font)
        self.label_SMS.setObjectName("label_SMS")
        self.gridLayout_3.addWidget(self.label_SMS, 0, 1, 1, 1)
        self.label_Email = QtWidgets.QLabel(self.widget)
        self.label_Email.setMinimumSize(QtCore.QSize(0, 30))
        self.label_Email.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_Email.setFont(font)
        self.label_Email.setObjectName("label_Email")
        self.gridLayout_3.addWidget(self.label_Email, 0, 3, 1, 1)
        self.label_Email_2 = QtWidgets.QLabel(self.widget)
        self.label_Email_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_Email_2.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_Email_2.setFont(font)
        self.label_Email_2.setObjectName("label_Email_2")
        self.gridLayout_3.addWidget(self.label_Email_2, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_main, "")
        self.tab_settings = QtWidgets.QWidget()
        self.tab_settings.setObjectName("tab_settings")
        self.layoutWidget = QtWidgets.QWidget(self.tab_settings)
        self.layoutWidget.setGeometry(QtCore.QRect(320, 10, 781, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_field = QtWidgets.QLabel(self.layoutWidget)
        self.label_field.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_field.setFont(font)
        self.label_field.setObjectName("label_field")
        self.horizontalLayout.addWidget(self.label_field)
        self.label_Last = QtWidgets.QLabel(self.layoutWidget)
        self.label_Last.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_Last.setFont(font)
        self.label_Last.setObjectName("label_Last")
        self.horizontalLayout.addWidget(self.label_Last)
        self.label_Limit = QtWidgets.QLabel(self.layoutWidget)
        self.label_Limit.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_Limit.setFont(font)
        self.label_Limit.setObjectName("label_Limit")
        self.horizontalLayout.addWidget(self.label_Limit)
        self.label_action = QtWidgets.QLabel(self.layoutWidget)
        self.label_action.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_action.setFont(font)
        self.label_action.setObjectName("label_action")
        self.horizontalLayout.addWidget(self.label_action)
        self.label_status = QtWidgets.QLabel(self.layoutWidget)
        self.label_status.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_status.setFont(font)
        self.label_status.setObjectName("label_status")
        self.horizontalLayout.addWidget(self.label_status)
        self.splitter_3 = QtWidgets.QSplitter(self.tab_settings)
        self.splitter_3.setGeometry(QtCore.QRect(11, 40, 1091, 671))
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter = QtWidgets.QSplitter(self.splitter_3)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_Server_Location = QtWidgets.QComboBox(self.widget1)
        self.comboBox_Server_Location.setMinimumSize(QtCore.QSize(75, 0))
        self.comboBox_Server_Location.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_Server_Location.setFont(font)
        self.comboBox_Server_Location.setObjectName("comboBox_Server_Location")
        self.comboBox_Server_Location.addItem("")
        self.comboBox_Server_Location.addItem("")
        self.comboBox_Server_Location.addItem("")
        self.comboBox_Server_Location.addItem("")
        self.gridLayout.addWidget(self.comboBox_Server_Location, 0, 0, 1, 1)
        self.pushButton_Start = QtWidgets.QPushButton(self.widget1)
        self.pushButton_Start.setMinimumSize(QtCore.QSize(75, 0))
        self.pushButton_Start.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_Start.setFont(font)
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.gridLayout.addWidget(self.pushButton_Start, 0, 1, 1, 1)
        self.pushButton_Stop = QtWidgets.QPushButton(self.widget1)
        self.pushButton_Stop.setMinimumSize(QtCore.QSize(75, 0))
        self.pushButton_Stop.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_Stop.setFont(font)
        self.pushButton_Stop.setObjectName("pushButton_Stop")
        self.gridLayout.addWidget(self.pushButton_Stop, 0, 2, 1, 1)
        self.pushButton_clearFields = QtWidgets.QPushButton(self.widget1)
        self.pushButton_clearFields.setMinimumSize(QtCore.QSize(75, 0))
        self.pushButton_clearFields.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_clearFields.setFont(font)
        self.pushButton_clearFields.setObjectName("pushButton_clearFields")
        self.gridLayout.addWidget(self.pushButton_clearFields, 1, 0, 1, 1)
        self.pushButton_Refresh = QtWidgets.QPushButton(self.widget1)
        self.pushButton_Refresh.setMinimumSize(QtCore.QSize(75, 0))
        self.pushButton_Refresh.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_Refresh.setFont(font)
        self.pushButton_Refresh.setObjectName("pushButton_Refresh")
        self.gridLayout.addWidget(self.pushButton_Refresh, 1, 1, 1, 1)
        self.comboBox_Running = QtWidgets.QComboBox(self.widget1)
        self.comboBox_Running.setMinimumSize(QtCore.QSize(75, 0))
        self.comboBox_Running.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_Running.setFont(font)
        self.comboBox_Running.setObjectName("comboBox_Running")
        self.comboBox_Running.addItem("")
        self.comboBox_Running.addItem("")
        self.comboBox_Running.addItem("")
        self.gridLayout.addWidget(self.comboBox_Running, 1, 2, 1, 1)
        self.listView_table = QtWidgets.QListView(self.splitter)
        self.listView_table.setMinimumSize(QtCore.QSize(280, 650))
        self.listView_table.setMaximumSize(QtCore.QSize(300, 650))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listView_table.setFont(font)
        self.listView_table.setObjectName("listView_table")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_loggingBox = QtWidgets.QTextEdit(self.splitter_2)
        self.textEdit_loggingBox.setMinimumSize(QtCore.QSize(0, 250))
        self.textEdit_loggingBox.setMaximumSize(QtCore.QSize(16777215, 200))
        self.textEdit_loggingBox.setObjectName("textEdit_loggingBox")
        self.tabWidget.addTab(self.tab_settings, "")
        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1144, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_Name.setText(_translate("MainWindow", "Name"))
        self.label_SMS.setText(_translate("MainWindow", "SMS"))
        self.label_Email.setText(_translate("MainWindow", "                                                                                                            "))
        self.label_Email_2.setText(_translate("MainWindow", "EMAIL"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main), _translate("MainWindow", "Tab 1"))
        self.label_field.setText(_translate("MainWindow", "Field"))
        self.label_Last.setText(_translate("MainWindow", "Last Measured"))
        self.label_Limit.setText(_translate("MainWindow", "Safe When"))
        self.label_action.setText(_translate("MainWindow", "Action"))
        self.label_status.setText(_translate("MainWindow", "Status"))
        self.comboBox_Server_Location.setItemText(0, _translate("MainWindow", "blue"))
        self.comboBox_Server_Location.setItemText(1, _translate("MainWindow", "green"))
        self.comboBox_Server_Location.setItemText(2, _translate("MainWindow", "local"))
        self.comboBox_Server_Location.setItemText(3, _translate("MainWindow", "skellig"))
        self.pushButton_Start.setText(_translate("MainWindow", "Start"))
        self.pushButton_Stop.setText(_translate("MainWindow", "Stop"))
        self.pushButton_clearFields.setText(_translate("MainWindow", "Clear Fields"))
        self.pushButton_Refresh.setText(_translate("MainWindow", "Refresh Files"))
        self.comboBox_Running.setItemText(0, _translate("MainWindow", "WAITING"))
        self.comboBox_Running.setItemText(1, _translate("MainWindow", "RUNNING"))
        self.comboBox_Running.setItemText(2, _translate("MainWindow", "ERROR"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), _translate("MainWindow", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
