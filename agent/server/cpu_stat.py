# -*- coding: utf-8 -*-
import logging
import time
import re

STAT_FILE = '/proc/stat'

#     user  : Time spent in user mode.
#     nice  : Time spent in user mode with low priority (nice).
#    system : Time spent in system mode.
#     idle  : Time spent in the idle task. This value should be USER_HZ times the second entry in the /proc/uptime pseudo-file.
#    iowait : Time waiting for I/O to complete. (since Linux 2.5.41)
#      irq  : Time servicing interrupts.(since Linux 2.6.0-test4)
#   softirq : Time servicing softirqs.(since Linux 2.6.0-test4)
#     steal : Stolen time, which is the time spent in other_proc operating systems when running in a virtualized environment.(since Linux 2.6.11)
#     guest : Time spent running a virtual CPU for guest operating systems under the control of the Linux kernel.(since Linux 2.6.24)
#guest_nice : Time spent running a niced guest (virtual CPU for guest operating systems under the control of the Linux kernel).(since Linux 2.6.33)

set_max_value=lambda x : x > 100 and 100 or x
CPU_STAT_2_6_11 = ['cpu_user','cpu_nice','cpu_system','cpu_idle','cpu_iowait','cpu_irq','cpu_softirq']
CPU_STAT_2_6_24 = ['cpu_user','cpu_nice','cpu_system','cpu_idle','cpu_iowait','cpu_irq','cpu_softirq','cpu_steal','cpu_guest']
CPU_STAT_2_6_33 = ['cpu_user','cpu_nice','cpu_system','cpu_idle','cpu_iowait','cpu_irq','cpu_softirq','cpu_steal','cpu_guest','cpu_guest_nice']
OTHER_PROC = ['ctxt','btime','processes','procs_running','procs_blocked']
def proc_stat_2_6_24():
	proc = {}
	proc['other_proc']={}
	try:
		f=open(STAT_FILE,'r')
	except IOError:
		logging.error("Error open "+STAT_FILE)
		return 0
	for line in f:
		tmp_line = re.split('\s+',line)
		if len(tmp_line) == 11:
			proc[tmp_line[0]]={}
			proc[tmp_line[0]][CPU_STAT_2_6_24[0]] = int(tmp_line[1])
			proc[tmp_line[0]][CPU_STAT_2_6_24[1]] = int(tmp_line[2])
			proc[tmp_line[0]][CPU_STAT_2_6_24[2]] = int(tmp_line[3])
			proc[tmp_line[0]][CPU_STAT_2_6_24[3]] = int(tmp_line[4])
			proc[tmp_line[0]][CPU_STAT_2_6_24[4]] = int(tmp_line[5])
			proc[tmp_line[0]][CPU_STAT_2_6_24[5]] = int(tmp_line[6])
			proc[tmp_line[0]][CPU_STAT_2_6_24[6]] = int(tmp_line[7])
			proc[tmp_line[0]][CPU_STAT_2_6_24[7]] = int(tmp_line[8])
			proc[tmp_line[0]][CPU_STAT_2_6_24[8]] = int(tmp_line[9])
			proc[tmp_line[0]]['cpu_guest_nice'] = 0
			continue
		if len(tmp_line) == 3:
			if tmp_line[0] in OTHER_PROC:
				proc['other_proc'][tmp_line[0]] = int(tmp_line[1])
	try:
		f.close()
	except Exception:
		pass
	return proc
def get_proc_stat():
	tmp_before={}
	while 1:
		tmp_result={}
		if tmp_before !={}:
			tmp_after=proc_stat_2_6_24()
			if tmp_after == 0:
				time.sleep(1)
				continue
			for pk,pv in tmp_before.iteritems():
				if pk in tmp_after:
					if pk == 'other_proc':
						tmp_result['other_proc']={}
						tmp_result['other_proc']['ctxt'] = set_max_value( tmp_after['other_proc']['ctxt'] - tmp_before['other_proc']['ctxt'] )
						tmp_result['other_proc']['processes'] = set_max_value( tmp_after['other_proc']['processes'] - tmp_before['other_proc']['processes'] )
						tmp_result['other_proc']['procs_running'] = tmp_after['other_proc']['procs_running']
						tmp_result['other_proc']['procs_blocked'] = tmp_after['other_proc']['procs_blocked']
						#tmp_result['other_proc']['btime'] = tmp_after['other_proc']['btime']
						continue
					tmp_result[pk]={}
					tmp_result[pk][CPU_STAT_2_6_24[0]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[0]] - tmp_before[pk][CPU_STAT_2_6_24[0]] )
					tmp_result[pk][CPU_STAT_2_6_24[1]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[1]] - tmp_before[pk][CPU_STAT_2_6_24[1]] )
					tmp_result[pk][CPU_STAT_2_6_24[2]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[2]] - tmp_before[pk][CPU_STAT_2_6_24[2]] )
					tmp_result[pk][CPU_STAT_2_6_24[3]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[3]] - tmp_before[pk][CPU_STAT_2_6_24[3]] )
					tmp_result[pk][CPU_STAT_2_6_24[4]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[4]] - tmp_before[pk][CPU_STAT_2_6_24[4]] )
					tmp_result[pk][CPU_STAT_2_6_24[5]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[5]] - tmp_before[pk][CPU_STAT_2_6_24[5]] )
					tmp_result[pk][CPU_STAT_2_6_24[6]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[6]] - tmp_before[pk][CPU_STAT_2_6_24[6]] )
					tmp_result[pk][CPU_STAT_2_6_24[7]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[7]] - tmp_before[pk][CPU_STAT_2_6_24[7]] )
					tmp_result[pk][CPU_STAT_2_6_24[8]] = set_max_value( tmp_after[pk][CPU_STAT_2_6_24[8]] - tmp_before[pk][CPU_STAT_2_6_24[8]] )
			tmp_before = tmp_after
		else:
			tmp_before=proc_stat_2_6_24()
		time.sleep(1)
		print tmp_result
if __name__ == '__main__':
	get_proc_stat()
