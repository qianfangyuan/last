# -*- coding: utf-8 -*-
import multiprocessing
from tool import background
import get_server_status
import os,sys

class ServerDaemon(background.Daemon):
	def _run(self,queue=''):
		get_server_status.get_server_status(5,queue)	


if __name__ == '__main__':
	abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
	server_log_file=abspath+'/log/server.log'
	server_pid_file=abspath+'/run/server.pid'
	sd=ServerDaemon(server_pid_file,stdout = server_log_file)
	if len(sys.argv) == 2:  
		if 'start' == sys.argv[1]:  
			sd.start(tqueue)
		elif 'stop' == sys.argv[1]:  
			sd.stop()
		elif 'restart' == sys.argv[1]:  
			sd.restart()
		else:  
			print 'unknown command'  
			sys.exit(2)  
			sys.exit(0)  
	else:  
		print 'usage: %s start|stop|restart' % sys.argv[0]  
		sys.exit(2)  
	
