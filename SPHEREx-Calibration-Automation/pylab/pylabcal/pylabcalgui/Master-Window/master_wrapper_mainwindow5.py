import sys
import os
import pdb
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

    def __init__(self, root_path, seq_config_path="\\pylabcal\\config\\sequence\\", default_seq_file='default_seq.ini'):
        super().__init__()

        ##Save configuration paths##############################################
        self.root_path = root_path
        self.seq_config_path = root_path + seq_config_path
        self.default_seq_file = self.seq_config_path + default_seq_file

        ##Saved sequence files###################################################
        self.saved_sequence_config_files = []
        for seq_file in os.listdir(self.seq_config_path):
            if seq_file.endswith(".ini"):
                self.saved_sequence_config_files.append(self.seq_config_path + seq_file)

        ##State Machine###################################
        self.state_machine = SpectralCalibrationMachine()
        self.control_loop_params = ControlLoopParams()
        ##################################################

        ##Set up GUI windows############################################################
        self.ui = masterDialog()
        self.ui.setupUi(self)
        self.popup = popupDialog()
        ###################################################################################

        # Automation Tab Buttons######################################################
        self.ui.autotab_savesequence_button.clicked.connect(self.save_sequence_to_file)

        # Monochromator Tab Buttons###################################################
        self.ui.monochromator_manualcontrol_setparameters_button.clicked.connect(
            self.set_monochromator_parameters_manual)

        # Populate displays with default values
        self.load_sequence_from_file(self.default_seq_file)

        # If initialization was successful, then move on to Waiting state
        state_status = self.state_machine.get_state_status()
        if state_status == SpectralCalibrationMachine.STATE_COMPLETE_SUCCESS:
            self.state_machine.next_state()

    # AUTOMATION TAB METHODS######################################################################################
    def load_sequence_from_file(self, filename=None):

        if filename is None:
            config_file = self.ui.autotab_savedsequences_list.currentItem()
        else:
            config_file = filename

        self.control_loop_params.__dict__ = get_params_dict(config_file)
        self.update_auto_display()

    def update_auto_display(self):
        self.ui.autotab_integrationtime_ledit.setText(str(self.control_loop_params.data['integration_time']))
        self.ui.autotab_storagepath_ledit.setText(str(self.control_loop_params.data['storage_path']))
        self.ui.autotab_storageformat_combobox.setCurrentText(str(self.control_loop_params.data['format']))
        self.ui.autotab_savedsequences_list.clear()
        for seq_file in self.saved_sequence_config_files:
            seq_file_name = seq_file.split('\\')[-1]
            seq_item = QtWidgets.QListWidgetItem()
            seq_item.setText(seq_file_name)
            seq_item.setData(SEQUENCE_ROLE, seq_file)
            self.ui.autotab_savedsequences_list.addItem(seq_item)

    def save_sequence_to_file(self):
        # First build control loop params for sequence#################################################################
        self.control_loop_params.data['integration_time'] = float(self.ui.autotab_integrationtime_ledit.text())
        self.control_loop_params.data['storage_path'] = self.ui.autotab_storagepath_ledit.text()
        self.control_loop_params.data['format'] = self.ui.autotab_storageformat_combobox.currentText()
        self.control_loop_params.metadata['cryo_temp'] = self.ui.autotab_metadata_cryo_checkbox.isChecked()
        self.control_loop_params.metadata['power_meter'] = self.ui.autotab_metadata_powermeter_checkbox.isChecked()
        self.control_loop_params.metadata['ndf_wheel'] = self.ui.autotab_metadata_grating_checkbox.isChecked()
        self.control_loop_params.metadata['wavelength'] = self.ui.autotab_metadata_wavelength_checkbox.isChecked()
        self.control_loop_params.monochromator['start_wavelength'] = float(self.ui.
                                                                           monochromator_sequencecontrol_startwave_ledit
                                                                           .text())
        self.control_loop_params.monochromator['stop_wavelength'] = float(self.ui.
                                                                          monochromator_sequencecontrol_endwave_ledit
                                                                          .text())
        self.control_loop_params.monochromator['step_size'] = float(self.ui.monochromator_sequencecontrol_step_ledit
                                                                    .text())
        self.control_loop_params.monochromator['grating'] = self.ui.monochromator_sequencecontrol_grating_combobox. \
                                                            currentIndex() + 1
        self.control_loop_params.monochromator['shutter'] = "Open"

        filename = self.ui.autotab_sequencename_ledit.text()
        config_path_out = os.path.join('..', '..', 'config', 'sequence', filename + '.ini')
        if not os.path.isfile(config_path_out):
            write_config_file(self.control_loop_params.__dict__, config_path_out)
            seq_item = QtWidgets.QListWidgetItem()
            seq_item.setText(filename)
            seq_item.setData(SEQUENCE_ROLE, config_path_out)
            self.ui.autotab_savedsequences_list.addItem(seq_item)
        else:
            self.popup.disp_msg(["Sequence file {} already exists!".format(filename + '.ini')])
            self.popup.popup()

    # MONOCHROMATOR TAB METHODS########################################################################################
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
