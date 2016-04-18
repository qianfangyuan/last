# -*- coding: utf-8 -*-
import re
import time
import logging

NET_FILE='/proc/net/dev'

NET_STAT=['recv_bytes','recv_packets','recv_error','recv_drop','recv_fifo','recv_frame','recv_compressed','recv_multicast','send_bytes','send_packets','send_error','send_drop','send_fifo','send_frame','send_compressed','send_multicast']

def net_stat():
	try:
		f = open(NET_FILE,'r')
	except IOError:
		logging.error("error open "+NET_FILE)
		return 0
	net = {}
	for line in f:
		tmp_line = re.split('\s+',line)
		if len(tmp_line) == 19 and tmp_line[2] != 'lo:':
			net[tmp_line[1]]={}
			net[tmp_line[1]][NET_STAT[0]] = int(tmp_line[2])
			net[tmp_line[1]][NET_STAT[1]] = int(tmp_line[3])
			net[tmp_line[1]][NET_STAT[2]] = int(tmp_line[4])
			net[tmp_line[1]][NET_STAT[3]] = int(tmp_line[5])
			net[tmp_line[1]][NET_STAT[4]] = int(tmp_line[6])
			net[tmp_line[1]][NET_STAT[5]] = int(tmp_line[7])
			net[tmp_line[1]][NET_STAT[6]] = int(tmp_line[8])
			net[tmp_line[1]][NET_STAT[7]] = int(tmp_line[9])
			net[tmp_line[1]][NET_STAT[8]] = int(tmp_line[10])
			net[tmp_line[1]][NET_STAT[9]] = int(tmp_line[11])
			net[tmp_line[1]][NET_STAT[10]] = int(tmp_line[12])
			net[tmp_line[1]][NET_STAT[11]] = int(tmp_line[13])
			net[tmp_line[1]][NET_STAT[12]] = int(tmp_line[14])
			net[tmp_line[1]][NET_STAT[13]] = int(tmp_line[15])
			net[tmp_line[1]][NET_STAT[14]] = int(tmp_line[16])
			net[tmp_line[1]][NET_STAT[15]] = int(tmp_line[17])
	try:
		f.close()
	except Exception,e:
		return 0
	return net
def get_net_stat():
	tmp_before = {}
	while 1:
		if tmp_before != {}:
			tmp_result = {}
			tmp_after = net_stat()
			for nk,nv in tmp_before.iteritems():
				if nk in tmp_after:
					tmp_result[nk]={}
					tmp_result[nk][NET_STAT[0]] = tmp_after[nk][NET_STAT[0]] - tmp_before[nk][NET_STAT[0]]
					tmp_result[nk][NET_STAT[1]] = tmp_after[nk][NET_STAT[1]] - tmp_before[nk][NET_STAT[1]]
					tmp_result[nk][NET_STAT[2]] = tmp_after[nk][NET_STAT[2]] - tmp_before[nk][NET_STAT[2]]
					tmp_result[nk][NET_STAT[3]] = tmp_after[nk][NET_STAT[3]] - tmp_before[nk][NET_STAT[3]]
					tmp_result[nk][NET_STAT[4]] = tmp_after[nk][NET_STAT[4]] - tmp_before[nk][NET_STAT[4]]
					tmp_result[nk][NET_STAT[5]] = tmp_after[nk][NET_STAT[5]] - tmp_before[nk][NET_STAT[5]]
					tmp_result[nk][NET_STAT[6]] = tmp_after[nk][NET_STAT[6]] - tmp_before[nk][NET_STAT[6]]
					tmp_result[nk][NET_STAT[7]] = tmp_after[nk][NET_STAT[7]] - tmp_before[nk][NET_STAT[7]]
					tmp_result[nk][NET_STAT[8]] = tmp_after[nk][NET_STAT[8]] - tmp_before[nk][NET_STAT[8]]
					tmp_result[nk][NET_STAT[9]] = tmp_after[nk][NET_STAT[9]] - tmp_before[nk][NET_STAT[9]]
					tmp_result[nk][NET_STAT[10]] = tmp_after[nk][NET_STAT[10]] - tmp_before[nk][NET_STAT[10]]
					tmp_result[nk][NET_STAT[11]] = tmp_after[nk][NET_STAT[11]] - tmp_before[nk][NET_STAT[11]]
					tmp_result[nk][NET_STAT[12]] = tmp_after[nk][NET_STAT[12]] - tmp_before[nk][NET_STAT[12]]
					tmp_result[nk][NET_STAT[13]] = tmp_after[nk][NET_STAT[13]] - tmp_before[nk][NET_STAT[13]]
					tmp_result[nk][NET_STAT[14]] = tmp_after[nk][NET_STAT[14]] - tmp_before[nk][NET_STAT[14]]
					tmp_result[nk][NET_STAT[15]] = tmp_after[nk][NET_STAT[15]] - tmp_before[nk][NET_STAT[15]]
			tmp_before = tmp_after
			print tmp_result
		if tmp_before == {}:
			tmp_before = net_stat()
		time.sleep(1)
if __name__ == "__main__":
	get_net_stat()
