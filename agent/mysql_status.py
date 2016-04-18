from tool import background
import multiprocessing
import os,sys
from mysql import mysql_status

class MySQLStatusDaemon(background.Daemon):
	def _run(self,tqueue='',interval=5):
		mysql_status.get_mysql_status('127.0.0.1',3306,'root','',tqueue,interval)	
		
def handler_daemon(handler,log_file,pid_file,tqueue,interval):
#	abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
#	mysql_status_log_file=abspath+'/log/mysql_status.log'
#	mysql_status_pid_file=abspath+'/run/mysql_status.pid'
	msd=MySQLStatusDaemon(pid_file,stdout = log_file)
	if handler == 'start':
		msd.start(tqueue)
	elif handler == 'stop':
		msd.stop()
	elif handler == 'restart':
		msd.restart()
	else:  
		return 0
	
if __name__ == "__main__":
	abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
	mysql_status_log_file=abspath+'/log/mysql_status.log'
	mysql_status_pid_file=abspath+'/run/mysql_status.pid'
	interval=5
	if len(sys.argv) == 2:  
		if 'start' == sys.argv[1]:  
			handler_daemon('start',mysql_status_log_file,mysql_status_pid_file,'',interval)
		elif 'stop' == sys.argv[1]:  
			handler_daemon('stop',mysql_status_log_file,mysql_status_pid_file,'',interval)
		elif 'restart' == sys.argv[1]:  
			handler_daemon('restart',mysql_status_log_file,mysql_status_pid_file,'',interval)
		else:  
			print 'unknown command'  
			sys.exit(2)  
			sys.exit(0)  
	else:  
		print 'usage: %s start|stop|restart' % sys.argv[0]  
		sys.exit(2)  
