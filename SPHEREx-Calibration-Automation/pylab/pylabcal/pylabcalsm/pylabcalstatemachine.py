import os
import sys
import pdb
import numpy as np
import datetime as datetime
from statemachine import State, StateMachine

#sys.path.append(r'..\pylab')
sys.path.append(r'..\..\..\..\pylablib')
sys.path.append(r'..\..\..')

from pylablib.utils.parameters import get_params_dict, write_config_file
from pylablib.instruments.powermaxusb import PowermaxUSB
from pylablib.instruments.serial_motor_dpy50601 import DPY50601

class SM(StateMachine):

	# Define States
	initializing = State('Initializing', initial=True)
	waiting = State('Waiting')
	thinking = State('Thinking')
	moving = State('Moving')
	measuring = State('Measuring')
	checking = State('Checking')
	compressing = State('Compressing')
	writing = State('Writing')
	resetting = State('Resetting')
	troubleshooting = State('Troubleshooting')

	# Define Transitions
	wait =

	def __init__(self, config_file='setup.ini'):
		print('Start by Initializing')

		#self.path = r"/pylab/pylabcal/config"
		#self.path = os.path.join('..','pylab','pylabcal','config')
		self.path = os.path.join('..', '..', 'config', 'sequence')

		if os.path.isfile(os.path.join(self.path,config_file)) == False:
			print('No config file by this name')
			print('Return some kind of error')
			pdb.set_trace()
		self.cfg_file_default = config_file
		self.message_box = []
		self.message_log = []
		self.overwrite_config_file = False
		self.config_box_checked = True

		#pdb.set_trace()
		# self.errorStatus = self.initialize()
		self.initialize()

		self.state = self.startState
		self.init_status = self.init
		self.data_in_queue = self.in_queue
		self.data_ready_to_store = self.ready_to_store
		self.errorStatus = self.error_status
		self.errorDict = {}
		self.metadata = {}
	# pdb.set_trace()


	def initialize(self):
		#print('Initialize each device, one at a time.  Each Returns Flag and Metadata, stored in a Dict')
		self.params = self.get_parameters_from_file(os.path.join(self.path, self.cfg_file_default))
		print(self.params)
		self.start()

		# Load Thorlabs Laser

		# Load Filter Wheels

		# Load Data Collection

		# Load Powermax
		#self.powermax = PowermaxUSB()
		# mn = self.params['powermax'] = wavelength_min
		# mx = self.params['powermax'] = wavelength_max
		# self.powermax.set_wavelength()

		# self.errorDict['powermax'] = self.powermax.error_record

		# Load Motor Controllers into Dict
		#self.stepper_motors = {}
		#for imotor in range(1):
		#	motor_name = 'motor_'+str(imotor)
		#	motor_name = 'xstage'
		#	self.stepper_motors[motor_name] = DPY50601(imotor)

		#self.stepper_motors['test'] = 3
		#pdb.set_trace()

		if np.sum(sum(self.errorDict.values())):
			# self.error_handler()
			self.errorStatus = True
			self.message_box.append(self.get_time_now() + 'Initialization unsuccessful')
			#self.message_box.append('Initialization unsuccessful')
		# return
		else:
			self.message_box.append(self.get_time_now() + 'Initialization successful')
			#self.message_box.append('Initialization successful')			self.init_status = True

		return 'waiting', 'Initialized without errors'  # errors

	def get_time_now(self):
		dateTimeObj = datetime.datetime.now()

		#return dateTimeObj.strftime("%d-%m-%Y (%H:%M:%S)") + " "
		return dateTimeObj.strftime("%H:%M:%S") + " "

	def get_parameters_from_file(self, config_path):

		#pdb.set_trace()
		params = get_params_dict(config_path)

		return params

	def get_parameters_from_gui(self):

		pdb.set_trace()
		errors = []
		warnings = []
		seq.name = self.ui.sequence_name_ledit.text()
		if seq.name == "":
			errors.append("Sequence Name left blank")
		# Grabbing value from cbox so no check needed yet.
		seq.grating = self.ui.grating_select_cbox_tab2.currentIndex() + 1
		# Grabbing value from cbox so no check needed yet.
		seq.osf = self.ui.osf_select_cbox.currentIndex() + 1

		try:
			seq.start_wave = float(self.ui.sequence_wave_start_ledit.text())
		except ValueError as e:
			errors.append("Invalid start wave arg: {}".format(e))
		# else: check input against valid wavelength range for grating and filters

		try:
			seq.end_wave = float(self.ui.sequence_wave_end_ledit.text())
		except ValueError as e:
			errors.append("Invalid end wave arg: {}".format(e))
		# else: check input against valid wavelength range for grating and filters

		try:
			seq.step_wave = float(self.ui.sequence_wave_step_ledit.text())
		except ValueError as e:
			errors.append("Invalid wave step arg: {}".format(e))
		# else: check input against grating step resolution

		try:
			seq.measure_interval = float(self.ui.sequence_measure_int_ledit.text())
		except ValueError as e:
			errors.append("Invalid measure interval arg: {}".format(e))
		else:
			if seq.measure_interval < 0.5:
				warnings.append("Small Measure Interval provided. Monochromator wavelength drive may not step as fast "
								"as the specified interval demands.")

		if len(errors) > 0:
			ret = -1
			self.show_invalid_seq_popup(errors)
		else:
			ret = 0

		return ret


	def write_parameters_to_file(self, config_path_out):
		#pdb.set_trace()
		configfilename = config_path_out.split('/')[-1].split('\\')[-1]
		if not os.path.isfile(config_path_out):
			write_config_file(self.params, config_path_out)
			self.message_box.append(configfilename + ' saved')
		elif self.overwrite_config_file == True:
			write_config_file(self.params, config_path_out)
			self.overwrite_config_file = False
			self.message_box.append(configfilename + ' overwritten')
		else:
			self.message_box.append(configfilename +' already exists')

	def update_parameters(self, config_file):
		config_path = os.path.join(self.path, config_file)
		if os.path.isfile(config_path):
			print(config_path)
			self.params = self.get_parameters_from_file(config_path)
		else:
			print(config_file+' file does not exist')
			return

	def error_handler(self):
		for key, value in self.errorDict.items():
			# pdb.set_trace()
			print(key, ':', value)
		# self.errorStatus = True

		self.errorStatus = False
		#self.message_box.append(self.get_time_now() + 'Errors Found. Be more specific!')
		self.message_box.append('Errors Found. Be more specific!')
		return 'waiting', 'Debug Errors'  # errors

	def collect_data(self):
		print('Collecting Data')

		# Clear Powermax DataFrame
		self.powermax.clear_data()

		# Collect Data

		# Record Errors
		errors = 0
		if np.sum(errors > 0):
			return
		else:
			self.data_in_queue = True

		self.message_box.append('Collected Data')
		return 'waiting', 'Data Collected'  # errors

	def compress_data(self):
		print('Compressing Data')
		errors = 0
		if np.sum(errors > 0):
			return
		else:
			self.data_ready_to_store = True

		self.message_box.append('Compressed Data as .??')
		return 'waiting', 'Data Compressed'  # errors

	def write_data_to_disk(self):
		print('Writing Data to Disk')
		errors = 0
		#pdb.set_trace()
		if np.sum(errors > 0):
			return
		else:
			self.data_ready_to_store = True

		self.message_box.append('Write Data to Disk')
		return 'waiting', 'Data Written to Disk'  # errors

	def generateOutput(self, state):
		if state == 'initializing':
			return self.initialize()
		elif state == 'collecting':
			return self.collect_data()
		elif state == 'compressing':
			return self.compress_data()
		elif state == 'storing':
			return self.write_data_to_disk()
		elif state == 'error':
			return self.error_handler()
		else:
			return 'wait'

	def getNextValues(self, state, dict_in):
		# pdb.set_trace()
		if self.errorStatus == True:
			nextState = 'error'
		elif state == 'waiting' and 'initialize' in dict_in:
			nextState = 'initializing'
		elif state == 'waiting' and self.init_status == True and 'collect' in dict_in:
			nextState = 'collecting'
		elif state == 'waiting' and self.data_in_queue == True and 'compress' in dict_in:
			nextState = 'compressing'
		elif state == 'waiting' and self.data_ready_to_store == True and 'write_to_disk' in dict_in:
			nextState = 'storing'
		else:
			nextState = 'error'
		self.message_box.append("STATE: "+ nextState)
		return (self.generateOutput(nextState))