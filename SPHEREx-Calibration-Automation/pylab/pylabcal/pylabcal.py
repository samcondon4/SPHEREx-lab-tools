#!/usr/bin/env python

'''
This script starts the spectral calibration code, pylabcald.
'''

import sys

from pylab.pylabcal.pylabcallib.settings import *
sys.path.append(COMMON_CODE_DIR)

#from pylabcallib.data_acq.data_acq import DataAcq
#from pylabcallib.instruments.instrument_loader import load_instruments

from pylab.pylabcal.pylabcallib.instruments import DPY50601

if __name__ == '__main__':

	print('just the start')
	#print(dir(load_instruments))

	# Initialize the instrument suite, including:
	# - Power Meter
	# - Monochrometer
	# - Motor 1
	xstage1 = DPY50601(0)

	# - Motor 2
	xstage2 = DPY50601(1)

	DPY50601.total_motors_in_chain()

	# ----------
	# Start GUI?

	# Configure logging

	# Initialize data acquisition process

