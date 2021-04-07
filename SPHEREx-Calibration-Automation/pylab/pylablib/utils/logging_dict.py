'''
Wraps a given dictionary and logs all changes
'''

#from __future__ import division, print_function

import logging
import time

from value_logger import ValueLogger
from pylabcaldlib.settings import DATA_LOG_FOLDER

class LoggingDict(dict):
	
	def __init__(self, subfolder_name):
		
		dict.__init__(self)
		self.subfolder_name = subfolder_name
		self._loggers = {}
		
	def __setitem__(self, key, item):
		
		dict.__setitem__(self, key, item)
		
		if key not in self._loggers:
			self._loggers[key] = ValueLogger(DATA_LOG_FOLDER, self.subfolder_name, key)
		
		self._loggers[key].log(item, time.time())
