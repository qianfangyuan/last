# -*- coding: utf-8 -*-
import multiprocessing
import os,sys
from tool import background
import time

class TransferDaemon(background.Daemon):
	def _run(self,queue):
		if not isinstance(queue,multiprocessing.queues.Queue):
			return 0
		while 1:
			#sys.stdout.write('%s:hello world\n' % (time.ctime(),))
			sys.stdout.write('%s\n'%queue.get())
			sys.stdout.flush()


def handler_transfer(handler,log_file,pid_file,tqueue):
#	abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
#	transfer_log_file=abspath+'/log/server.log'
#	transfer_pid_file=abspath+'/run/server.pid'
	td=TransferDaemon(pid_file,stdout=log_file)
	if handler == 'start':
		td.start(tqueue)
	elif handler == 'stop':
		td.stop()
	elif handler == 'restart':
		td.restart()
	else:  
		return 0
	
if __name__ == "__main__":
	abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
	transfer_log_file=abspath+'/log/transfer.log'
	transfer_pid_file=abspath+'/run/transfer.pid'
	tqueue=multiprocessing.Queue(1024)
	if len(sys.argv) == 2:  
		if 'start' == sys.argv[1]:  
			handler_transfer('start',transfer_log_file,transfer_pid_file,tqueue)
		elif 'stop' == sys.argv[1]:  
			handler_transfer('stop',transfer_log_file,transfer_pid_file,tqueue)
		elif 'restart' == sys.argv[1]:  
			handler_transfer('restart',transfer_log_file,transfer_pid_file,tqueue)
		else:  
			print 'unknown command'  
			sys.exit(2)  
			sys.exit(0)  
	else:  
		print 'usage: %s start|stop|restart' % sys.argv[0]  
		sys.exit(2)  
