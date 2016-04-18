# -*- coding: utf-8 -*-
import re
import time
import logging


DISK_FILE='/proc/diskstats'
# 1 - major number
# 2 - minor mumber
# 3 - device name
# 4 - reads completed successfully
# 5 - reads merged
# 6 - sectors read
# 7 - time spent reading (ms)
# 8 - writes completed
# 9 - writes merged
#10 - sectors written
#11 - time spent writing (ms)
#12 - I/Os currently in progress
#13 - time spent doing I/Os (ms)
#14 - weighted time spent doing I/Os (ms)


#Field  1 -- # of reads completed
#    This is the total number of reads completed successfully.
#Field  2 -- # of reads merged, field 6 -- # of writes merged
#    Reads and writes which are adjacent to each other may be merged for
#    efficiency.  Thus two 4K reads may become one 8K read before it is
#    ultimately handed to the disk, and so it will be counted (and queued)
#    as only one I/O.  This field lets you know how often this was done.
#Field  3 -- # of sectors read
#    This is the total number of sectors read successfully.
#Field  4 -- # of milliseconds spent reading
#    This is the total number of milliseconds spent by all reads (as
#    measured from __make_request() to end_that_request_last()).
#Field  5 -- # of writes completed
#    This is the total number of writes completed successfully.
#Field  6 -- # of writes merged
#    See the description of field 2.
#Field  7 -- # of sectors written
#    This is the total number of sectors written successfully.
#Field  8 -- # of milliseconds spent writing
#    This is the total number of milliseconds spent by all writes (as
#    measured from __make_request() to end_that_request_last()).
#Field  9 -- # of I/Os currently in progress
#    The only field that should go to zero. Incremented as requests are
#    given to appropriate struct request_queue and decremented as they finish.
#Field 10 -- # of milliseconds spent doing I/Os
#    This field increases so long as field 9 is nonzero.
#Field 11 -- weighted # of milliseconds spent doing I/Os
#    This field is incremented at each I/O start, I/O completion, I/O
#    merge, or read of these stats by the number of I/Os in progress
#    (field 9) times the number of milliseconds spent doing I/O since the
#    last update of this field.  This can provide an easy measure of both
#    I/O completion time and the backlog that may be accumulating.

DISK_STATS=['reads','reads_merge','reads_sector','read_time','writes','write_merge','write_sector','write_time','io_curr','io_ms','io_weight']
def disk_stat():
	disk={}
	try:
		f=open(DISK_FILE,'r')
	except IOError:
		logging.error("can't open "+DISK_FILE)
		return 0
	for line in f:
		line_tmp=re.split('\s+',line)
		if line_tmp[1] >= '8' and line_tmp[1] != '11' and len(line_tmp) == 16:
			disk[line_tmp[3]]={ \
			DISK_STATS[0] : int(line_tmp[4]),\
			DISK_STATS[1] : int(line_tmp[5]),\
			DISK_STATS[2] : int(line_tmp[6]),\
			DISK_STATS[3] : int(line_tmp[7]),\
			DISK_STATS[4] : int(line_tmp[8]),\
			DISK_STATS[5] : int(line_tmp[9]),\
			DISK_STATS[6] : int(line_tmp[10]),\
			DISK_STATS[7] : int(line_tmp[11]),\
			DISK_STATS[8] : int(line_tmp[12]),\
			DISK_STATS[9] : int(line_tmp[13]),\
			DISK_STATS[10] : int(line_tmp[14])\
			}
		else:
			pass
	try:
		f.close()
	except IOError:
		return 0
	except Exception,e:
		return 0
#			logging.error("error read file "+DISK_FILE+" with line["+line+"]")
	return disk
def get_disk_stat():
	tmp_before={}
	while 1:
		tmp_result={}
		if tmp_before != {} :
			tmp_after=disk_stat()
			if tmp_after == 0:
				time.sleep(1)
				continue
			for dk,dv in tmp_before.iteritems():
				if dk in tmp_after:
					tmp_result[dk]={}
					for i in dv:
						tmp_result[dk][DISK_STATS[0]] = tmp_after[dk][DISK_STATS[0]] - tmp_before[dk][DISK_STATS[0]]
						tmp_result[dk][DISK_STATS[1]] = tmp_after[dk][DISK_STATS[1]] - tmp_before[dk][DISK_STATS[1]]
						tmp_result[dk][DISK_STATS[2]] = tmp_after[dk][DISK_STATS[2]] - tmp_before[dk][DISK_STATS[2]]
						tmp_result[dk][DISK_STATS[3]] = tmp_after[dk][DISK_STATS[3]] - tmp_before[dk][DISK_STATS[3]]
						tmp_result[dk][DISK_STATS[4]] = tmp_after[dk][DISK_STATS[4]] - tmp_before[dk][DISK_STATS[4]]
						tmp_result[dk][DISK_STATS[5]] = tmp_after[dk][DISK_STATS[5]] - tmp_before[dk][DISK_STATS[5]]
						tmp_result[dk][DISK_STATS[6]] = tmp_after[dk][DISK_STATS[6]] - tmp_before[dk][DISK_STATS[6]]
						tmp_result[dk][DISK_STATS[7]] = tmp_after[dk][DISK_STATS[7]] - tmp_before[dk][DISK_STATS[7]]
						tmp_result[dk][DISK_STATS[8]] = tmp_after[dk][DISK_STATS[8]] - tmp_before[dk][DISK_STATS[8]]
						tmp_result[dk][DISK_STATS[9]] = tmp_after[dk][DISK_STATS[9]] - tmp_before[dk][DISK_STATS[9]]
						tmp_result[dk][DISK_STATS[10]] = tmp_after[dk][DISK_STATS[10]] - tmp_before[dk][DISK_STATS[10]]
			tmp_before=tmp_after
		else:
			tmp_before=disk_stat()
		time.sleep(1)
		print tmp_result			
if __name__ == "__main__":
	get_disk_stat()
