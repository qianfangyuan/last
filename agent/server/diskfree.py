# -*- coding: utf-8 -*-
import re
import time
import os
import logging

MOUNT_FILE='/proc/mounts'


# os.statvfs() and os.fstatvfs().  
#F_BSIZE   = 0           # Preferred file system block size  
#F_FRSIZE  = 1           # Fundamental file system block size  
#F_BLOCKS  = 2           # Total number of file system blocks (FRSIZE)  
#F_BFREE   = 3           # Total number of free blocks  
#F_BAVAIL  = 4           # Free blocks available to non-superuser  
#F_FILES   = 5           # Total number of file nodes  
#F_FFREE   = 6           # Total number of free file nodes  
#F_FAVAIL  = 7           # Free nodes available to non-superuser  
#F_FLAG    = 8           # Flags (see your local statvfs man page)  
#F_NAMEMAX = 9           # Maximum file name length  


DISK_FREE=['diskfree','diskfreepercent','diskfreeinode']
SKIP_FS=['proc','autofs','iso9660','usbfs']
def diskfree():
	try:
		f=open(MOUNT_FILE,'r')
	except IOError:
		logging.error("error open "+MOUNT_FILE)
		return 0
	diskfree = {}
	for line in f:
		if line[0] == '/' :
			tmp_line = re.split('\s',line)
			if tmp_line[2] in SKIP_FS:continue
			disk_tmp = os.statvfs(tmp_line[1])
			diskfree[tmp_line[1]]={}
			diskfree[tmp_line[1]][DISK_FREE[0]] = (disk_tmp.f_bavail * disk_tmp.f_frsize) / float(2 ** 30)
			diskfree[tmp_line[1]][DISK_FREE[1]] = int((float(disk_tmp.f_bavail) / float(disk_tmp.f_blocks)) * 10000) 
			diskfree[tmp_line[1]][DISK_FREE[2]] = int((float(disk_tmp.f_ffree) / float(disk_tmp.f_files)) * 10000)
	try:
		f.close()
	except Exception,e:
		pass
	return diskfree
def get_diskfree():
	while 1:
		print diskfree()	
		time.sleep(1)
if __name__ == "__main__":
	get_diskfree()
