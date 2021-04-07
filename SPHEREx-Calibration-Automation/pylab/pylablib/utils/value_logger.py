'''
Logs values in a date-based folder structure
'''

#from __future__ import division, print_function

import time
import urllib
import datetime
import os
import logging

class ValueLogger():

	# base_folder_location: location of the date-sorted log structure
	# subfolder_name: name of the value type (used for folder names)
	def __init__(self, base_folder_location, subfolder_name, value_name):
		
		self._base_folder_location = base_folder_location
		self._fileobj = None
		
		# Escape special chars
		self._subfolder_name = urllib.quote(str(subfolder_name))
		self._value_name = urllib.quote(str(value_name))
		
		self._open_current_file()
	
	def __del__(self):
					
		if self._fileobj is not None:
			self._fileobj.close()
			
	def _open_current_file(self):
		
		d = datetime.date.today()
		self._last_filename_update = d
		
		self._filedir = os.path.join(self._base_folder_location, 
									 "%04d" % d.year,
									 "%02d" % d.month,
									 "%02d" % d.day,
									 self._subfolder_name)
		
		if not os.path.exists(self._filedir):
			os.makedirs(self._filedir)
		
		self._filename = os.path.join(self._filedir,
									  self._value_name + ".txt")
									 
		if self._fileobj is not None:
			self._fileobj.close()
			
		self._fileobj = open(self._filename, 'a', buffering=0)
		logging.info("Opening log file: " + self._filename)
	
	# update_time should be a value returned by time.time()
	def log(self, value, update_time):

		# Make sure we don't need to open a new file
		if self._last_filename_update != datetime.date.today():
			self._open_current_file()
		
		#logging.debug("Writing data to file for " + self._value_name)
		self._fileobj.write('%.3f\t%.8g\n' % (update_time, value))

