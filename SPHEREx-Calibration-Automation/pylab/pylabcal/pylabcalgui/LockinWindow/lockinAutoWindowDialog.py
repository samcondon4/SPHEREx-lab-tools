# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lockinAutoWindowDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1969, 1606)
        self.main_layout = QtWidgets.QGridLayout(Form)
        self.main_layout.setObjectName("main_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_layout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_layout.addItem(spacerItem1, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 1)
        self.list_listXlist_Sr510SensTransitionsXSavedSequences_listXPassiveListAll_Sr510SensitivityTransitions = QtWidgets.QListWidget(self.tab)
        self.list_listXlist_Sr510SensTransitionsXSavedSequences_listXPassiveListAll_Sr510SensitivityTransitions.setObjectName("list_listXlist_Sr510SensTransitionsXSavedSequences_listXPassiveListAll_Sr510SensitivityTransitions")
        self.gridLayout_2.addWidget(self.list_listXlist_Sr510SensTransitionsXSavedSequences_listXPassiveListAll_Sr510SensitivityTransitions, 6, 0, 1, 2)
        self.button_list_Sr510SensTransitions_remover_RemoveSr510SensTransition = QtWidgets.QPushButton(self.tab)
        self.button_list_Sr510SensTransitions_remover_RemoveSr510SensTransition.setObjectName("button_list_Sr510SensTransitions_remover_RemoveSr510SensTransition")
        self.gridLayout_2.addWidget(self.button_list_Sr510SensTransitions_remover_RemoveSr510SensTransition, 12, 0, 1, 2)
        self.button_list_Sr510SensTransitions_RemoverOfAll_RemoveAllSr510SensTransitions = QtWidgets.QPushButton(self.tab)
        self.button_list_Sr510SensTransitions_RemoverOfAll_RemoveAllSr510SensTransitions.setObjectName("button_list_Sr510SensTransitions_RemoverOfAll_RemoveAllSr510SensTransitions")
        self.gridLayout_2.addWidget(self.button_list_Sr510SensTransitions_RemoverOfAll_RemoveAllSr510SensTransitions, 13, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 8, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 7, 0, 1, 1)
        self.button_list_Sr510SensTransitions_setter_AddSr510SensTransition = QtWidgets.QPushButton(self.tab)
        self.button_list_Sr510SensTransitions_setter_AddSr510SensTransition.setObjectName("button_list_Sr510SensTransitions_setter_AddSr510SensTransition")
        self.gridLayout_2.addWidget(self.button_list_Sr510SensTransitions_setter_AddSr510SensTransition, 11, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 9, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 4, 0, 1, 1)
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits = QtWidgets.QComboBox(self.tab)
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.setObjectName("combobox_list_SavedSequences_passive_Sr510TimeConstantUnits")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.addItem("")
        self.gridLayout_2.addWidget(self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits, 4, 1, 1, 1)
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits = QtWidgets.QComboBox(self.tab)
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.setObjectName("combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.addItem("")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.addItem("")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.addItem("")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.addItem("")
        self.gridLayout_2.addWidget(self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits, 10, 1, 1, 1)
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier = QtWidgets.QComboBox(self.tab)
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier.setObjectName("combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier.addItem("")
        self.gridLayout_2.addWidget(self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier, 3, 1, 1, 1)
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier = QtWidgets.QComboBox(self.tab)
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier.setObjectName("combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier.addItem("")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier.addItem("")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier.addItem("")
        self.gridLayout_2.addWidget(self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier, 9, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantValue = QtWidgets.QComboBox(self.tab)
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantValue.setObjectName("combobox_list_SavedSequences_passive_Sr510TimeConstantValue")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantValue.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantValue.addItem("")
        self.gridLayout_2.addWidget(self.combobox_list_SavedSequences_passive_Sr510TimeConstantValue, 2, 1, 1, 1)
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue = QtWidgets.QComboBox(self.tab)
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue.setObjectName("combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue.addItem("")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue.addItem("")
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue.addItem("")
        self.gridLayout_2.addWidget(self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue, 8, 1, 1, 1)
        self.lineedit_list_Sr510SensTransitions_ItemDisplay_wavelength = QtWidgets.QLineEdit(self.tab)
        self.lineedit_list_Sr510SensTransitions_ItemDisplay_wavelength.setObjectName("lineedit_list_Sr510SensTransitions_ItemDisplay_wavelength")
        self.gridLayout_2.addWidget(self.lineedit_list_Sr510SensTransitions_ItemDisplay_wavelength, 7, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency = QtWidgets.QComboBox(self.tab)
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setObjectName("combobox_list_SavedSequences_passive_Sr510SampleFrequency")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.addItem("")
        self.gridLayout_2.addWidget(self.combobox_list_SavedSequences_passive_Sr510SampleFrequency, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 10, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 0, 1, 1)
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency = QtWidgets.QComboBox(self.tab_2)
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setObjectName("combobox_list_SavedSequences_passive_Sr830SampleFrequency")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.addItem("")
        self.gridLayout.addWidget(self.combobox_list_SavedSequences_passive_Sr830SampleFrequency, 1, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.tab_2)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 2, 0, 1, 1)
        self.button_list_Sr830SensTransitions_RemoverOfAll_RemoveAllSr830SensTransitions = QtWidgets.QPushButton(self.tab_2)
        self.button_list_Sr830SensTransitions_RemoverOfAll_RemoveAllSr830SensTransitions.setObjectName("button_list_Sr830SensTransitions_RemoverOfAll_RemoveAllSr830SensTransitions")
        self.gridLayout.addWidget(self.button_list_Sr830SensTransitions_RemoverOfAll_RemoveAllSr830SensTransitions, 13, 0, 1, 2)
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 5, 0, 1, 1)
        self.list_listXlist_Sr830SensTransitionsXSavedSequences_listXPassiveListAll_Sr830SensitivityTransitions = QtWidgets.QListWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_listXlist_Sr830SensTransitionsXSavedSequences_listXPassiveListAll_Sr830SensitivityTransitions.sizePolicy().hasHeightForWidth())
        self.list_listXlist_Sr830SensTransitionsXSavedSequences_listXPassiveListAll_Sr830SensitivityTransitions.setSizePolicy(sizePolicy)
        self.list_listXlist_Sr830SensTransitionsXSavedSequences_listXPassiveListAll_Sr830SensitivityTransitions.setObjectName("list_listXlist_Sr830SensTransitionsXSavedSequences_listXPassiveListAll_Sr830SensitivityTransitions")
        self.gridLayout.addWidget(self.list_listXlist_Sr830SensTransitionsXSavedSequences_listXPassiveListAll_Sr830SensitivityTransitions, 6, 0, 1, 2)
        self.button_list_Sr830SensTransitions_setter_AddSr830SensTransition = QtWidgets.QPushButton(self.tab_2)
        self.button_list_Sr830SensTransitions_setter_AddSr830SensTransition.setObjectName("button_list_Sr830SensTransitions_setter_AddSr830SensTransition")
        self.gridLayout.addWidget(self.button_list_Sr830SensTransitions_setter_AddSr830SensTransition, 11, 0, 1, 2)
        self.label_20 = QtWidgets.QLabel(self.tab_2)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 7, 0, 1, 1)
        self.button_list_Sr830SensTransitions_remover_RemoveSr830SensTransition = QtWidgets.QPushButton(self.tab_2)
        self.button_list_Sr830SensTransitions_remover_RemoveSr830SensTransition.setObjectName("button_list_Sr830SensTransitions_remover_RemoveSr830SensTransition")
        self.gridLayout.addWidget(self.button_list_Sr830SensTransitions_remover_RemoveSr830SensTransition, 12, 0, 1, 2)
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits = QtWidgets.QComboBox(self.tab_2)
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.setObjectName("lineedit_list_Sr830SensTransitions_passive_SensitivityUnits")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.addItem("")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.addItem("")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.addItem("")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.addItem("")
        self.gridLayout.addWidget(self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits, 10, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 3, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 9, 0, 1, 1)
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue = QtWidgets.QComboBox(self.tab_2)
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue.setObjectName("lineedit_list_Sr830SensTransitions_passive_SensitivityValue")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue.addItem("")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue.addItem("")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue.addItem("")
        self.gridLayout.addWidget(self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue, 8, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 10, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.tab_2)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 8, 0, 1, 1)
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier = QtWidgets.QComboBox(self.tab_2)
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier.setObjectName("lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier.addItem("")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier.addItem("")
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier.addItem("")
        self.gridLayout.addWidget(self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier, 9, 1, 1, 1)
        self.lineedit_list_Sr830SensTransitions_ItemDisplay_wavelength = QtWidgets.QLineEdit(self.tab_2)
        self.lineedit_list_Sr830SensTransitions_ItemDisplay_wavelength.setObjectName("lineedit_list_Sr830SensTransitions_ItemDisplay_wavelength")
        self.gridLayout.addWidget(self.lineedit_list_Sr830SensTransitions_ItemDisplay_wavelength, 7, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.tab_2)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 4, 0, 1, 1)
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantValue = QtWidgets.QComboBox(self.tab_2)
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantValue.setObjectName("combobox_list_SavedSequences_passive_Sr830TimeConstantValue")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantValue.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantValue.addItem("")
        self.gridLayout.addWidget(self.combobox_list_SavedSequences_passive_Sr830TimeConstantValue, 2, 1, 1, 1)
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier = QtWidgets.QComboBox(self.tab_2)
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier.setObjectName("combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier.addItem("")
        self.gridLayout.addWidget(self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier, 3, 1, 1, 1)
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits = QtWidgets.QComboBox(self.tab_2)
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.setObjectName("combobox_list_SavedSequences_passive_Sr830TimeConstantUnits")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.addItem("")
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.addItem("")
        self.gridLayout.addWidget(self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits, 4, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.main_layout.addWidget(self.tabWidget, 1, 0, 1, 2)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Lockin Amplifier(s)"))
        self.label_6.setText(_translate("Form", "SR510 Sensitivity Transitions in Sequence:"))
        self.button_list_Sr510SensTransitions_remover_RemoveSr510SensTransition.setText(_translate("Form", "Remove SR510 Sensitivity Transition from Sequence"))
        self.button_list_Sr510SensTransitions_RemoverOfAll_RemoveAllSr510SensTransitions.setText(_translate("Form", "Remove All SR510 Transitions from Sequence"))
        self.label.setText(_translate("Form", "SR510 Lock-In Sequence Control:"))
        self.label_5.setText(_translate("Form", "Sensitivity Value:"))
        self.label_10.setText(_translate("Form", "Wavelength:"))
        self.button_list_Sr510SensTransitions_setter_AddSr510SensTransition.setText(_translate("Form", "Add SR510 Sensitivity Transition to Sequence"))
        self.label_3.setText(_translate("Form", "Sensitivity Multiplier:"))
        self.label_8.setText(_translate("Form", "Time Constant Units:"))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.setCurrentText(_translate("Form", "ks."))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.setItemText(0, _translate("Form", "ks."))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.setItemText(1, _translate("Form", "s."))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.setItemText(2, _translate("Form", "ms."))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantUnits.setItemText(3, _translate("Form", "us."))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.setCurrentText(_translate("Form", "V."))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.setItemText(0, _translate("Form", "V."))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.setItemText(1, _translate("Form", "mV."))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.setItemText(2, _translate("Form", "uV."))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityUnits.setItemText(3, _translate("Form", "nV."))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier.setItemText(0, _translate("Form", "x1"))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier.setItemText(1, _translate("Form", "x10"))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantMultiplier.setItemText(2, _translate("Form", "x100"))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier.setCurrentText(_translate("Form", "x1"))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier.setItemText(0, _translate("Form", "x1"))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier.setItemText(1, _translate("Form", "x10"))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityMultiplier.setItemText(2, _translate("Form", "x100"))
        self.label_7.setText(_translate("Form", "Time Constant Multiplier:"))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantValue.setItemText(0, _translate("Form", "1"))
        self.combobox_list_SavedSequences_passive_Sr510TimeConstantValue.setItemText(1, _translate("Form", "3"))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue.setCurrentText(_translate("Form", "1"))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue.setItemText(0, _translate("Form", "1"))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue.setItemText(1, _translate("Form", "2"))
        self.combobox_list_Sr510SensTransitions_passive_Sr510SensitivityValue.setItemText(2, _translate("Form", "5"))
        self.label_2.setText(_translate("Form", "Sample Frequency (Hz.):"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setCurrentText(_translate("Form", "0.0625"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(0, _translate("Form", "0.0625"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(1, _translate("Form", "0.125"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(2, _translate("Form", "0.250"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(3, _translate("Form", "0.5"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(4, _translate("Form", "1"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(5, _translate("Form", "2"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(6, _translate("Form", "4"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(7, _translate("Form", "8"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(8, _translate("Form", "16"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(9, _translate("Form", "32"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(10, _translate("Form", "64"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(11, _translate("Form", "128"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(12, _translate("Form", "256"))
        self.combobox_list_SavedSequences_passive_Sr510SampleFrequency.setItemText(13, _translate("Form", "512"))
        self.label_9.setText(_translate("Form", "Time Constant Value:"))
        self.label_4.setText(_translate("Form", "Sensitivity Units:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "SR510"))
        self.label_11.setText(_translate("Form", "SR830 Lock-In Sequence Control:"))
        self.label_12.setText(_translate("Form", "Sample Frequency (Hz.):"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setCurrentText(_translate("Form", "0.0625"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(0, _translate("Form", "0.0625"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(1, _translate("Form", "0.125"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(2, _translate("Form", "0.250"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(3, _translate("Form", "0.5"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(4, _translate("Form", "1"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(5, _translate("Form", "2"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(6, _translate("Form", "4"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(7, _translate("Form", "8"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(8, _translate("Form", "16"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(9, _translate("Form", "32"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(10, _translate("Form", "64"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(11, _translate("Form", "128"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(12, _translate("Form", "256"))
        self.combobox_list_SavedSequences_passive_Sr830SampleFrequency.setItemText(13, _translate("Form", "512"))
        self.label_19.setText(_translate("Form", "Time Constant Value:"))
        self.button_list_Sr830SensTransitions_RemoverOfAll_RemoveAllSr830SensTransitions.setText(_translate("Form", "Remove All SR830 Transitions from Sequence"))
        self.label_16.setText(_translate("Form", "SR830 Sensitivity Transitions in Sequence:"))
        self.button_list_Sr830SensTransitions_setter_AddSr830SensTransition.setText(_translate("Form", "Add SR830 Sensitivity Transition to Sequence"))
        self.label_20.setText(_translate("Form", "Wavelength:"))
        self.button_list_Sr830SensTransitions_remover_RemoveSr830SensTransition.setText(_translate("Form", "Remove SR830 Sensitivity Transitions from Sequence"))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.setItemText(0, _translate("Form", "V."))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.setItemText(1, _translate("Form", "mV."))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.setItemText(2, _translate("Form", "uV."))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityUnits.setItemText(3, _translate("Form", "nV."))
        self.label_17.setText(_translate("Form", "Time Constant Multiplier:"))
        self.label_13.setText(_translate("Form", "Sensitivity Multiplier:"))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue.setItemText(0, _translate("Form", "1"))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue.setItemText(1, _translate("Form", "2"))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityValue.setItemText(2, _translate("Form", "5"))
        self.label_14.setText(_translate("Form", "Sensitivity Units:"))
        self.label_15.setText(_translate("Form", "Sensitivity Value:"))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier.setItemText(0, _translate("Form", "x1"))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier.setItemText(1, _translate("Form", "x10"))
        self.lineedit_list_Sr830SensTransitions_passive_SensitivityMultiplier.setItemText(2, _translate("Form", "x100"))
        self.label_18.setText(_translate("Form", "Time Constant Units:"))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantValue.setItemText(0, _translate("Form", "1"))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantValue.setItemText(1, _translate("Form", "3"))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier.setItemText(0, _translate("Form", "x1"))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier.setItemText(1, _translate("Form", "x10"))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantMultiplier.setItemText(2, _translate("Form", "x100"))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.setCurrentText(_translate("Form", "ks."))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.setItemText(0, _translate("Form", "ks."))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.setItemText(1, _translate("Form", "s."))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.setItemText(2, _translate("Form", "ms."))
        self.combobox_list_SavedSequences_passive_Sr830TimeConstantUnits.setItemText(3, _translate("Form", "us."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "SR830"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

