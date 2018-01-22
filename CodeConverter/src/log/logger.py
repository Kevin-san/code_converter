#!/usr/local/jython2.7/bin/jython

# -*- coding:UTF-8 -*-


import logging
import os
import time
import os.path

def get_log(log_name,logger_name):
	time_str = time.strftime("%Y_%m_%d", time.localtime(time.time()))
	logname = time_str + '_' + log_name + '.log'
	
	log_filedir = os.getcwd()
	if not os.path.isdir(log_filedir):
		print("%s not exist,start create log dir" %log_filedir)
		os.mkdir(log_filedir)
	else:
		print("log dir %s exist" %log_filedir)
	
	os.chdir(log_filedir)
	
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.DEBUG)
	
	file_handler = logging.FileHandler(logname)
	file_handler.setLevel(logging.DEBUG)
	
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.DEBUG)
	
	formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
	file_handler.setFormatter(formatter)
	console_handler.setFormatter(formatter)
	
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)
	return logger
	
