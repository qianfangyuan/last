from greenlet import greenlet
from server import connstat
from server import diskfree
from server import diskstat
from server import mem
from server import network
from server import cpu_stat
import time
from CONCAT import FIELD
import multiprocessing
import sys,os
from tool import background
import multiprocessing

PROC_STAT=''
DISK_STATS=FIELD.DISK_STATS
CPU_STAT=FIELD.CPU_STAT_2_6_24
NET_STAT=FIELD.NET_STAT
QUEUE=''
GLS={}

set_max_value_hundred=lambda x : x > 100 and 100 or x
def get_conn_status():
	while 1:
		mtime=time.time()
		tmp_result=connstat.conn_status()
		if tmp_result == 0:
			time.sleep(1)
			continue
		out_status(tmp_result,mtime)
		GLS['gl_df'].switch()

def get_disk_free():
	while 1:
		mtime=time.time()
		tmp_result=diskfree.diskfree()
		if tmp_result == 0 :
			time.sleep(1)
			continue
		out_status(tmp_result,mtime)
		GLS['gl_ds'].switch()

def get_disk_stat():
	tmp_result={}
	btime=time.time()
	tmp_before=diskstat.disk_stat()
	if tmp_before == 0:
		return 0
	while 1:
		tmp_after=diskstat.disk_stat()
		atime=time.time()
		if tmp_after == 0:
			time.sleep(1)
			continue
		interval=atime-btime
		for dk,dv in tmp_before.iteritems():
			if dk in tmp_after:
				tmp_result[dk]={}
				for i in dv:
					tmp_result[dk][DISK_STATS[0]] = int((tmp_after[dk][DISK_STATS[0]] - tmp_before[dk][DISK_STATS[0]]) / interval)
					tmp_result[dk][DISK_STATS[1]] = int((tmp_after[dk][DISK_STATS[1]] - tmp_before[dk][DISK_STATS[1]]) / interval)
					tmp_result[dk][DISK_STATS[2]] = int((tmp_after[dk][DISK_STATS[2]] - tmp_before[dk][DISK_STATS[2]]) / interval)
					tmp_result[dk][DISK_STATS[3]] = int((tmp_after[dk][DISK_STATS[3]] - tmp_before[dk][DISK_STATS[3]]) / interval)
					tmp_result[dk][DISK_STATS[4]] = int((tmp_after[dk][DISK_STATS[4]] - tmp_before[dk][DISK_STATS[4]]) / interval)
					tmp_result[dk][DISK_STATS[5]] = int((tmp_after[dk][DISK_STATS[5]] - tmp_before[dk][DISK_STATS[5]]) / interval)
					tmp_result[dk][DISK_STATS[6]] = int((tmp_after[dk][DISK_STATS[6]] - tmp_before[dk][DISK_STATS[6]]) / interval)
					tmp_result[dk][DISK_STATS[7]] = int((tmp_after[dk][DISK_STATS[7]] - tmp_before[dk][DISK_STATS[7]]) / interval)
					tmp_result[dk][DISK_STATS[8]] = int((tmp_after[dk][DISK_STATS[8]] - tmp_before[dk][DISK_STATS[8]]) / interval)
					tmp_result[dk][DISK_STATS[9]] = int((tmp_after[dk][DISK_STATS[9]] - tmp_before[dk][DISK_STATS[9]]) / interval)
					tmp_result[dk][DISK_STATS[10]] = int((tmp_after[dk][DISK_STATS[10]] - tmp_before[dk][DISK_STATS[10]]) / interval)
		tmp_before=tmp_after
		btime=atime
		out_status(tmp_result,atime)
		GLS['gl_ms'].switch()

def get_mem_stat():
	while 1:
		tmp_result=mem.get_memory_stat()
		mtime=time.time()
		if tmp_result == 0:
			time.sleep(1)
			continue
		out_status(tmp_result,mtime)
		GLS['gl_cs'].switch()
