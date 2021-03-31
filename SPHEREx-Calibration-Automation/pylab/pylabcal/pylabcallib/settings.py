from __future__ import division, print_function

import os

##### pylabcald settings #####

VERSION_STR = 'v2.0'
DATA_LOG_FOLDER = '/data/hk'
APP_LOG_BASE_FOLDER = '/var/log/pylabcal'
APP_LOG_FILENAME = 'pylabcald.log'
APP_LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'
RECV_PORT = 7945
PYLABCALD_PROCNAME = 'pylabcald'
INSTRUMENT_CONFIG_FOLDER = './config'
COMMON_CODE_DIR = os.path.abspath(os.path.join(__file__, '../pylabcald', '..', '..', 'common'))

# Make sure the folders exists
for f in [DATA_LOG_FOLDER, APP_LOG_BASE_FOLDER]:
	try:
		os.makedirs(f)
	except OSError:
		if not os.path.isdir(f):
			raise
