# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/viero/Repositories/SPHEREx-lab-tools-11012022/spherexanalysistools/gui/QTDesigner/mySQLQueryWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1742, 1060)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_SQL_Database_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_SQL_Database_4.sizePolicy().hasHeightForWidth())
        self.label_SQL_Database_4.setSizePolicy(sizePolicy)
        self.label_SQL_Database_4.setMaximumSize(QtCore.QSize(160, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_SQL_Database_4.setFont(font)
        self.label_SQL_Database_4.setObjectName("label_SQL_Database_4")
        self.verticalLayout_6.addWidget(self.label_SQL_Database_4)
        self.comboBox_Server_Location = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_Server_Location.sizePolicy().hasHeightForWidth())
        self.comboBox_Server_Location.setSizePolicy(sizePolicy)
        self.comboBox_Server_Location.setMaximumSize(QtCore.QSize(160, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_Server_Location.setFont(font)
        self.comboBox_Server_Location.setObjectName("comboBox_Server_Location")
        self.comboBox_Server_Location.addItem("")
        self.comboBox_Server_Location.addItem("")
        self.comboBox_Server_Location.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_Server_Location)
        self.label_SQL_Database = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_SQL_Database.sizePolicy().hasHeightForWidth())
        self.label_SQL_Database.setSizePolicy(sizePolicy)
        self.label_SQL_Database.setMaximumSize(QtCore.QSize(160, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_SQL_Database.setFont(font)
        self.label_SQL_Database.setObjectName("label_SQL_Database")
        self.verticalLayout_6.addWidget(self.label_SQL_Database)
        self.comboBox_database_name = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_database_name.setMaximumSize(QtCore.QSize(160, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_database_name.setFont(font)
        self.comboBox_database_name.setObjectName("comboBox_database_name")
        self.verticalLayout_6.addWidget(self.comboBox_database_name)
        self.label_SQL_Database_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_SQL_Database_2.sizePolicy().hasHeightForWidth())
        self.label_SQL_Database_2.setSizePolicy(sizePolicy)
        self.label_SQL_Database_2.setMaximumSize(QtCore.QSize(160, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_SQL_Database_2.setFont(font)
        self.label_SQL_Database_2.setObjectName("label_SQL_Database_2")
        self.verticalLayout_6.addWidget(self.label_SQL_Database_2)
        self.comboBox_table_name = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_table_name.sizePolicy().hasHeightForWidth())
        self.comboBox_table_name.setSizePolicy(sizePolicy)
        self.comboBox_table_name.setMaximumSize(QtCore.QSize(160, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_table_name.setFont(font)
        self.comboBox_table_name.setObjectName("comboBox_table_name")
        self.verticalLayout_6.addWidget(self.comboBox_table_name)
        self.label_SQL_Database_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_SQL_Database_3.sizePolicy().hasHeightForWidth())
        self.label_SQL_Database_3.setSizePolicy(sizePolicy)
        self.label_SQL_Database_3.setMaximumSize(QtCore.QSize(160, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_SQL_Database_3.setFont(font)
        self.label_SQL_Database_3.setObjectName("label_SQL_Database_3")
        self.verticalLayout_6.addWidget(self.label_SQL_Database_3)
        self.listView_table = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_table.sizePolicy().hasHeightForWidth())
        self.listView_table.setSizePolicy(sizePolicy)
        self.listView_table.setMaximumSize(QtCore.QSize(160, 16777215))
        self.listView_table.setObjectName("listView_table")
        self.verticalLayout_6.addWidget(self.listView_table)
        self.gridLayout_6.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.comboBox_scriptedQueries = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_scriptedQueries.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_scriptedQueries.setFont(font)
        self.comboBox_scriptedQueries.setObjectName("comboBox_scriptedQueries")
        self.comboBox_scriptedQueries.addItem("")
        self.verticalLayout_5.addWidget(self.comboBox_scriptedQueries)
        self.textEdit_SQL_Query = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_SQL_Query.setFont(font)
        self.textEdit_SQL_Query.setObjectName("textEdit_SQL_Query")
        self.verticalLayout_5.addWidget(self.textEdit_SQL_Query)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_downloadPath = QtWidgets.QLabel(self.centralwidget)
        self.label_downloadPath.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_downloadPath.setFont(font)
        self.label_downloadPath.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_downloadPath.setObjectName("label_downloadPath")
        self.gridLayout.addWidget(self.label_downloadPath, 2, 3, 1, 1)
        self.label_exportPath = QtWidgets.QLabel(self.centralwidget)
        self.label_exportPath.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_exportPath.setFont(font)
        self.label_exportPath.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_exportPath.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_exportPath.setObjectName("label_exportPath")
        self.gridLayout.addWidget(self.label_exportPath, 1, 3, 1, 1)
        self.button_ClearQuery = QtWidgets.QPushButton(self.centralwidget)
        self.button_ClearQuery.setMinimumSize(QtCore.QSize(120, 30))
        self.button_ClearQuery.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_ClearQuery.setFont(font)
        self.button_ClearQuery.setObjectName("button_ClearQuery")
        self.gridLayout.addWidget(self.button_ClearQuery, 0, 2, 1, 1)
        self.button_SaveQuery = QtWidgets.QPushButton(self.centralwidget)
        self.button_SaveQuery.setMinimumSize(QtCore.QSize(140, 0))
        self.button_SaveQuery.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_SaveQuery.setFont(font)
        self.button_SaveQuery.setObjectName("button_SaveQuery")
        self.gridLayout.addWidget(self.button_SaveQuery, 0, 3, 1, 1)
        self.button_RunQuery = QtWidgets.QPushButton(self.centralwidget)
        self.button_RunQuery.setMinimumSize(QtCore.QSize(140, 0))
        self.button_RunQuery.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_RunQuery.setFont(font)
        self.button_RunQuery.setObjectName("button_RunQuery")
        self.gridLayout.addWidget(self.button_RunQuery, 0, 1, 1, 1)
        self.button_ExportCSV = QtWidgets.QPushButton(self.centralwidget)
        self.button_ExportCSV.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_ExportCSV.setFont(font)
        self.button_ExportCSV.setObjectName("button_ExportCSV")
        self.gridLayout.addWidget(self.button_ExportCSV, 1, 2, 1, 1)
        self.button_LoadCSV = QtWidgets.QPushButton(self.centralwidget)
        self.button_LoadCSV.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_LoadCSV.setFont(font)
        self.button_LoadCSV.setObjectName("button_LoadCSV")
        self.gridLayout.addWidget(self.button_LoadCSV, 1, 1, 1, 1)
        self.button_DownloadData = QtWidgets.QPushButton(self.centralwidget)
        self.button_DownloadData.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_DownloadData.setFont(font)
        self.button_DownloadData.setObjectName("button_DownloadData")
        self.gridLayout.addWidget(self.button_DownloadData, 2, 2, 1, 1)
        self.button_ClearTable = QtWidgets.QPushButton(self.centralwidget)
        self.button_ClearTable.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_ClearTable.setFont(font)
        self.button_ClearTable.setObjectName("button_ClearTable")
        self.gridLayout.addWidget(self.button_ClearTable, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lineEdit_SQL_Save_Query = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_SQL_Save_Query.setFont(font)
        self.lineEdit_SQL_Save_Query.setObjectName("lineEdit_SQL_Save_Query")
        self.verticalLayout_7.addWidget(self.lineEdit_SQL_Save_Query)
        self.lineEdit_ExportCSV = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_ExportCSV.setFont(font)
        self.lineEdit_ExportCSV.setObjectName("lineEdit_ExportCSV")
        self.verticalLayout_7.addWidget(self.lineEdit_ExportCSV)
        self.lineEdit_ExportFITS = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_ExportFITS.setFont(font)
        self.lineEdit_ExportFITS.setObjectName("lineEdit_ExportFITS")
        self.verticalLayout_7.addWidget(self.lineEdit_ExportFITS)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.gridLayout_4.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.button_Include_Lockin = QtWidgets.QPushButton(self.centralwidget)
        self.button_Include_Lockin.setMinimumSize(QtCore.QSize(0, 30))
        self.button_Include_Lockin.setMaximumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_Include_Lockin.setFont(font)
        self.button_Include_Lockin.setObjectName("button_Include_Lockin")
        self.verticalLayout_4.addWidget(self.button_Include_Lockin)
        self.button_Include_Blue = QtWidgets.QPushButton(self.centralwidget)
        self.button_Include_Blue.setMinimumSize(QtCore.QSize(0, 30))
        self.button_Include_Blue.setMaximumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_Include_Blue.setFont(font)
        self.button_Include_Blue.setObjectName("button_Include_Blue")
        self.verticalLayout_4.addWidget(self.button_Include_Blue)
        self.button_Include_Green = QtWidgets.QPushButton(self.centralwidget)
        self.button_Include_Green.setMinimumSize(QtCore.QSize(180, 30))
        self.button_Include_Green.setMaximumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_Include_Green.setFont(font)
        self.button_Include_Green.setObjectName("button_Include_Green")
        self.verticalLayout_4.addWidget(self.button_Include_Green)
        self.button_Import_Wavelengths = QtWidgets.QPushButton(self.centralwidget)
        self.button_Import_Wavelengths.setMinimumSize(QtCore.QSize(0, 30))
        self.button_Import_Wavelengths.setMaximumSize(QtCore.QSize(1000, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_Import_Wavelengths.setFont(font)
        self.button_Import_Wavelengths.setObjectName("button_Import_Wavelengths")
        self.verticalLayout_4.addWidget(self.button_Import_Wavelengths)
        self.doubleSpinBox_lower = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_lower.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.doubleSpinBox_lower.setFont(font)
        self.doubleSpinBox_lower.setDecimals(3)
        self.doubleSpinBox_lower.setProperty("value", 0.7)
        self.doubleSpinBox_lower.setObjectName("doubleSpinBox_lower")
        self.verticalLayout_4.addWidget(self.doubleSpinBox_lower)
        self.doubleSpinBox_upper = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_upper.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.doubleSpinBox_upper.setFont(font)
        self.doubleSpinBox_upper.setDecimals(3)
        self.doubleSpinBox_upper.setProperty("value", 1.36)
        self.doubleSpinBox_upper.setObjectName("doubleSpinBox_upper")
        self.verticalLayout_4.addWidget(self.doubleSpinBox_upper)
        self.label_SQL_Database_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_SQL_Database_9.setMinimumSize(QtCore.QSize(0, 25))
        self.label_SQL_Database_9.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_SQL_Database_9.setFont(font)
        self.label_SQL_Database_9.setObjectName("label_SQL_Database_9")
        self.verticalLayout_4.addWidget(self.label_SQL_Database_9)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout_2.addWidget(self.checkBox_5, 2, 1, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_2.addWidget(self.checkBox_3, 3, 0, 1, 1)
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout_2.addWidget(self.checkBox_6, 3, 1, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_2.addWidget(self.checkBox_4, 1, 1, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 2, 0, 1, 1)
        self.checkBox_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_1.setObjectName("checkBox_1")
        self.gridLayout_2.addWidget(self.checkBox_1, 1, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.gridLayout_5.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_SQL_Database_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_SQL_Database_6.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_SQL_Database_6.setFont(font)
        self.label_SQL_Database_6.setObjectName("label_SQL_Database_6")
        self.verticalLayout.addWidget(self.label_SQL_Database_6)
        self.label_SQL_Database_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_SQL_Database_8.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.label_SQL_Database_8.setFont(font)
        self.label_SQL_Database_8.setObjectName("label_SQL_Database_8")
        self.verticalLayout.addWidget(self.label_SQL_Database_8)
        self.checkBox_PIX_all_frames = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBox_PIX_all_frames.setFont(font)
        self.checkBox_PIX_all_frames.setObjectName("checkBox_PIX_all_frames")
        self.verticalLayout.addWidget(self.checkBox_PIX_all_frames)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_PIX_between_frames = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_PIX_between_frames.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBox_PIX_between_frames.setFont(font)
        self.checkBox_PIX_between_frames.setObjectName("checkBox_PIX_between_frames")
        self.horizontalLayout.addWidget(self.checkBox_PIX_between_frames)
        self.spinBox_PIX_frames_lo = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_PIX_frames_lo.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_PIX_frames_lo.setObjectName("spinBox_PIX_frames_lo")
        self.horizontalLayout.addWidget(self.spinBox_PIX_frames_lo)
        self.spinBox_PIX_frames_hi = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_PIX_frames_hi.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_PIX_frames_hi.setObjectName("spinBox_PIX_frames_hi")
        self.horizontalLayout.addWidget(self.spinBox_PIX_frames_hi)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkBox_include_frame_data_RST = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_include_frame_data_RST.setFont(font)
        self.checkBox_include_frame_data_RST.setObjectName("checkBox_include_frame_data_RST")
        self.verticalLayout.addWidget(self.checkBox_include_frame_data_RST)
        self.checkBox_include_frame_data_SUR = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_include_frame_data_SUR.setFont(font)
        self.checkBox_include_frame_data_SUR.setObjectName("checkBox_include_frame_data_SUR")
        self.verticalLayout.addWidget(self.checkBox_include_frame_data_SUR)
        self.gridLayout_5.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_SQL_Database_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_SQL_Database_7.setFont(font)
        self.label_SQL_Database_7.setObjectName("label_SQL_Database_7")
        self.verticalLayout_2.addWidget(self.label_SQL_Database_7)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        self.checkBox_lab_output_unCorr = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_lab_output_unCorr.setFont(font)
        self.checkBox_lab_output_unCorr.setChecked(True)
        self.checkBox_lab_output_unCorr.setObjectName("checkBox_lab_output_unCorr")
        self.verticalLayout_2.addWidget(self.checkBox_lab_output_unCorr)
        self.checkBox_lab_output_phantom = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_lab_output_phantom.setFont(font)
        self.checkBox_lab_output_phantom.setChecked(True)
        self.checkBox_lab_output_phantom.setObjectName("checkBox_lab_output_phantom")
        self.verticalLayout_2.addWidget(self.checkBox_lab_output_phantom)
        self.checkBox_lab_output_phanCorr = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_lab_output_phanCorr.setFont(font)
        self.checkBox_lab_output_phanCorr.setChecked(True)
        self.checkBox_lab_output_phanCorr.setObjectName("checkBox_lab_output_phanCorr")
        self.verticalLayout_2.addWidget(self.checkBox_lab_output_phanCorr)
        self.checkBox_lab_output_refCorr = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_lab_output_refCorr.setFont(font)
        self.checkBox_lab_output_refCorr.setChecked(True)
        self.checkBox_lab_output_refCorr.setObjectName("checkBox_lab_output_refCorr")
        self.verticalLayout_2.addWidget(self.checkBox_lab_output_refCorr)
        self.gridLayout_5.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.button_Import_All = QtWidgets.QPushButton(self.centralwidget)
        self.button_Import_All.setMinimumSize(QtCore.QSize(0, 30))
        self.button_Import_All.setMaximumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_Import_All.setFont(font)
        self.button_Import_All.setObjectName("button_Import_All")
        self.verticalLayout_3.addWidget(self.button_Import_All)
        self.button_Import_Last_Hour = QtWidgets.QPushButton(self.centralwidget)
        self.button_Import_Last_Hour.setMinimumSize(QtCore.QSize(0, 30))
        self.button_Import_Last_Hour.setMaximumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_Import_Last_Hour.setFont(font)
        self.button_Import_Last_Hour.setObjectName("button_Import_Last_Hour")
        self.verticalLayout_3.addWidget(self.button_Import_Last_Hour)
        self.button_Import_Last_Day = QtWidgets.QPushButton(self.centralwidget)
        self.button_Import_Last_Day.setMinimumSize(QtCore.QSize(0, 30))
        self.button_Import_Last_Day.setMaximumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_Import_Last_Day.setFont(font)
        self.button_Import_Last_Day.setObjectName("button_Import_Last_Day")
        self.verticalLayout_3.addWidget(self.button_Import_Last_Day)
        self.button_Import_Between = QtWidgets.QPushButton(self.centralwidget)
        self.button_Import_Between.setMinimumSize(QtCore.QSize(0, 30))
        self.button_Import_Between.setMaximumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_Import_Between.setFont(font)
        self.button_Import_Between.setObjectName("button_Import_Between")
        self.verticalLayout_3.addWidget(self.button_Import_Between)
        self.dateTimeEdit_start = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_start.setMinimumSize(QtCore.QSize(0, 30))
        self.dateTimeEdit_start.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dateTimeEdit_start.setFont(font)
        self.dateTimeEdit_start.setObjectName("dateTimeEdit_start")
        self.verticalLayout_3.addWidget(self.dateTimeEdit_start)
        self.dateTimeEdit_end = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_end.setMinimumSize(QtCore.QSize(0, 30))
        self.dateTimeEdit_end.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dateTimeEdit_end.setFont(font)
        self.dateTimeEdit_end.setObjectName("dateTimeEdit_end")
        self.verticalLayout_3.addWidget(self.dateTimeEdit_end)
        self.label_SQL_Database_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_SQL_Database_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_SQL_Database_5.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_SQL_Database_5.setFont(font)
        self.label_SQL_Database_5.setObjectName("label_SQL_Database_5")
        self.verticalLayout_3.addWidget(self.label_SQL_Database_5)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBox_all_eng = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_all_eng.setChecked(False)
        self.checkBox_all_eng.setObjectName("checkBox_all_eng")
        self.gridLayout_3.addWidget(self.checkBox_all_eng, 0, 0, 1, 1)
        self.checkBox_9 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_9.setChecked(False)
        self.checkBox_9.setObjectName("checkBox_9")
        self.gridLayout_3.addWidget(self.checkBox_9, 2, 1, 1, 1)
        self.checkBox_8 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_8.setChecked(False)
        self.checkBox_8.setObjectName("checkBox_8")
        self.gridLayout_3.addWidget(self.checkBox_8, 1, 1, 1, 1)
        self.checkBox_7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_7.setChecked(False)
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout_3.addWidget(self.checkBox_7, 2, 0, 1, 1)
        self.checkBox_0 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_0.setChecked(True)
        self.checkBox_0.setObjectName("checkBox_0")
        self.gridLayout_3.addWidget(self.checkBox_0, 1, 0, 1, 1)
        self.checkBox_all_flight = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_all_flight.setChecked(False)
        self.checkBox_all_flight.setObjectName("checkBox_all_flight")
        self.gridLayout_3.addWidget(self.checkBox_all_flight, 0, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.gridLayout_5.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_5, 0, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)
        self.tableView_SQL_Results = QtWidgets.QTableView(self.centralwidget)
        self.tableView_SQL_Results.setObjectName("tableView_SQL_Results")
        self.gridLayout_4.addWidget(self.tableView_SQL_Results, 2, 0, 1, 2)
        self.gridLayout_6.addLayout(self.gridLayout_4, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1742, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_SQL_Database_4.setText(_translate("MainWindow", "SQL Location"))
        self.comboBox_Server_Location.setItemText(0, _translate("MainWindow", "ragnarok"))
        self.comboBox_Server_Location.setItemText(1, _translate("MainWindow", "local"))
        self.comboBox_Server_Location.setItemText(2, _translate("MainWindow", "green"))
        self.label_SQL_Database.setText(_translate("MainWindow", "SQL Database"))
        self.label_SQL_Database_2.setText(_translate("MainWindow", " Table"))
        self.label_SQL_Database_3.setText(_translate("MainWindow", "Columns"))
        self.comboBox_scriptedQueries.setItemText(0, _translate("MainWindow", "SAVED QUERIES"))
        self.textEdit_SQL_Query.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">select * from control_software</span></p></body></html>"))
        self.label_downloadPath.setText(_translate("MainWindow", "Download Path:"))
        self.label_exportPath.setText(_translate("MainWindow", "CSV Path:"))
        self.button_ClearQuery.setText(_translate("MainWindow", "Clear Query"))
        self.button_SaveQuery.setText(_translate("MainWindow", "Save Query"))
        self.button_RunQuery.setText(_translate("MainWindow", "Run Query"))
        self.button_ExportCSV.setText(_translate("MainWindow", "Export CSV"))
        self.button_LoadCSV.setText(_translate("MainWindow", "Load CSV"))
        self.button_DownloadData.setText(_translate("MainWindow", "Download Data"))
        self.button_ClearTable.setText(_translate("MainWindow", "Clear Table"))
        self.lineEdit_SQL_Save_Query.setText(_translate("MainWindow", "Saved Query Name"))
        self.lineEdit_ExportCSV.setText(_translate("MainWindow", "D:\\\\spherex\\\\mySQL\\\\exportedCSV\\\\"))
        self.lineEdit_ExportFITS.setText(_translate("MainWindow", "D:\\\\spherex\\\\mySQL\\\\Downloads\\\\"))
        self.button_Include_Lockin.setText(_translate("MainWindow", "Include Lockin"))
        self.button_Include_Blue.setText(_translate("MainWindow", "Include Blue"))
        self.button_Include_Green.setText(_translate("MainWindow", "Include Green"))
        self.button_Import_Wavelengths.setText(_translate("MainWindow", "Between Wavelengths"))
        self.label_SQL_Database_9.setText(_translate("MainWindow", "Flight Detectors"))
        self.checkBox_5.setText(_translate("MainWindow", "05-XXXXX"))
        self.checkBox_3.setText(_translate("MainWindow", "03-XXXXX"))
        self.checkBox_6.setText(_translate("MainWindow", "06-XXXXX"))
        self.checkBox_4.setText(_translate("MainWindow", "04-XXXXX"))
        self.checkBox_2.setText(_translate("MainWindow", "02-XXXXX"))
        self.checkBox_1.setText(_translate("MainWindow", "01-XXXXX"))
        self.label_SQL_Database_6.setText(_translate("MainWindow", "FRAME_DATA"))
        self.label_SQL_Database_8.setText(_translate("MainWindow", "Frames/PIX:"))
        self.checkBox_PIX_all_frames.setText(_translate("MainWindow", "All"))
        self.checkBox_PIX_between_frames.setText(_translate("MainWindow", "Between"))
        self.checkBox_include_frame_data_RST.setText(_translate("MainWindow", "Frames/RST"))
        self.checkBox_include_frame_data_SUR.setText(_translate("MainWindow", "Frames/SUR"))
        self.label_SQL_Database_7.setText(_translate("MainWindow", "LAB_OUTPUT"))
        self.checkBox.setText(_translate("MainWindow", "SampleUpRamp"))
        self.checkBox_lab_output_unCorr.setText(_translate("MainWindow", "unCorr"))
        self.checkBox_lab_output_phantom.setText(_translate("MainWindow", "phantom"))
        self.checkBox_lab_output_phanCorr.setText(_translate("MainWindow", "phanCorr"))
        self.checkBox_lab_output_refCorr.setText(_translate("MainWindow", "refCorr"))
        self.button_Import_All.setText(_translate("MainWindow", "Import All"))
        self.button_Import_Last_Hour.setText(_translate("MainWindow", "Import Last Hour"))
        self.button_Import_Last_Day.setText(_translate("MainWindow", "Import Last Day"))
        self.button_Import_Between.setText(_translate("MainWindow", " Between Date/Times"))
        self.dateTimeEdit_start.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH:mm:ss"))
        self.dateTimeEdit_end.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH:mm:ss"))
        self.label_SQL_Database_5.setText(_translate("MainWindow", "Engineering Detectors"))
        self.checkBox_all_eng.setText(_translate("MainWindow", "All Engineering"))
        self.checkBox_9.setText(_translate("MainWindow", "09-21708"))
        self.checkBox_8.setText(_translate("MainWindow", "08-22145"))
        self.checkBox_7.setText(_translate("MainWindow", "07-XXXXX"))
        self.checkBox_0.setText(_translate("MainWindow", "00-18831"))
        self.checkBox_all_flight.setText(_translate("MainWindow", "All Flight"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