def get_network_stat():
	tmp_result = {}
	tmp_before = network.net_stat()
	btime=time.time()
	if tmp_before == 0:
		return 0
	while 1:
		tmp_after = network.net_stat()
		atime=time.time()
		if tmp_after == 0:
			time.sleep(1)
			continue
		interval=atime-btime
		for nk,nv in tmp_before.iteritems():
			if nk in tmp_after:
				tmp_result[nk]={}
				tmp_result[nk][NET_STAT[0]] =int((tmp_after[nk][NET_STAT[0]] - tmp_before[nk][NET_STAT[0]])/interval)
				tmp_result[nk][NET_STAT[1]] =int((tmp_after[nk][NET_STAT[1]] - tmp_before[nk][NET_STAT[1]])/interval)
				tmp_result[nk][NET_STAT[2]] =int((tmp_after[nk][NET_STAT[2]] - tmp_before[nk][NET_STAT[2]])/interval)
				tmp_result[nk][NET_STAT[3]] =int((tmp_after[nk][NET_STAT[3]] - tmp_before[nk][NET_STAT[3]])/interval)
				tmp_result[nk][NET_STAT[4]] =int((tmp_after[nk][NET_STAT[4]] - tmp_before[nk][NET_STAT[4]])/interval)
				tmp_result[nk][NET_STAT[5]] =int((tmp_after[nk][NET_STAT[5]] - tmp_before[nk][NET_STAT[5]])/interval)
				tmp_result[nk][NET_STAT[6]] =int((tmp_after[nk][NET_STAT[6]] - tmp_before[nk][NET_STAT[6]])/interval)
				tmp_result[nk][NET_STAT[7]] =int((tmp_after[nk][NET_STAT[7]] - tmp_before[nk][NET_STAT[7]])/interval)
				tmp_result[nk][NET_STAT[8]] =int((tmp_after[nk][NET_STAT[8]] - tmp_before[nk][NET_STAT[8]])/interval)
				tmp_result[nk][NET_STAT[9]] =int((tmp_after[nk][NET_STAT[9]] - tmp_before[nk][NET_STAT[9]])/interval)
				tmp_result[nk][NET_STAT[10]] =int((tmp_after[nk][NET_STAT[10]] - tmp_before[nk][NET_STAT[10]])/interval)
				tmp_result[nk][NET_STAT[11]] =int((tmp_after[nk][NET_STAT[11]] - tmp_before[nk][NET_STAT[11]])/interval)
				tmp_result[nk][NET_STAT[12]] =int((tmp_after[nk][NET_STAT[12]] - tmp_before[nk][NET_STAT[12]])/interval)
				tmp_result[nk][NET_STAT[13]] =int((tmp_after[nk][NET_STAT[13]] - tmp_before[nk][NET_STAT[13]])/interval)
				tmp_result[nk][NET_STAT[14]] =int((tmp_after[nk][NET_STAT[14]] - tmp_before[nk][NET_STAT[14]])/interval)
				tmp_result[nk][NET_STAT[15]] =int((tmp_after[nk][NET_STAT[15]] - tmp_before[nk][NET_STAT[15]])/interval)
		tmp_before = tmp_after
		btime=atime
		out_status(tmp_result,atime)
		GLS['gl_st'].switch()


def get_cpu_stat():
	proc_stat=PROC_STAT
	tmp_result={}
	tmp_before=proc_stat()
	btime=time.time()
	if tmp_before == 0:
		return 0
	while 1:
		tmp_after=proc_stat()
		atime=time.time()
		if tmp_after == 0:
			time.sleep(1)
			continue
		interval=atime-btime
		for pk,pv in tmp_before.iteritems():
			if pk in tmp_after:
				if pk == 'other_proc':
					tmp_result['other_proc']={}
					tmp_result['other_proc']['ctxt'] = set_max_value_hundred(int(( tmp_after['other_proc']['ctxt'] - tmp_before['other_proc']['ctxt'] )/interval))
					tmp_result['other_proc']['processes'] = set_max_value_hundred(int(( tmp_after['other_proc']['processes'] - tmp_before['other_proc']['processes'] )/interval))
					tmp_result['other_proc']['procs_running'] = tmp_after['other_proc']['procs_running']
					tmp_result['other_proc']['procs_blocked'] = tmp_after['other_proc']['procs_blocked']
					#tmp_result['other_proc']['btime'] = tmp_after['other_proc']['btime']/interval))
					continue
				tmp_result[pk]={}
				tmp_result[pk][CPU_STAT[0]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[0]] - tmp_before[pk][CPU_STAT[0]] )/interval))
				tmp_result[pk][CPU_STAT[1]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[1]] - tmp_before[pk][CPU_STAT[1]] )/interval))
				tmp_result[pk][CPU_STAT[2]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[2]] - tmp_before[pk][CPU_STAT[2]] )/interval))
				tmp_result[pk][CPU_STAT[3]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[3]] - tmp_before[pk][CPU_STAT[3]] )/interval))
				tmp_result[pk][CPU_STAT[4]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[4]] - tmp_before[pk][CPU_STAT[4]] )/interval))
				tmp_result[pk][CPU_STAT[5]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[5]] - tmp_before[pk][CPU_STAT[5]] )/interval))
				tmp_result[pk][CPU_STAT[6]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[6]] - tmp_before[pk][CPU_STAT[6]] )/interval))
				tmp_result[pk][CPU_STAT[7]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[7]] - tmp_before[pk][CPU_STAT[7]] )/interval))
				tmp_result[pk][CPU_STAT[8]] = set_max_value_hundred(int(( tmp_after[pk][CPU_STAT[8]] - tmp_before[pk][CPU_STAT[8]] )/interval))
		tmp_before = tmp_after
		btime=atime
		out_status(tmp_result,atime)
		GLS['gl_ns'].switch()

