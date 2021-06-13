import sys
import os
import asyncio
from qasync import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from scanWindowDialog5 import Ui_Dialog as masterDialog
from popupDialog import PopupDialog as popupDialog

# add package root directory to search path
sys.path.append("..\\..\\..\\")
from pylabcal.pylabcalsm.pylabcal_sm import SpectralCalibrationMachine, ControlLoopParams
from pylablib.utils.parameters import write_config_file, get_params_dict

SEQUENCE_ROLE = 1


class masterWindow(QtWidgets.QDialog):
    """
    Spectral calibration master control GUI window
    """

    def __init__(self, root_path, seq_config_path="\\pylabcal\\config\\sequence\\"):
        super().__init__()

        ##Configuration paths##############################################
        self.root_path = root_path
        self.seq_config_path = root_path + seq_config_path
        ########################################################################

        ##Sequence files and variables###########################################################
        self.saved_sequence_config_files = []
        for seq_file in os.listdir(self.seq_config_path):
            if seq_file.endswith(".ini"):
                self.saved_sequence_config_files.append(seq_file)
        #########################################################################################

        ##Series files and variables#############################################################
        self.saved_series_config_files = []
        self.active_series = []
        #########################################################################################

        ##State Machine###################################
        self.state_machine = SpectralCalibrationMachine()
        self.control_loop_params = ControlLoopParams()
        ##################################################

        ##Set up GUI windows############################################################
        self.ui = masterDialog()
        self.ui.setupUi(self)
        self.popup = popupDialog()
        ###################################################################################

        # Automation Tab Buttons##########################################################################
        self.ui.autotab_savesequence_button.clicked.connect(self.save_sequence_to_file)
        self.ui.autotab_savedsequences_list.currentItemChanged.connect(self.update_highlighted_sequence)
        self.ui.autotab_addsequencetoseries_button.clicked.connect(self.add_sequence_to_series)
        self.ui.autotab_removesequence_button.clicked.connect(self.remove_sequence_from_series)
        self.ui.autotab_removeallsequences_button.clicked.connect(self.remove_all_sequences_from_series)
        self.ui.autotab_runseries_button.clicked.connect(self.run_series)
        ###################################################################################################

        # Monochromator Tab Buttons###################################################
        self.ui.monochromator_manualcontrol_setparameters_button.clicked.connect(
            self.set_monochromator_parameters_manual)

        # Populate displays with default values#######################################
        self.update_auto_display()

        # If initialization was successful, then move on to Waiting state
        state_status = self.state_machine.get_state_status()
        if state_status == SpectralCalibrationMachine.STATE_COMPLETE_SUCCESS:
            self.state_machine.next_state()

    # AUTOMATION TAB METHODS######################################################################################
    def run_series(self):
        if len(self.active_series):
            #Build list of ControlLoopParams instances to pass to state machine
            control_loop_params_list = [0 for seq in self.active_series]
            ind = 0
            for seq_file in self.active_series:
                control_loop_params = ControlLoopParams()
                control_loop_params.__dict__ = get_params_dict(self.seq_config_path + seq_file)
                control_loop_params_list[ind] = control_loop_params
                ind += 1
            self.state_machine.next_state(next_state_data=control_loop_params_list)
        else:
            self.popup.disp_msg(["No sequences found in series!"])
            self.popup.popup()

    def add_sequence_to_series(self):
        cur_item = self.ui.autotab_savedsequences_list.currentItem()
        if cur_item is not None:
            self.active_series.append(cur_item.text())
        else:
            self.popup.disp_msg(["No sequence selected!"])
            self.popup.popup()

        self.update_auto_display()

    def remove_sequence_from_series(self):
        rem_seq = self.ui.autotab_series_list.currentItem()
        if rem_seq is not None:
            self.active_series.remove(rem_seq.text())
            print(self.active_series)
            self.ui.autotab_series_list.takeItem(self.ui.autotab_series_list.currentRow())

    def remove_all_sequences_from_series(self):
        self.ui.autotab_series_list.clear()
        self.active_series = []

    def update_highlighted_sequence(self):
        self.load_sequence_from_file()
        self.update_auto_display()
        self.update_monochromator_display()

    def load_sequence_from_file(self, filename=None):

        if filename is None:
            config_file = self.ui.autotab_savedsequences_list.currentItem().data(SEQUENCE_ROLE)
        else:
            config_file = filename

        self.control_loop_params.__dict__ = get_params_dict(config_file)

    def save_sequence_to_file(self):
        # First build control loop params for sequence#################################################################
        #monochromator parameters
        self.control_loop_params.data['storage_path'] = self.ui.autotab_storagepath_ledit.text()
        self.control_loop_params.data['format'] = self.ui.autotab_storageformat_combobox.currentText()
        self.control_loop_params.metadata['cryo_temp'] = self.ui.autotab_metadata_cryo_checkbox.isChecked()
        self.control_loop_params.metadata['power_meter'] = self.ui.autotab_metadata_powermeter_checkbox.isChecked()
        self.control_loop_params.metadata['ndf_wheel'] = self.ui.autotab_metadata_ndf_checkbox.isChecked()
        self.control_loop_params.metadata['grating'] = self.ui.autotab_metadata_grating_checkbox.isChecked()
        self.control_loop_params.metadata['wavelength'] = self.ui.autotab_metadata_wavelength_checkbox.isChecked()
        self.control_loop_params.monochromator['start_wavelength'] = float(self.ui.
                                                                           monochromator_sequencecontrol_startwave_ledit
                                                                           .text())
        self.control_loop_params.monochromator['stop_wavelength'] = float(self.ui.
                                                                          monochromator_sequencecontrol_endwave_ledit
                                                                          .text())
        self.control_loop_params.monochromator['step_size'] = float(self.ui.monochromator_sequencecontrol_step_ledit
                                                                    .text()) * 1e-3
        self.control_loop_params.monochromator['shutter'] = "Open"
        self.control_loop_params.monochromator['g1_g2_transition'] = float(self.ui.monochromator_sequencecontrol_g1g2transition_ledit.text())
        self.control_loop_params.monochromator['g2_g3_transition'] = float(self.ui.monochromator_sequencecontrol_g2g3transition_ledit.text())
        self.control_loop_params.monochromator['noosf_osf1_transition'] = float(self.ui.monochromator_sequencecontrol_noosfosf1transition_ledit.text())
        self.control_loop_params.monochromator['osf1_osf2_transition'] = float(self.ui.monochromator_sequencecontrol_osf1osf2transition_ledit.text())
        self.control_loop_params.monochromator['osf2_osf3_transition'] = float(self.ui.monochromator_sequencecontrol_osf2osf3transition_ledit.text())
        #lockin parameters
        self.control_loop_params.lockin['sample_frequency'] = float(self.ui.lockin_samplefrequency_ledit.text())
        self.control_loop_params.lockin['sample_time'] = float(self.ui.lockin_sampletime_ledit.text())
        self.control_loop_params.lockin['time_constant'] = float(self.ui.lockin_timeconstant_ledit.text())
        sensitivities = self.ui.lockin_sensitivitystring_ledit.text().split(',')
        self.control_loop_params.lockin['sensitivities'] = [float(s) for s in sensitivities]
        ###############################################################################################################
        filename = self.ui.autotab_sequencename_ledit.text() + '.ini'
        config_path_out = os.path.join('..', '..', 'config', 'sequence', filename)
        if not os.path.isfile(config_path_out):
            write_config_file(self.control_loop_params.__dict__, config_path_out)
            self.saved_sequence_config_files.append(filename)
        else:
            self.popup.disp_msg(["Sequence file {} already exists!".format(filename + '.ini')])
            self.popup.popup()

        ##Update display after saving item
        self.update_auto_display()

    def update_auto_display(self, initial=False):
        self.ui.autotab_storagepath_ledit.setText(str(self.control_loop_params.data['storage_path']))
        self.ui.autotab_storageformat_combobox.setCurrentText(str(self.control_loop_params.data['format']))

        for seq_file in self.saved_sequence_config_files:
            if len(self.ui.autotab_savedsequences_list.findItems(seq_file, QtCore.Qt.MatchExactly)) == 0:
                seq_item = QtWidgets.QListWidgetItem()
                seq_item.setText(seq_file)
                seq_item.setData(SEQUENCE_ROLE, self.seq_config_path + seq_file)
                self.ui.autotab_savedsequences_list.addItem(seq_item)

        for seq_file in self.active_series:
            if len(self.ui.autotab_series_list.findItems(seq_file, QtCore.Qt.MatchExactly)) == 0:
                seq_item = QtWidgets.QListWidgetItem()
                seq_item.setText(seq_file)
                seq_item.setData(SEQUENCE_ROLE, self.seq_config_path + seq_file)
                self.ui.autotab_series_list.addItem(seq_item)

    # MONOCHROMATOR TAB METHODS########################################################################################
    def update_monochromator_display(self):
        self.ui.monochromator_sequencecontrol_startwave_ledit.setText(
            self.control_loop_params.monochromator['start_wavelength'])

        self.ui.monochromator_sequencecontrol_endwave_ledit.setText(
            self.control_loop_params.monochromator['stop_wavelength']
        )

        self.ui.monochromator_sequencecontrol_step_ledit.setText(
            str(float(self.control_loop_params.monochromator['step_size'])*1e3)
        )

        self.ui.monochromator_sequencecontrol_g1g2transition_ledit.setText(
            self.control_loop_params.monochromator['g1_g2_transition'])

        self.ui.monochromator_sequencecontrol_g2g3transition_ledit.setText(
            self.control_loop_params.monochromator['g2_g3_transition']
        )

        self.ui.monochromator_sequencecontrol_noosfosf1transition_ledit.setText(
            self.control_loop_params.monochromator['noosf_osf1_transition']
        )

        self.ui.monochromator_sequencecontrol_osf1osf2transition_ledit.setText(
            self.control_loop_params.monochromator['osf1_osf2_transition']
        )

        self.ui.monochromator_sequencecontrol_osf2osf3transition_ledit.setText(
            self.control_loop_params.monochromator['osf2_osf3_transition']
        )

    def set_monochromator_parameters_manual(self):
        cur_state = self.state_machine.get_state()
        if cur_state == 'Waiting':
            # Reset control loop parameters
            self.control_loop_params.reset()

            # Set monochromator params#################################################
            grating = self.ui.monochromator_manualcontrol_grating_combobox.currentIndex() + 1
            self.control_loop_params.monochromator['grating'] = [grating]
            wavelength = float(self.ui.monochromator_manualcontrol_wavelength_ledit.text())
            self.control_loop_params.monochromator['start-wavelength'] = [wavelength]
            self.control_loop_params.monochromator['stop-wavelength'] = [wavelength]
            self.control_loop_params.monochromator['step-size'] = [0]
            self.control_loop_params.monochromator['shutter'] = self.ui.monochromator_manualcontrol_shutter_combobox. \
                currentText()

            ##Since this function should only change Monochromator, leave all other parameters in reset state

            # Enter next state, pass in new control loop parameters
            self.state_machine.next_state(next_state_data=self.control_loop_params)
        else:
            print("Cannot enter Thinking from {}".format(cur_state))

    ####################################################################################################################

    def start_scan_series(self):
        cur_state = self.state_machine.get_state()
        if cur_state == 'Waiting':
            self.state_machine.next_state()
        else:
            print("Cannot enter Thinking from {}".format(cur_state))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    rootpath = "C:\\Users\\thoma\\Studies\\SPHEREx\\SW-Dev\\SPHEREx-lab-tools\\SPHEREx-Calibration-Automation\\pylab"
    window = masterWindow(rootpath)  # cs)
    window.show()
    with loop:
        loop.run_forever()
        loop.close()
    sys.exit(app.exec_())
