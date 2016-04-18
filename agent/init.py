# -*- coding: utf-8 -*-
import multiprocessing
from tool import background
import server_status
import transfer
import os,sys
import mysql_status

def start_transfer(transfer_log_file,transfer_pid_file,queue=''):
	transfer.handler_transfer('start',transfer_log_file,transfer_pid_file,queue)
def stop_transfer(transfer_log_file,transfer_pid_file,queue=''):
	transfer.handler_transfer('stop',transfer_log_file,transfer_pid_file,queue)

def start_server(server_log_file,server_pid_file,queue='',interval=5):
	server_status.handler_daemon('start',server_log_file,server_pid_file,queue,interval)
def stop_server(server_log_file,server_pid_file,queue='',interval=5):
	server_status.handler_daemon('stop',server_log_file,server_pid_file,queue,interval)

def start_mysql(mysql_log_file,mysql_pid_file,queue='',interval=5):
	mysql_status.handler_daemon('start',mysql_log_file,mysql_pid_file,queue,interval)
def stop_mysql(mysql_log_file,mysql_pid_file,queue='',interval=5):
	mysql_status.handler_daemon('stop',mysql_log_file,mysql_pid_file,queue,interval)



if __name__ == '__main__':
	abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
	server_log_file=abspath+'/log/server_status.log'
	server_pid_file=abspath+'/run/server_status.pid'
	transfer_log_file=abspath+'/log/transfer.log'
	transfer_pid_file=abspath+'/run/transfer.pid'
	mysql_log_file=abspath+'/log/mysql_status.log'
	mysql_pid_file=abspath+'/run/mysql_status.pid'
	qsize=1024
	tqueue=multiprocessing.Queue(qsize)
	if len(sys.argv) == 2:  
		if 'start' == sys.argv[1]:  
			sp=multiprocessing.Process(target=start_server,args=(server_log_file,server_pid_file,tqueue,5))
			tp=multiprocessing.Process(target=start_transfer,args=(transfer_log_file,transfer_pid_file,tqueue))
			mp=multiprocessing.Process(target=start_mysql,args=(mysql_log_file,mysql_pid_file,tqueue,5))
			tp.start()
			mp.start()
			sp.start()
		elif 'stop' == sys.argv[1]:  
			stop_server(server_log_file,server_pid_file,tqueue,5)
			stop_transfer(transfer_log_file,transfer_pid_file,tqueue)
			stop_mysql(mysql_log_file,mysql_pid_file,tqueue,5)
		elif 'restart' == sys.argv[1]:  
			stop_server(server_log_file,server_pid_file,tqueue,5)
			stop_transfer(transfer_log_file,transfer_pid_file,tqueue)
			stop_mysql(mysql_log_file,mysql_pid_file,tqueue,5)
			sp=multiprocessing.Process(target=start_server,args=(server_log_file,server_pid_file,tqueue,5))
			tp=multiprocessing.Process(target=start_transfer,args=(transfer_log_file,transfer_pid_file,tqueue))
			mp=multiprocessing.Process(target=start_mysql,args=(mysql_log_file,mysql_pid_file,tqueue,5))
			tp.start()
			mp.start()
			sp.start()
		else:  
			print 'unknown command'  
			sys.exit(2)  
			sys.exit(0)  
	else:  
		print 'usage: %s start|stop|restart' % sys.argv[0]  
		sys.exit(2)  
	