def out_status(sstats,rtoime):
	if isinstance(QUEUE,multiprocessing.queues.Queue):
#	if type(QUEUE) == type(multiprocessing.Queue()):
		QUEUE.put(sstats)
	sys.stdout.write('%s\n'%sstats)
	sys.stdout.flush()
#	file1=open('/tmp/ll','w+')
#	file1.write(str(sstats))
#	file1.close()
#	print sstats
def sleep_time(interval=5):
	time.sleep(interval)
	GLS['gl_co'].switch()
def get_server_status(interval=5,queue=''):
	global 	PROC_STAT
	global GLS
	global QUEUE
	QUEUE=queue
	PROC_STAT=cpu_stat.proc_stat_2_6_24
	gl_co=greenlet(get_conn_status)
	gl_df=greenlet(get_disk_free)
	gl_ds=greenlet(get_disk_stat)
	gl_ms=greenlet(get_mem_stat)
	gl_ns=greenlet(get_network_stat)
	gl_cs=greenlet(get_cpu_stat)
	gl_st=greenlet(sleep_time)
#	gls={'gl_co':gl_co,'gl_df':gl_df,'gl_ds':gl_ds,'gl_ms':gl_ms,'gl_ns':gl_ns,'gl_cs':gl_cs,'gl_st':gl_st}
	GLS={'gl_co':gl_co,'gl_df':gl_df,'gl_ds':gl_ds,'gl_ms':gl_ms,'gl_ns':gl_ns,'gl_cs':gl_cs,'gl_st':gl_st}
	while 1:
		gl_co.switch()
		time.sleep(interval)

class ServerDaemon(background.Daemon):
	def _run(self,queue='',interval=5):
		get_server_status(interval,queue)	
		
def handler_daemon(handler,log_file,pid_file,tqueue,interval):
#	abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
#	server_log_file=abspath+'/log/server.log'
#	server_pid_file=abspath+'/run/server.pid'
	sd=ServerDaemon(pid_file,stdout = log_file)
	if handler == 'start':
		sd.start(tqueue)
	elif handler == 'stop':
		sd.stop()
	elif handler == 'restart':
		sd.restart()
	else:  
		return 0
	
if __name__ == "__main__":
	abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
	server_log_file=abspath+'/log/server.log'
	server_pid_file=abspath+'/run/server.pid'
	interval=5
	if len(sys.argv) == 2:  
		if 'start' == sys.argv[1]:  
			handler_daemon('start',server_log_file,server_pid_file,'',interval)
		elif 'stop' == sys.argv[1]:  
			handler_daemon('stop',server_log_file,server_pid_file,'',interval)
		elif 'restart' == sys.argv[1]:  
			handler_daemon('restart',server_log_file,server_pid_file,'',interval)
		else:  
			print 'unknown command'  
			sys.exit(2)  
			sys.exit(0)  
	else:  
		print 'usage: %s start|stop|restart' % sys.argv[0]  
		sys.exit(2)  
