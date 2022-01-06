import os

##### pyhkd settings #####

VERSION_STR = 'v0.5'
DATA_LOG_FOLDER = os.environ['SLT_DATA']
APP_LOG_BASE_FOLDER = os.path.join(os.environ['SLT_DATA'], 'log')
APP_LOG_FILENAME = 'pylab.log'
APP_LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'
RECV_PORT = 7945
PYLAB_PROCNAME = 'pylab'
SCHEMA_NAME = 'spectral_cal'
SCHEMA_USER = 'root'
SCHEMA_PSWD = '$PHEREx_B111'
#COMMON_CODE_DIR = os.path.abspath(os.path.join(__file__,'..','..','..','common'))

# Make sure the folders exists
for f in [DATA_LOG_FOLDER, APP_LOG_BASE_FOLDER]:
	try: 
		os.makedirs(f)
	except OSError:
		if not os.path.isdir(f):
			raise
