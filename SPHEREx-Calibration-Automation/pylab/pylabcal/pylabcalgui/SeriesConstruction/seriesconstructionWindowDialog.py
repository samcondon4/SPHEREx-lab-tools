# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'seriesconstructionWindowDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1551, 1650)
        self.main_layout = QtWidgets.QGridLayout(Form)
        self.main_layout.setObjectName("main_layout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.main_layout.addWidget(self.label, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.main_layout.addWidget(self.line, 1, 0, 1, 2)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.auto_series_sequence_name_label = QtWidgets.QLabel(Form)
        self.auto_series_sequence_name_label.setObjectName("auto_series_sequence_name_label")
        self.gridLayout_13.addWidget(self.auto_series_sequence_name_label, 0, 0, 1, 1)
        self.auto_series_savedsequences_list = QtWidgets.QListWidget(Form)
        self.auto_series_savedsequences_list.setObjectName("auto_series_savedsequences_list")
        self.gridLayout_13.addWidget(self.auto_series_savedsequences_list, 4, 0, 1, 1)
        self.auto_series_sequence_save_button = QtWidgets.QPushButton(Form)
        self.auto_series_sequence_save_button.setObjectName("auto_series_sequence_save_button")
        self.gridLayout_13.addWidget(self.auto_series_sequence_save_button, 2, 0, 1, 1)
        self.auto_series_sequence_name_ledit = QtWidgets.QLineEdit(Form)
        self.auto_series_sequence_name_ledit.setObjectName("auto_series_sequence_name_ledit")
        self.gridLayout_13.addWidget(self.auto_series_sequence_name_ledit, 1, 0, 1, 1)
        self.auto_series_savedsequences_label = QtWidgets.QLabel(Form)
        self.auto_series_savedsequences_label.setObjectName("auto_series_savedsequences_label")
        self.gridLayout_13.addWidget(self.auto_series_savedsequences_label, 3, 0, 1, 1)
        self.auto_series_addsequencestoseries_button = QtWidgets.QPushButton(Form)
        self.auto_series_addsequencestoseries_button.setObjectName("auto_series_addsequencestoseries_button")
        self.gridLayout_13.addWidget(self.auto_series_addsequencestoseries_button, 5, 0, 1, 1)
        self.main_layout.addLayout(self.gridLayout_13, 2, 0, 1, 1)
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.auto_series_removesequencefromseries_button = QtWidgets.QPushButton(Form)
        self.auto_series_removesequencefromseries_button.setObjectName("auto_series_removesequencefromseries_button")
        self.gridLayout_15.addWidget(self.auto_series_removesequencefromseries_button, 2, 0, 1, 1)
        self.auto_series_series_label = QtWidgets.QLabel(Form)
        self.auto_series_series_label.setObjectName("auto_series_series_label")
        self.gridLayout_15.addWidget(self.auto_series_series_label, 0, 0, 1, 1)
        self.auto_series_series_list = QtWidgets.QListWidget(Form)
        self.auto_series_series_list.setObjectName("auto_series_series_list")
        self.gridLayout_15.addWidget(self.auto_series_series_list, 1, 0, 1, 1)
        self.auto_series_removeallsequencesfromseries_button = QtWidgets.QPushButton(Form)
        self.auto_series_removeallsequencesfromseries_button.setObjectName("auto_series_removeallsequencesfromseries_button")
        self.gridLayout_15.addWidget(self.auto_series_removeallsequencesfromseries_button, 3, 0, 1, 1)
        self.main_layout.addLayout(self.gridLayout_15, 2, 1, 1, 1)
        self.auto_data_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.auto_data_label.setFont(font)
        self.auto_data_label.setObjectName("auto_data_label")
        self.main_layout.addWidget(self.auto_data_label, 3, 0, 1, 2)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.main_layout.addWidget(self.line_2, 4, 0, 1, 2)
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.auto_data_metadatatoinclude_label = QtWidgets.QLabel(Form)
        self.auto_data_metadatatoinclude_label.setObjectName("auto_data_metadatatoinclude_label")
        self.gridLayout_16.addWidget(self.auto_data_metadatatoinclude_label, 0, 1, 1, 2)
        self.data_configuration_metadata_ndfwheel_position_checkbox = QtWidgets.QCheckBox(Form)
        self.data_configuration_metadata_ndfwheel_position_checkbox.setObjectName("data_configuration_metadata_ndfwheel_position_checkbox")
        self.gridLayout_16.addWidget(self.data_configuration_metadata_ndfwheel_position_checkbox, 6, 2, 1, 1)
        self.data_configuration_metadata_labjack_diostate_checkbox = QtWidgets.QCheckBox(Form)
        self.data_configuration_metadata_labjack_diostate_checkbox.setObjectName("data_configuration_metadata_labjack_diostate_checkbox")
        self.gridLayout_16.addWidget(self.data_configuration_metadata_labjack_diostate_checkbox, 6, 1, 1, 1)
        self.data_configuration_metadata_grating_cbox = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_configuration_metadata_grating_cbox.sizePolicy().hasHeightForWidth())
        self.data_configuration_metadata_grating_cbox.setSizePolicy(sizePolicy)
        self.data_configuration_metadata_grating_cbox.setChecked(True)
        self.data_configuration_metadata_grating_cbox.setObjectName("data_configuration_metadata_grating_cbox")
        self.gridLayout_16.addWidget(self.data_configuration_metadata_grating_cbox, 1, 2, 2, 1)
        self.data_configuration_metadata_lockints_cbox = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_configuration_metadata_lockints_cbox.sizePolicy().hasHeightForWidth())
        self.data_configuration_metadata_lockints_cbox.setSizePolicy(sizePolicy)
        self.data_configuration_metadata_lockints_cbox.setChecked(True)
        self.data_configuration_metadata_lockints_cbox.setObjectName("data_configuration_metadata_lockints_cbox")
        self.gridLayout_16.addWidget(self.data_configuration_metadata_lockints_cbox, 4, 2, 1, 1)
        self.data_configuration_metadata_lockin_sensitivity_cbox = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_configuration_metadata_lockin_sensitivity_cbox.sizePolicy().hasHeightForWidth())
        self.data_configuration_metadata_lockin_sensitivity_cbox.setSizePolicy(sizePolicy)
        self.data_configuration_metadata_lockin_sensitivity_cbox.setChecked(True)
        self.data_configuration_metadata_lockin_sensitivity_cbox.setObjectName("data_configuration_metadata_lockin_sensitivity_cbox")
        self.gridLayout_16.addWidget(self.data_configuration_metadata_lockin_sensitivity_cbox, 5, 2, 1, 1)
        self.data_configuration_metadata_shutter_cbox = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_configuration_metadata_shutter_cbox.sizePolicy().hasHeightForWidth())
        self.data_configuration_metadata_shutter_cbox.setSizePolicy(sizePolicy)
        self.data_configuration_metadata_shutter_cbox.setChecked(True)
        self.data_configuration_metadata_shutter_cbox.setObjectName("data_configuration_metadata_shutter_cbox")
        self.gridLayout_16.addWidget(self.data_configuration_metadata_shutter_cbox, 3, 2, 1, 1)
        self.auto_data_metadata_lockinfs_cbox = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_data_metadata_lockinfs_cbox.sizePolicy().hasHeightForWidth())
        self.auto_data_metadata_lockinfs_cbox.setSizePolicy(sizePolicy)
        self.auto_data_metadata_lockinfs_cbox.setChecked(True)
        self.auto_data_metadata_lockinfs_cbox.setObjectName("auto_data_metadata_lockinfs_cbox")
        self.gridLayout_16.addWidget(self.auto_data_metadata_lockinfs_cbox, 4, 1, 1, 1)
        self.auto_data_metadata_wavelength_cbox = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_data_metadata_wavelength_cbox.sizePolicy().hasHeightForWidth())
        self.auto_data_metadata_wavelength_cbox.setSizePolicy(sizePolicy)
        self.auto_data_metadata_wavelength_cbox.setChecked(True)
        self.auto_data_metadata_wavelength_cbox.setObjectName("auto_data_metadata_wavelength_cbox")
        self.gridLayout_16.addWidget(self.auto_data_metadata_wavelength_cbox, 1, 1, 2, 1)
        self.auto_data_metadata_osf_cbox = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_data_metadata_osf_cbox.sizePolicy().hasHeightForWidth())
        self.auto_data_metadata_osf_cbox.setSizePolicy(sizePolicy)
        self.auto_data_metadata_osf_cbox.setChecked(True)
        self.auto_data_metadata_osf_cbox.setObjectName("auto_data_metadata_osf_cbox")
        self.gridLayout_16.addWidget(self.auto_data_metadata_osf_cbox, 3, 1, 1, 1)
        self.auto_data_metadata_lockintimeconstant_cbox = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_data_metadata_lockintimeconstant_cbox.sizePolicy().hasHeightForWidth())
        self.auto_data_metadata_lockintimeconstant_cbox.setSizePolicy(sizePolicy)
        self.auto_data_metadata_lockintimeconstant_cbox.setChecked(True)
        self.auto_data_metadata_lockintimeconstant_cbox.setObjectName("auto_data_metadata_lockintimeconstant_cbox")
        self.gridLayout_16.addWidget(self.auto_data_metadata_lockintimeconstant_cbox, 5, 1, 1, 1)
        self.auto_data_exposure_duration_ledit = QtWidgets.QLineEdit(Form)
        self.auto_data_exposure_duration_ledit.setObjectName("auto_data_exposure_duration_ledit")
        self.gridLayout_16.addWidget(self.auto_data_exposure_duration_ledit, 10, 2, 1, 1)
        self.auto_data_exposure_duration_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_data_exposure_duration_label.sizePolicy().hasHeightForWidth())
        self.auto_data_exposure_duration_label.setSizePolicy(sizePolicy)
        self.auto_data_exposure_duration_label.setObjectName("auto_data_exposure_duration_label")
        self.gridLayout_16.addWidget(self.auto_data_exposure_duration_label, 10, 1, 1, 1)
        self.auto_data_storagepath_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_data_storagepath_label.sizePolicy().hasHeightForWidth())
        self.auto_data_storagepath_label.setSizePolicy(sizePolicy)
        self.auto_data_storagepath_label.setObjectName("auto_data_storagepath_label")
        self.gridLayout_16.addWidget(self.auto_data_storagepath_label, 7, 1, 1, 1)
        self.auto_data_storagepath_ledit = QtWidgets.QLineEdit(Form)
        self.auto_data_storagepath_ledit.setObjectName("auto_data_storagepath_ledit")
        self.gridLayout_16.addWidget(self.auto_data_storagepath_ledit, 7, 2, 1, 1)
        self.main_layout.addLayout(self.gridLayout_16, 5, 0, 1, 2)
        self.auto_control_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.auto_control_label.setFont(font)
        self.auto_control_label.setObjectName("auto_control_label")
        self.main_layout.addWidget(self.auto_control_label, 6, 0, 1, 2)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.main_layout.addWidget(self.line_3, 7, 0, 1, 2)
        self.auto_control_runseries_button = QtWidgets.QPushButton(Form)
        self.auto_control_runseries_button.setObjectName("auto_control_runseries_button")
        self.main_layout.addWidget(self.auto_control_runseries_button, 8, 0, 1, 2)
        self.auto_control_pauseseries_button = QtWidgets.QPushButton(Form)
        self.auto_control_pauseseries_button.setObjectName("auto_control_pauseseries_button")
        self.main_layout.addWidget(self.auto_control_pauseseries_button, 9, 0, 1, 2)
        self.auto_control_abortseries_button = QtWidgets.QPushButton(Form)
        self.auto_control_abortseries_button.setObjectName("auto_control_abortseries_button")
        self.main_layout.addWidget(self.auto_control_abortseries_button, 10, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Series Construction"))
        self.label.setText(_translate("Form", "Series Construction:"))
        self.auto_series_sequence_name_label.setText(_translate("Form", "Sequence Name:"))
        self.auto_series_sequence_save_button.setText(_translate("Form", "Save New Sequence"))
        self.auto_series_savedsequences_label.setText(_translate("Form", "Saved Sequences:"))
        self.auto_series_addsequencestoseries_button.setText(_translate("Form", "Add Sequence To Series"))
        self.auto_series_removesequencefromseries_button.setText(_translate("Form", "Remove Sequence From Series"))
        self.auto_series_series_label.setText(_translate("Form", "Series:"))
        self.auto_series_removeallsequencesfromseries_button.setText(_translate("Form", "Remove All Sequences From Series"))
        self.auto_data_label.setText(_translate("Form", "Data Configuration:"))
        self.auto_data_metadatatoinclude_label.setText(_translate("Form", "Metadata to Include:"))
        self.data_configuration_metadata_ndfwheel_position_checkbox.setText(_translate("Form", "NDF Wheel Position"))
        self.data_configuration_metadata_labjack_diostate_checkbox.setText(_translate("Form", "LabJack DIO State"))
        self.data_configuration_metadata_grating_cbox.setText(_translate("Form", "Monochromator Grating"))
        self.data_configuration_metadata_lockints_cbox.setText(_translate("Form", "Lock-in Sample Time"))
        self.data_configuration_metadata_lockin_sensitivity_cbox.setText(_translate("Form", "Lock-in Sensitivity"))
        self.data_configuration_metadata_shutter_cbox.setText(_translate("Form", "Monochromator Shutter"))
        self.auto_data_metadata_lockinfs_cbox.setText(_translate("Form", "Lock-in Sample Frequency"))
        self.auto_data_metadata_wavelength_cbox.setText(_translate("Form", "Monochromator Wavelength"))
        self.auto_data_metadata_osf_cbox.setText(_translate("Form", "Monochromator Order Sort Filter"))
        self.auto_data_metadata_lockintimeconstant_cbox.setText(_translate("Form", "Lock-in Time Constant"))
        self.auto_data_exposure_duration_label.setText(_translate("Form", "Exposure Duration (s.):"))
        self.auto_data_storagepath_label.setText(_translate("Form", "Storage Path:"))
        self.auto_control_label.setText(_translate("Form", "Control:"))
        self.auto_control_runseries_button.setText(_translate("Form", "Run Series"))
        self.auto_control_pauseseries_button.setText(_translate("Form", "Pause Series"))
        self.auto_control_abortseries_button.setText(_translate("Form", "Abort Series"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

