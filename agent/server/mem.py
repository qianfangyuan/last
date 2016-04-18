# -*- coding: utf-8 -*-
import time
import json
import re
import logging

#data struct
#
#name:10
#value:10
#type:x
#description:xxxx

MEM_FILE="/proc/meminfo"
MEM_STATS= {\
#orgname:[name,orgname,unit]
'MemTotal':['mem_total','MemTotal','kB'],\
'MemFree':['mem_free','MemFree','kB'],\
'Buffers':['mem_buffer','Buffers','kB'],\
'Cached':['cached','Cached','kB'],\
'Active':['mem_swap_cached','SwapCached','kB'],\
'Active':['mem_active','Active','kB'],\
'Inactive':['mem_inactive','Inactive','kB'],\
'AnonPages':['mem_total_anon','AnonPages','kB'],\
'Active(anon)':['mem_active_anon','Active(anon)','kB'],\
'Inactive(anon)':['mem_inactive,anon','Inactive(anon)','kB'],\
'Active(file)':['mem_active_file','Active(file)','kB'],\
'Inactive(file)':['mem_inactive_file','Inactive(file)','kB'],\
'SwapTotal':['swap_total','SwapTotal','kB'],\
'SwapFree':['swap_free','SwapFree','kB'],\
'Dirty':['mem_dirty','Dirty','kB'],\
'Writeback':['mem_writeback','Writeback','kB'],\
'HugePages_Total':['hugepage_total','HugePages_Total',''],\
'HugePages_Free':['hugepage_free','HugePages_Free',''],\
'HugePages_Rsvd':['hugepage_reserved','HugePages_Rsvd',''],\
'HugePages_Surp':['hugepage_surplus','HugePages_Surp',''],\
'Hugepagesize':['hugepage_size','Hugepagesize','kB'],\
}


def get_memory_stat():
	mem = {}
	try:
		f=open(MEM_FILE,'r')
	except IOError:
		logging.error("can't open "+MEM_FILE)
		return 0
	for line in f:
		line_tmp=re.split('\s+',line)
		if len(line_tmp) < 2:continue
		if line_tmp[0][:-1] in MEM_STATS:
			if line_tmp[2] == MEM_STATS[line_tmp[0][:-1]][2]:
				mem[MEM_STATS[line_tmp[0][:-1]][0]]=int(line_tmp[1])
			else:
				mem[MEM_STATS[line_tmp[0][:-1]][0]]=format_unit(line_tmp[1],line_tmp[2])
	try:
		f.close()
	except Exception,e:
		pass
	return mem
def format_unit(data,unit):
	unit=unit.lower()
	if unit == 'bytes' or unit == 'b':
		return data/1024
	elif unit == 'mb' or unit == 'm':
		return data*1024
	elif unit == 'gb' or unit == 'b':
		return data*1024*1024
	else:
		return data

if __name__ == '__main__':
	while 1 :
		print get_memory_stat()
		time.sleep(1)
