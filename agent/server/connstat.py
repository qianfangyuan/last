# -*- coding: utf-8 -*-
import re
import time
import logging
import os
import commands

TCP_CONNSTAT=['tcp_established','tcp_listen','tcp_timewait','tcp_closewait','tcp_synsent','tcp_synrecv','tcp_synwait','tcp_finwait1','tcp_finwait2','tcp_closed','tcp_lastack','tcp_closing','tcp_unknown']
UDP_CONNSTAT=['udp_unconn','udp_estab']


SS_COMMAND='ss -a --query=all  -n'
#Netid,State,Recv-Q,Send-Q,Local Address:Port,Peer Address:Port
SS_COMMAND_TCP_UDP='ss --tcp --udp -a -n'
NETSTAT_COMMAND='netstat -anlp'

commands.getoutput(SS_COMMAND_TCP_UDP)

CONN_PORT=3306

def conn_status():
	#conn[protocol][protocol_state] = num
	#conn[protocol][port][protocol_state] = num
	conn = {}
	conn['tcp'] = {}
	conn['udp'] = {}
	try:
		result = commands.getoutput(SS_COMMAND_TCP_UDP)
	except Exception,e:
		logging.error('command ss is not install')
		return 0
	for tmp_result in result.split('\n')[1:]:
		try:
			protocol,protocol_state,recv_q,send_q,local_ip_port,peer_ip_port = tmp_result.split()
		except:
			logging.error('error format command ss output')
			continue
		protocol_state = protocol_state.lower()
		if protocol_state in conn[protocol]:
			conn[protocol][protocol_state] = conn[protocol][protocol_state]+1
		else:
			conn[protocol][protocol_state] = 1
		local_port=int(local_ip_port.split(':')[-1])
		if local_port in conn:
			conn[local_port]=conn[local_port]+1
		else:
			conn[local_port]=1
	return conn
def get_conn_status():
	while 1:
		print conn_status()
		time.sleep(1)

if __name__ == "__main__":
	get_conn_status()
