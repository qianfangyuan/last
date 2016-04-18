import logging
LOG_FILE='/tmp/log'
LOG_FORMAT=logging.Formatter('%(asctime)s[%(levelname)s]-%(funcName)s(%(lineno)d):%(message)s')
LOG_DATE_FORMAT='%Y-%m-%d %H:%M:%S'
logging.basicConfig(
	level=logging.Warning,
	format=LOG_FORMAT,
	datefmt=LOG_DATE_FORMAT,  
	filename=LOG_FILE,  
	filemode='a')
