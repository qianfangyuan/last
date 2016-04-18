import socket
import struce
import log
import sys

#IPPROTO_TCP
#IPPROTO_UDP
#IPPROTO_ICMP
#ETH_P_IP
#ETH_P_ARP
#ETH_P_ALL

def get_socket():
	try:
		hostname = socket.gethostname()
	except:
		log.logging("Error get hostname!")
		return 1
	try:
		hostip = socket.gethostbyname(hostname)
	except:
		logging.error("Error get ip,please set hostname and ip mappings!")
		return 1

	s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP)
	#s = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
	pkt = s.recvfrom(2048);
	#struct.unpack('!6s6s2s',pkt[0][0:14])
	#ethernetHeader=pkt[0][0:14]
	#eth_hdr = struct.unpack("!6s6s2s",ethernetHeader)
	#binascii.hexlify(eth_hdr[0])
	#binascii.hexlify(eth_hdr[1])
	#binascii.hexlify(eth_hdr[2])
	#ipHeader = pkt[0][14:34]
	#ip_hdr = struct.unpack("!12s4s4s",ipHeader)
	#print "Source IP address:"+socket.inet_ntoa(ip_hdr[1])
	#print "Destination IP address:"+socket.inet_ntoa(ip_hdr[2])
	#tcpHeader = pkt[0][34:54]
	#tcp_hdr = struct.unpack("!HH16s",tcpHeader)
	#tcp_version,tcp_header_len,tcp_tos,tcp_total_len,tcp_identifier,tcp_flag,tcp_offset,tcp_ttl,tcp_protocol,tcp_head_checksum,tcp_src_ip,tcp_dst_ip
	tcp_head,tcp_src_ip,tcp_dst_ip=struct.unpack("!12s4s4s",pkt[0][0:20])
	head_len=binascii.hexlify(struct.unpack("!12s4s4s",pkt1[0][0:20])[0])[1]
	if head_len == '5':
		tcp_src_port,tcp_dst_port,tcp_seq,tcp_ack_seq,
	else:
