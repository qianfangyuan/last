# -*- coding: utf-8 -*-
import pymysql
import logging
import collections
import re
import time
import os,sys
import multiprocessing
absdir=os.path.dirname(os.path.abspath(os.path.dirname(sys.argv[0])))
sys.path.append(absdir)
from tool import util
from CONCAT import FIELD
GET_MYSQL_VERSION="SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES WHERE VARIABLE_NAME IN ('VERSION_COMMENT','VERSION');"

GLOBAL_STATUS=["BYTES_SENT","BYTES_RECEIVED",\
"COM_SELECT","COM_INSERT","COM_UPDATE","COM_DELETE",\
"INNODB_BUFFER_POOL_READS","INNODB_BUFFER_POOL_READ_REQUESTS","INNODB_BUFFER_POOL_WRITE_REQUESTS",\
"INNODB_ROWS_INSERTED","INNODB_ROWS_DELETED","INNODB_ROWS_UPDATED","INNODB_ROWS_READ",\
"THREADS_CREATED","THREADS_CONNECTED","THREADS_RUNNING","THREADS_CACHED",\
"INNODB_BUFFER_POOL_PAGES_TOTAL","INNODB_BUFFER_POOL_PAGES_DATA","INNODB_BUFFER_POOL_PAGES_FREE","INNODB_BUFFER_POOL_PAGES_FLUSHED","INNODB_BUFFER_POOL_PAGES_DIRTY"\
"INNODB_DATA_READ","INNODB_DATA_READS","INNODB_DATA_WRITES","INNODB_DATA_WRITTEN",\
"INNODB_OS_LOG_FSYNCS","INNODB_OS_LOG_WRITTEN",\
"CONNECTIONS",\
"INNODB_LSN_CURRENT","INNODB_LSN_FLUSHED","INNODB_LSN_LAST_CHECKPOINT",\
"INNODB_ROW_LOCK_TIME","INNODB_ROW_LOCK_CURRENT_WAITS",\
"INNODB_S_LOCK_OS_WAITS","INNODB_S_LOCK_SPIN_ROUNDS","INNODB_S_LOCK_SPIN_WAITS","INNODB_X_LOCK_OS_WAITS","INNODB_X_LOCK_SPIN_ROUNDS","INNODB_X_LOCK_SPIN_WAITS",\
"OPEN_TABLES","OPEN_FILES","OPENED_VIEWS",\
"KEY_READS","KEY_READ_REQUESTS","KEY_WRITE_REQUESTS","KEY_WRITES",\
"INNODB_LOG_WAITS","INNODB_LOG_WRITE_REQUESTS","INNODB_LOG_WRITES",\
"TABLE_LOCKS_IMMEDIATE","TABLE_LOCKS_WAITED",\
"THREADPOOL_IDLE_THREADS","THREADPOOL_THREADS",\
"INNODB_MASTER_THREAD_ACTIVE_LOOPS","INNODB_MASTER_THREAD_IDLE_LOOPS",\
"INNODB_MEM_TOTAL","INNODB_MEM_ADAPTIVE_HASH","INNODB_MEM_DICTIONARY",\
"INNODB_HISTORY_LIST_LENGTH",\
"HANDLER_COMMIT","HANDLER_ROLLBACK","HANDLER_SAVEPOINT","HANDLER_MRR_INIT","HANDLER_UPDATE","HANDLER_DELETE",\
"HANDLER_READ_FIRST","HANDLER_READ_KEY","HANDLER_READ_NEXT","HANDLER_READ_NEXT","HANDLER_READ_PREV","HANDLER_READ_RND","HANDLER_READ_RND_NEXT",\
"SELECT_FULL_JOIN","SELECT_FULL_RANGE_JOIN","SELECT_RANGE","SELECT_RANGE_CHECK","SELECT_SCAN",\
"CREATED_TMP_DISK_TABLES","CREATED_TMP_TABLES",\
"EMPTY_QUERIES","EXECUTED_EVENTS","COM_EMPTY_QUERY","EMPTY_QUERIES"
]


GET_MYSQL_STATUS='SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME IN ("BYTES_SENT","BYTES_RECEIVED","COM_SELECT","COM_INSERT","COM_UPDATE","COM_DELETE","INNODB_BUFFER_POOL_READS","INNODB_BUFFER_POOL_READ_REQUESTS","INNODB_BUFFER_POOL_WRITE_REQUESTS","INNODB_ROWS_INSERTED","INNODB_ROWS_DELETED","INNODB_ROWS_UPDATED","INNODB_ROWS_READ","THREADS_CREATED","THREADS_CONNECTED","THREADS_RUNNING","THREADS_CACHED","INNODB_BUFFER_POOL_PAGES_TOTAL","INNODB_BUFFER_POOL_PAGES_DATA","INNODB_BUFFER_POOL_PAGES_FREE","INNODB_BUFFER_POOL_PAGES_FLUSHED","INNODB_BUFFER_POOL_PAGES_DIRTY","INNODB_DATA_READ","INNODB_DATA_READS","INNODB_DATA_WRITES","INNODB_DATA_WRITTEN","INNODB_OS_LOG_FSYNCS","INNODB_OS_LOG_WRITTEN","CONNECTIONS","INNODB_LSN_CURRENT","INNODB_LSN_FLUSHED","INNODB_LSN_LAST_CHECKPOINT","INNODB_ROW_LOCK_TIME","INNODB_ROW_LOCK_CURRENT_WAITS","INNODB_S_LOCK_OS_WAITS","INNODB_S_LOCK_SPIN_ROUNDS","INNODB_S_LOCK_SPIN_WAITS","INNODB_X_LOCK_OS_WAITS","INNODB_X_LOCK_SPIN_ROUNDS","INNODB_X_LOCK_SPIN_WAITS","OPEN_TABLES","OPEN_FILES","OPENED_VIEWS","KEY_READS","KEY_READ_REQUESTS","KEY_WRITE_REQUESTS","KEY_WRITES","INNODB_LOG_WAITS","INNODB_LOG_WRITE_REQUESTS","INNODB_LOG_WRITES","TABLE_LOCKS_IMMEDIATE","TABLE_LOCKS_WAITED","THREADPOOL_IDLE_THREADS","THREADPOOL_THREADS","INNODB_MASTER_THREAD_ACTIVE_LOOPS","INNODB_MASTER_THREAD_IDLE_LOOPS","INNODB_MEM_TOTAL","INNODB_MEM_ADAPTIVE_HASH","INNODB_MEM_DICTIONARY","INNODB_HISTORY_LIST_LENGTH","HANDLER_COMMIT","HANDLER_ROLLBACK","HANDLER_SAVEPOINT","HANDLER_MRR_INIT","HANDLER_UPDATE","HANDLER_DELETE","HANDLER_READ_FIRST","HANDLER_READ_KEY","HANDLER_READ_NEXT","HANDLER_READ_NEXT","HANDLER_READ_PREV","HANDLER_READ_RND","HANDLER_READ_RND_NEXT","SELECT_FULL_JOIN","SELECT_FULL_RANGE_JOIN","SELECT_RANGE","SELECT_RANGE_CHECK","SELECT_SCAN","CREATED_TMP_DISK_TABLES","CREATED_TMP_TABLES","EMPTY_QUERIES","EXECUTED_EVENTS","COM_EMPTY_QUERY","EMPTY_QUERIES");'
GET_MYSQL_VARIABLES='SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES;'
GET_MYSQL_BINLOGS="SHOW MASTER LOGS;"
GET_MYSQL_PROCESSLIST='SELECT STATE  FROM INFORMATION_SCHEMA.PROCESSLIST;'
GET_MYSQL_QEURY_RESPONSE_BASE='SHOW GLOBAL VARIABLES LIKE "QUERY_RESPONSE_TIME_RANGE_BASE"'
GET_MYSQL_QUERY_RESPONSE_TIME='SELECT TIME,COUNT,TOTAL FROM INFORMATION_SCHEMA.QUERY_RESPONSE_TIME;'

SLAVE_STATUS_PERCONA_SERVER_5_6=["Slave_IO_State","Master_Host","Master_User","Master_Port","Connect_Retry","Master_Log_File","Read_Master_Log_Pos","Relay_Log_File","Relay_Log_Pos","Relay_Master_Log_File","Slave_IO_Running","Slave_SQL_Running","Replicate_Do_DB","Replicate_Ignore_DB","Replicate_Do_Table","Replicate_Ignore_Table","Replicate_Wild_Do_Table","Replicate_Wild_Ignore_Table","Last_Errno","Last_Error","Skip_Counter","Exec_Master_Log_Pos","Relay_Log_Space","Until_Condition","Until_Log_File","Until_Log_Pos","Master_SSL_Allowed","Master_SSL_CA_File","Master_SSL_CA_Path","Master_SSL_Cert","Master_SSL_Cipher","Master_SSL_Key","Seconds_Behind_Master","Master_SSL_Verify_Server_Cert","Last_IO_Errno","Last_IO_Error","Last_SQL_Errno","Last_SQL_Error","Replicate_Ignore_Server_Ids","Master_Server_Id","Master_UUID","Master_Info_File","SQL_Delay","SQL_Remaining_Delay","Slave_SQL_Running_State","Master_Retry_Count","Master_Bind","Last_IO_Error_Timestamp","Last_SQL_Error_Timestamp","Master_SSL_Crl","Master_SSL_Crlpath","Retrieved_Gtid_Set","Executed_Gtid_Set","Auto_Position"]
GET_MYSQL_SLAVE_STATUS_PERCONA_SERVER_5_6="SHOW SLAVE STATUS"


GET_STATUS_MARIADB_10 = 'SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME IN ("BYTES_SENT","BYTES_RECEIVED","COM_SELECT","COM_INSERT","COM_UPDATE","COM_DELETE","INNODB_BUFFER_POOL_READS","INNODB_BUFFER_POOL_READ_REQUESTS","INNODB_BUFFER_POOL_WRITE_REQUESTS","INNODB_ROWS_INSERTED","INNODB_ROWS_DELETED","INNODB_ROWS_UPDATED","INNODB_ROWS_READ","THREADS_CREATED","THREADS_CONNECTED","THREADS_RUNNING","THREADS_CACHED","INNODB_BUFFER_POOL_PAGES_TOTAL","INNODB_BUFFER_POOL_PAGES_DATA","INNODB_BUFFER_POOL_PAGES_FREE","INNODB_BUFFER_POOL_PAGES_FLUSHED","INNODB_BUFFER_POOL_PAGES_DIRTY","INNODB_DATA_READ","INNODB_DATA_READS","INNODB_DATA_WRITES","INNODB_DATA_WRITTEN","INNODB_OS_LOG_FSYNCS","INNODB_OS_LOG_WRITTEN","CONNECTIONS","INNODB_LSN_CURRENT","INNODB_LSN_FLUSHED","INNODB_LSN_LAST_CHECKPOINT","INNODB_ROW_LOCK_TIME","INNODB_ROW_LOCK_CURRENT_WAITS","INNODB_S_LOCK_OS_WAITS","INNODB_S_LOCK_SPIN_ROUNDS","INNODB_S_LOCK_SPIN_WAITS","INNODB_X_LOCK_OS_WAITS","INNODB_X_LOCK_SPIN_ROUNDS","INNODB_X_LOCK_SPIN_WAITS","OPEN_TABLES","OPEN_FILES","OPENED_VIEWS","KEY_READS","KEY_READ_REQUESTS","KEY_WRITE_REQUESTS","KEY_WRITES","INNODB_LOG_WAITS","INNODB_LOG_WRITE_REQUESTS","INNODB_LOG_WRITES","TABLE_LOCKS_IMMEDIATE","TABLE_LOCKS_WAITED","THREADPOOL_IDLE_THREADS","THREADPOOL_THREADS","INNODB_MASTER_THREAD_ACTIVE_LOOPS","INNODB_MASTER_THREAD_IDLE_LOOPS","INNODB_MEM_TOTAL","INNODB_MEM_ADAPTIVE_HASH","INNODB_MEM_DICTIONARY","INNODB_HISTORY_LIST_LENGTH","HANDLER_COMMIT","HANDLER_ROLLBACK","HANDLER_SAVEPOINT","HANDLER_MRR_INIT","HANDLER_UPDATE","HANDLER_DELETE","HANDLER_READ_FIRST","HANDLER_READ_KEY","HANDLER_READ_NEXT","HANDLER_READ_NEXT","HANDLER_READ_PREV","HANDLER_READ_RND","HANDLER_READ_RND_NEXT","SELECT_FULL_JOIN","SELECT_FULL_RANGE_JOIN","SELECT_RANGE","SELECT_RANGE_CHECK","SELECT_SCAN","CREATED_TMP_DISK_TABLES","CREATED_TMP_TABLES","EMPTY_QUERIES","EXECUTED_EVENTS","COM_EMPTY_QUERY","EMPTY_QUERIES");'
GET_VARIABLES_MARIADB_10 = 'SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES;'
GET_BINLOGS_MARIADB_10="SHOW MASTER LOGS;"
GET_PROCESSLIST_MARIADB_10 = 'SELECT STATE  FROM INFORMATION_SCHEMA.PROCESSLIST;'
GET_QEURY_RESPONSE_BASE_MARIADB_10 = 'SHOW GLOBAL VARIABLES LIKE "QUERY_RESPONSE_TIME_RANGE_BASE"'
GET_QUERY_RESPONSE_TIME_MARIADB_10 = "SELECT TIME,COUNT,if(TOTAL='TOO LONG',0,TOTAL)* 1000000 FROM INFORMATION_SCHEMA.QUERY_RESPONSE_TIME;"
GET_SLAVE_STATUS_MARIADB_10="SHOW ALL SLAVES STATUS"


get_response_total_time=lambda x: x == 'TOO LONG' and x  or int(x)

def get_mysql_cursor(hhost,pport,uuser,ppassword):
	while 1:
		try:
			conn = pymysql.connect(host=hhost,port=pport,user=uuser,password=ppassword)
			cursor=conn.cursor()
			break
		except Exception,e:
#			logging.error("Can't connect to mysql server")
			logging.error(e[1])
			time.sleep(10)
	return cursor
def get_mysql_version(cursor):
	try:
		cursor.execute(GET_MYSQL_VERSION)
		result=cursor.fetchall()
	except:
		return 1
	if len(result) !=2 :
		return 1
	if result[0][0] == 'VERSION_COMMENT':
		distribution=0
		version=1
	elif result[0][1] == 'VERSION_COMMENT':
		distribution=1
		version=0

	if re.search('MARIADB',result[distribution][1].upper()) and re.match('5.5.',result[version][1]):
		return 'mariadb5'
	elif re.search('MARIADB',result[distribution][1].upper()) and re.match('10.0.',result[version][1]):
		return 'mariadb10_0'
	elif re.search('MARIADB',result[distribution][1].upper()) and re.match('10.1.',result[version][1]):
		return 'mariadb10_1'
	elif re.search('PERCONA',result[distribution][1].upper()) and re.match('5.5.',result[version][1]):
		return 'percona_server5_5'
	elif re.search('PERCONA',result[distribution][1].upper()) and re.match('5.6.',result[version][1]):
		return 'percona_server5_6'
	return  1
def get_mysql_status_percona_server_5_6(cursor):
	try:
		cursor.execute(GET_MYSQL_SLAVE_STATUS_PERCNA_SERVER_5_6)
		result_response=cursor.fetchall()
		mysql_status['slave']={}
		mysql_status['slave']['Slave_IO_State','Master_Host','Master_Port','Master_User','Master_Log_File','Exec_Master_Log_Pos','Slave_IO_Running','Slave_SQL_Running','Replicate_Do_DB','Replicate_Ignore_DB','Replicate_Do_Table','Replicate_Ignore_Table','Replicate_Wild_Do_Table','Replicate_Wild_Ignore_Table','Seconds_Behind_Master']
	except:
		pass
	#mariadb_10_status
	#{
	#'status':{}
	#'binlog':{}
	#'processlist':{}
	#'response':{}	
	#'slave':{}
processlist_state=[
'cleaning up',\
'closing tables',\
'copying to tmp table',\
'copying to tmp table on disk',\
'creating sort index',\
'end',\
'executing',\
'init',\
'killed',\
'locked',\
'logging slow query',\
'login',\
'optimizing',\
'preparing',\
'removing tmp table',\
'rolling back',\
'searching rows for update',\
'sending data',\
'sorting for group',\
'sorting for order',\
'statistics',\
'updating',\
'writing_to_net',\
'sleep',\
'other'
]
def get_mysql_status_mariadb_10(cursor):
	mysql_status={}
	try:
		cursor.execute(GET_STATUS_MARIADB_10)
		result_status=cursor.fetchall()
		mysql_status['status']={}
		for i in result_status:
			mysql_status['status'][i[0]]=int(i[1])
	except:
		pass
	try:
		cursor.execute(GET_VARIABLES_MARIADB_10)
		result_variables=cursor.fetchall()
		mysql_status['variables']={}
	except:
		pass
	try:
		cursor.execute(GET_BINLOGS_MARIADB_10)
		result_binlog=cursor.fetchall()
		mysql_status['binlog']['binlog_space']=reduce(lambda x,y:x+y,[i[1] for i in result_binlog])
	except:
		pass
	try:
		cursor.execute(GET_PROCESSLIST_MARIADB_10)
		result_process=cursor.fetchall()
		processlist_count=collections.Counter(map(lambda x:x == '' and 'sleep' or x ,[i[0] for i in result_process]))
		#mysql_status['processlist']=collections.Counter(map(lambda x:x == '' and 'None' or x ,[i[0] for i in result_process]))
		mysql_status['processlist']={'other':0,'locked':0}
		for i in processlist_count.elements():
			if i.lower() in processlist_state:
				mysql_status['processlist'][i.lower()]=processlist_count[i]
			elif re.match('(Table lock|Waiting for .*lock)$',i):
				mysql_status['processlist']['lock'] = mysql_status['processlist']['lock'] +1
			else:
				mysql_status['processlist']['other'] = mysql_status['processlist']['other']+1
		for i in processlist_state:
			if i not in mysql_status['processlist']:
				mysql_status['processlist'][i]=0
	except:
		pass
	try:
		cursor.execute(GET_QEURY_RESPONSE_BASE_MARIADB_10)
		response_base=cursor.fetchall()[0][1]
		cursor.execute(GET_QUERY_RESPONSE_TIME_MARIADB_10)
		result_response=cursor.fetchall()
		mysql_status['response']={}
		mysql_status['response']['query_response_time_range_base']=response_base
		for i in result_response:
			mysql_status['response'][i[0].strip()]={}
			mysql_status['response'][i[0].strip()]['count']=int(i[1])
			mysql_status['response'][i[0].strip()]['total']=get_response_total_time(i[2])
	except :
		pass
	try:
		cursor.execute(GET_SLAVE_STATUS_MARIADB_10)
		result_response=cursor.fetchall()
		mysql_status['slave']={}
		mysql_status['']
	except:
		pass
	return mysql_status
def get_mysql_init_status(cursor):
	mysql_version = get_mysql_version(cursor)	
def out_status(sstats,rtime,queue=''):
	if isinstance(queue,multiprocessing.queues.Queue):
		queue.put(sstats)
	sys.stdout.write('%s\n'%sstats)
	sys.stdout.flush()
def get_mysql_status(server,port,user,password,queue='',interval=5):
	cursor = get_mysql_cursor(server,port,user,password)
	if cursor == 1:
		print 'error'
	tmp_before=get_mysql_status_mariadb_10(cursor)
	btime=time.time()
	time.sleep(interval)
	while 1:
		tmp_after=get_mysql_status_mariadb_10(cursor)
		atime=time.time()
		interval_time=atime-btime
		##status
		tmp_result={}
		tmp_result['status']={}
		tmp_result['status']['BYTES_SENT']=(tmp_after['status']['BYTES_SENT']-tmp_before['status']['BYTES_SENT'])/interval_time
		tmp_result['status']['BYTES_RECEIVED']=(tmp_after['status']['BYTES_RECEIVED']-tmp_before['status']['BYTES_RECEIVED'])/interval_time
		tmp_result['status']['COM_SELECT']=(tmp_after['status']['COM_SELECT']-tmp_before['status']['COM_SELECT'])/interval_time

		tmp_result['status']['COM_INSERT']=(tmp_after['status']['COM_INSERT']-tmp_before['status']['COM_INSERT'])/interval_time
		tmp_result['status']['COM_UPDATE']=(tmp_after['status']['COM_UPDATE']-tmp_before['status']['COM_UPDATE'])/interval_time
		tmp_result['status']['COM_DELETE']=(tmp_after['status']['COM_DELETE']-tmp_before['status']['COM_DELETE'])/interval_time

		tmp_result['status']['INNODB_BUFFER_POOL_READS']=(tmp_after['status']['INNODB_BUFFER_POOL_READS']-tmp_before['status']['INNODB_BUFFER_POOL_READS'])/interval_time
		tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']=(tmp_after['status']['INNODB_BUFFER_POOL_READ_REQUESTS']-tmp_before['status']['INNODB_BUFFER_POOL_READ_REQUESTS'])/interval_time
		#innodb_buffer_pool_read_hit
		#(1-INNODB_BUFFER_POOL_READS/INNODB_BUFFER_POOL_READ_REQUESTS)*100
		
		tmp_result['status']['INNODB_BUFFER_POOL_READ_HIT']=100 if tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS'] ==0 else round((tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']-tmp_result['status']['INNODB_BUFFER_POOL_READS'])/tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']*100,4)
		#round((tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']-tmp_result['status']['INNODB_BUFFER_POOL_READS'])/tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']*100,4)

		tmp_result['status']['INNODB_BUFFER_POOL_WRITE_REQUESTS']=(tmp_after['status']['INNODB_BUFFER_POOL_WRITE_REQUESTS']-tmp_before['status']['INNODB_BUFFER_POOL_WRITE_REQUESTS'])/interval_time

		tmp_result['status']['INNODB_ROWS_INSERTED']=(tmp_after['status']['INNODB_ROWS_INSERTED']-tmp_before['status']['INNODB_ROWS_INSERTED'])/interval_time
		tmp_result['status']['INNODB_ROWS_DELETED']=(tmp_after['status']['INNODB_ROWS_DELETED']-tmp_before['status']['INNODB_ROWS_DELETED'])/interval_time
		tmp_result['status']['INNODB_ROWS_UPDATED']=(tmp_after['status']['INNODB_ROWS_UPDATED']-tmp_before['status']['INNODB_ROWS_UPDATED'])/interval_time
		tmp_result['status']['INNODB_ROWS_READ']=(tmp_after['status']['INNODB_ROWS_READ']-tmp_before['status']['INNODB_ROWS_READ'])/interval_time

		tmp_result['status']['THREADS_CREATED']=(tmp_after['status']['THREADS_CREATED']-tmp_before['status']['THREADS_CREATED'])/interval_time
		tmp_result['status']['THREADS_CONNECTED']=tmp_after['status']['THREADS_CONNECTED']
		tmp_result['status']['THREADS_RUNNING']=tmp_after['status']['THREADS_RUNNING']
		tmp_result['status']['THREADS_CACHED']=tmp_after['status']['THREADS_CACHED']

		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_TOTAL']=(tmp_after['status']['INNODB_BUFFER_POOL_PAGES_TOTAL']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_TOTAL'])/interval_time
		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_DATA']=(tmp_after['status']['INNODB_BUFFER_POOL_PAGES_DATA']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_DATA'])/interval_time
		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_FREE']=(tmp_after['status']['INNODB_BUFFER_POOL_PAGES_FREE']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_FREE'])/interval_time
		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_FLUSHED']=(tmp_after['status']['INNODB_BUFFER_POOL_PAGES_FLUSHED']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_FLUSHED'])/interval_time
		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_DIRTY']=(tmp_after['status']['INNODB_BUFFER_POOL_PAGES_DIRTY']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_DIRTY'])/interval_time
		tmp_result['status']['INNODB_DATA_READ']=(tmp_after['status']['INNODB_DATA_READ']-tmp_before['status']['INNODB_DATA_READ'])/interval_time
		tmp_result['status']['INNODB_DATA_READS']=(tmp_after['status']['INNODB_DATA_READS']-tmp_before['status']['INNODB_DATA_READS'])/interval_time

		##innodb file read bytes per request
		tmp_result['status']['INNODB_DATA_READ_PER_REQUEST']=0 if tmp_result['status']['INNODB_DATA_READS'] == 0 else round(tmp_result['status']['INNODB_DATA_READ']/tmp_result['status']['INNODB_DATA_READS']/1024,4)

		tmp_result['status']['INNODB_DATA_WRITES']=(tmp_after['status']['INNODB_DATA_WRITES']-tmp_before['status']['INNODB_DATA_WRITES'])/interval_time
		tmp_result['status']['INNODB_DATA_WRITTEN']=(tmp_after['status']['INNODB_DATA_WRITTEN']-tmp_before['status']['INNODB_DATA_WRITTEN'])/interval_time

		##innodb physical write
		tmp_result['status']['INNODB_DATA_WRITE_PER_REQUEST']=0 if tmp_result['status']['INNODB_DATA_WRITTEN'] == 0 else round(tmp_result['status']['INNODB_DATA_WRITES']/tmp_result['status']['INNODB_DATA_WRITTEN']/1024/interval_time,4)

		tmp_result['status']['INNODB_OS_LOG_FSYNCS']=(tmp_after['status']['INNODB_OS_LOG_FSYNCS']-tmp_before['status']['INNODB_OS_LOG_FSYNCS'])/interval_time
		tmp_result['status']['INNODB_OS_LOG_WRITTEN']=(tmp_after['status']['INNODB_OS_LOG_WRITTEN']-tmp_before['status']['INNODB_OS_LOG_WRITTEN'])/interval_time

		tmp_result['status']['CONNECTIONS']=(tmp_after['status']['CONNECTIONS']-tmp_before['status']['CONNECTIONS'])/interval_time

		tmp_result['status']['INNODB_LSN_CURRENT']=(tmp_after['status']['INNODB_LSN_CURRENT']-tmp_before['status']['INNODB_LSN_CURRENT'])/interval_time
		tmp_result['status']['INNODB_LSN_FLUSHED']=tmp_after['status']['INNODB_LSN_FLUSHED']  #-tmp_before['status']['INNODB_LSN_FLUSHED']
		tmp_result['status']['INNODB_LSN_LAST_CHECKPOINT']=tmp_after['status']['INNODB_LSN_LAST_CHECKPOINT']  #-tmp_before['status']['INNODB_LSN_LAST_CHECKPOINT']

		##LSN unflushed
		tmp_result['status']['LSN_UNFLUSHED']=tmp_result['status']['INNODB_LSN_CURRENT']-tmp_result['status']['INNODB_LSN_FLUSHED']
		##LSN uncheckpoint
		tmp_result['status']['LSN_UNCHECKPOINT']=tmp_result['status']['INNODB_LSN_FLUSHED']-tmp_result['status']['INNODB_LSN_LAST_CHECKPOINT']

		tmp_result['status']['INNODB_ROW_LOCK_TIME']=(tmp_after['status']['INNODB_ROW_LOCK_TIME']-tmp_before['status']['INNODB_ROW_LOCK_TIME'])/interval_time
		tmp_result['status']['INNODB_ROW_LOCK_CURRENT_WAITS']=(tmp_after['status']['INNODB_ROW_LOCK_CURRENT_WAITS']-tmp_before['status']['INNODB_ROW_LOCK_CURRENT_WAITS'])/interval_time
		tmp_result['status']['INNODB_S_LOCK_OS_WAITS']=(tmp_after['status']['INNODB_S_LOCK_OS_WAITS']-tmp_before['status']['INNODB_S_LOCK_OS_WAITS'])/interval_time
		tmp_result['status']['INNODB_S_LOCK_SPIN_ROUNDS']=(tmp_after['status']['INNODB_S_LOCK_SPIN_ROUNDS']-tmp_before['status']['INNODB_S_LOCK_SPIN_ROUNDS'])/interval_time
		tmp_result['status']['INNODB_S_LOCK_SPIN_WAITS']=(tmp_after['status']['INNODB_S_LOCK_SPIN_WAITS']-tmp_before['status']['INNODB_S_LOCK_SPIN_WAITS'])/interval_time
		tmp_result['status']['INNODB_X_LOCK_OS_WAITS']=(tmp_after['status']['INNODB_X_LOCK_OS_WAITS']-tmp_before['status']['INNODB_X_LOCK_OS_WAITS'])/interval_time
		tmp_result['status']['INNODB_X_LOCK_SPIN_ROUNDS']=(tmp_after['status']['INNODB_X_LOCK_SPIN_ROUNDS']-tmp_before['status']['INNODB_X_LOCK_SPIN_ROUNDS'])/interval_time
		tmp_result['status']['INNODB_X_LOCK_SPIN_WAITS']=(tmp_after['status']['INNODB_X_LOCK_SPIN_WAITS']-tmp_before['status']['INNODB_X_LOCK_SPIN_WAITS'])/interval_time

		tmp_result['status']['OPEN_TABLES']=(tmp_after['status']['OPEN_TABLES']-tmp_before['status']['OPEN_TABLES'])/interval_time
		tmp_result['status']['OPEN_FILES']=(tmp_after['status']['OPEN_FILES']-tmp_before['status']['OPEN_FILES'])/interval_time
		tmp_result['status']['OPENED_VIEWS']=(tmp_after['status']['OPENED_VIEWS']-tmp_before['status']['OPENED_VIEWS'])/interval_time

		tmp_result['status']['KEY_READS']=(tmp_after['status']['KEY_READS']-tmp_before['status']['KEY_READS'])/interval_time
		tmp_result['status']['KEY_READ_REQUESTS']=(tmp_after['status']['KEY_READ_REQUESTS']-tmp_before['status']['KEY_READ_REQUESTS'])/interval_time
		tmp_result['status']['KEY_WRITE_REQUESTS']=(tmp_after['status']['KEY_WRITE_REQUESTS']-tmp_before['status']['KEY_WRITE_REQUESTS'])/interval_time
		tmp_result['status']['KEY_WRITES']=(tmp_after['status']['KEY_WRITES']-tmp_before['status']['KEY_WRITES'])/interval_time

		tmp_result['status']['INNODB_LOG_WAITS']=(tmp_after['status']['INNODB_LOG_WAITS']-tmp_before['status']['INNODB_LOG_WAITS'])/interval_time
		tmp_result['status']['INNODB_LOG_WRITE_REQUESTS']=(tmp_after['status']['INNODB_LOG_WRITE_REQUESTS']-tmp_before['status']['INNODB_LOG_WRITE_REQUESTS'])/interval_time
		tmp_result['status']['INNODB_LOG_WRITES']=(tmp_after['status']['INNODB_LOG_WRITES']-tmp_before['status']['INNODB_LOG_WRITES'])/interval_time

		tmp_result['status']['TABLE_LOCKS_IMMEDIATE']=(tmp_after['status']['TABLE_LOCKS_IMMEDIATE']-tmp_before['status']['TABLE_LOCKS_IMMEDIATE'])/interval_time
		tmp_result['status']['TABLE_LOCKS_WAITED']=(tmp_after['status']['TABLE_LOCKS_WAITED']-tmp_before['status']['TABLE_LOCKS_WAITED'])/interval_time

		tmp_result['status']['THREADPOOL_IDLE_THREADS']=tmp_after['status']['THREADPOOL_IDLE_THREADS']-tmp_before['status']['THREADPOOL_IDLE_THREADS']
		tmp_result['status']['THREADPOOL_THREADS']=tmp_after['status']['THREADPOOL_THREADS']-tmp_before['status']['THREADPOOL_THREADS']

		tmp_result['status']['INNODB_MASTER_THREAD_ACTIVE_LOOPS']=(tmp_after['status']['INNODB_MASTER_THREAD_ACTIVE_LOOPS']-tmp_before['status']['INNODB_MASTER_THREAD_ACTIVE_LOOPS'])/interval_time
		tmp_result['status']['INNODB_MASTER_THREAD_IDLE_LOOPS']=(tmp_after['status']['INNODB_MASTER_THREAD_IDLE_LOOPS']-tmp_before['status']['INNODB_MASTER_THREAD_IDLE_LOOPS'])/interval_time

		tmp_result['status']['INNODB_MEM_TOTAL']=(tmp_after['status']['INNODB_MEM_TOTAL']-tmp_before['status']['INNODB_MEM_TOTAL'])/interval_time
		tmp_result['status']['INNODB_MEM_ADAPTIVE_HASH']=(tmp_after['status']['INNODB_MEM_ADAPTIVE_HASH']-tmp_before['status']['INNODB_MEM_ADAPTIVE_HASH'])/interval_time
		tmp_result['status']['INNODB_MEM_DICTIONARY']=(tmp_after['status']['INNODB_MEM_DICTIONARY']-tmp_before['status']['INNODB_MEM_DICTIONARY'])/interval_time
		tmp_result['status']['INNODB_HISTORY_LIST_LENGTH']=(tmp_after['status']['INNODB_HISTORY_LIST_LENGTH']-tmp_before['status']['INNODB_HISTORY_LIST_LENGTH'])/interval_time
		tmp_result['status']['HANDLER_COMMIT']=(tmp_after['status']['HANDLER_COMMIT']-tmp_before['status']['HANDLER_COMMIT'])/interval_time
		tmp_result['status']['HANDLER_ROLLBACK']=(tmp_after['status']['HANDLER_ROLLBACK']-tmp_before['status']['HANDLER_ROLLBACK'])/interval_time
		tmp_result['status']['HANDLER_SAVEPOINT']=(tmp_after['status']['HANDLER_SAVEPOINT']-tmp_before['status']['HANDLER_SAVEPOINT'])/interval_time
		tmp_result['status']['HANDLER_MRR_INIT']=(tmp_after['status']['HANDLER_MRR_INIT']-tmp_before['status']['HANDLER_MRR_INIT'])/interval_time
		tmp_result['status']['HANDLER_UPDATE']=(tmp_after['status']['HANDLER_UPDATE']-tmp_before['status']['HANDLER_UPDATE'])/interval_time
		tmp_result['status']['HANDLER_DELETE']=(tmp_after['status']['HANDLER_DELETE']-tmp_before['status']['HANDLER_DELETE'])/interval_time
		tmp_result['status']['HANDLER_READ_FIRST']=(tmp_after['status']['HANDLER_READ_FIRST']-tmp_before['status']['HANDLER_READ_FIRST'])/interval_time
		tmp_result['status']['HANDLER_READ_KEY']=(tmp_after['status']['HANDLER_READ_KEY']-tmp_before['status']['HANDLER_READ_KEY'])/interval_time
		tmp_result['status']['HANDLER_READ_NEXT']=(tmp_after['status']['HANDLER_READ_NEXT']-tmp_before['status']['HANDLER_READ_NEXT'])/interval_time
		tmp_result['status']['HANDLER_READ_PREV']=(tmp_after['status']['HANDLER_READ_PREV']-tmp_before['status']['HANDLER_READ_PREV'])/interval_time
		tmp_result['status']['HANDLER_READ_RND']=(tmp_after['status']['HANDLER_READ_RND']-tmp_before['status']['HANDLER_READ_RND'])/interval_time
		tmp_result['status']['HANDLER_READ_RND_NEXT']=(tmp_after['status']['HANDLER_READ_RND_NEXT']-tmp_before['status']['HANDLER_READ_RND_NEXT'])/interval_time

		tmp_result['status']['SELECT_FULL_JOIN']=(tmp_after['status']['SELECT_FULL_JOIN']-tmp_before['status']['SELECT_FULL_JOIN'])/interval_time
		tmp_result['status']['SELECT_FULL_RANGE_JOIN']=(tmp_after['status']['SELECT_FULL_RANGE_JOIN']-tmp_before['status']['SELECT_FULL_RANGE_JOIN'])/interval_time
		tmp_result['status']['SELECT_RANGE']=(tmp_after['status']['SELECT_RANGE']-tmp_before['status']['SELECT_RANGE'])/interval_time
		tmp_result['status']['SELECT_RANGE_CHECK']=(tmp_after['status']['SELECT_RANGE_CHECK']-tmp_before['status']['SELECT_RANGE_CHECK'])/interval_time
		tmp_result['status']['SELECT_SCAN']=(tmp_after['status']['SELECT_SCAN']-tmp_before['status']['SELECT_SCAN'])/interval_time

		tmp_result['status']['CREATED_TMP_DISK_TABLES']=(tmp_after['status']['CREATED_TMP_DISK_TABLES']-tmp_before['status']['CREATED_TMP_DISK_TABLES'])/interval_time
		tmp_result['status']['CREATED_TMP_TABLES']=(tmp_after['status']['CREATED_TMP_TABLES']-tmp_before['status']['CREATED_TMP_TABLES'])/interval_time

		tmp_result['status']['EMPTY_QUERIES']=(tmp_after['status']['EMPTY_QUERIES']-tmp_before['status']['EMPTY_QUERIES'])/interval_time
		tmp_result['status']['EXECUTED_EVENTS']=(tmp_after['status']['EXECUTED_EVENTS']-tmp_before['status']['EXECUTED_EVENTS'])/interval_time
		tmp_result['status']['COM_EMPTY_QUERY']=(tmp_after['status']['COM_EMPTY_QUERY']-tmp_before['status']['COM_EMPTY_QUERY'])/interval_time
		tmp_result['status']['EMPTY_QUERIES']=(tmp_after['status']['EMPTY_QUERIES']-tmp_before['status']['EMPTY_QUERIES'])/interval_time

		##variables
		tmp_result['variables']=tmp_after['variables']


		##processlist
		tmp_result['processlist']=tmp_after['processlist']
		
		##response
		tmp_result['response']={}
		if tmp_before['response']['query_response_time_range_base'] == '10' and tmp_before['response']['query_response_time_range_base'] == tmp_after['response']['query_response_time_range_base']:
			tmp_result['response']['0.000001']={}
			tmp_result['response']['0.000010']={}
			tmp_result['response']['0.000100']={}
			tmp_result['response']['0.001000']={}
			tmp_result['response']['0.010000']={}
			tmp_result['response']['0.100000']={}
			tmp_result['response']['1.000000']={}
			tmp_result['response']['10.000000']={}
			tmp_result['response']['100.000000']={}
			tmp_result['response']['1000.000000']={}
			tmp_result['response']['10000.000000']={}
			tmp_result['response']['100000.000000']={}
			tmp_result['response']['1000000.000000']={}
			tmp_result['response']['TOO LONG']={}

			tmp_result['response']['0.000001']['total']=tmp_after['response']['0.000001']['total']-tmp_before['response']['0.000001']['total']
			tmp_result['response']['0.000010']['total']=tmp_after['response']['0.000010']['total']-tmp_before['response']['0.000010']['total']
			tmp_result['response']['0.000100']['total']=tmp_after['response']['0.000100']['total']-tmp_before['response']['0.000100']['total']
			tmp_result['response']['0.001000']['total']=tmp_after['response']['0.001000']['total']-tmp_before['response']['0.001000']['total']
			tmp_result['response']['0.010000']['total']=tmp_after['response']['0.010000']['total']-tmp_before['response']['0.010000']['total']
			tmp_result['response']['0.100000']['total']=tmp_after['response']['0.100000']['total']-tmp_before['response']['0.100000']['total']
			tmp_result['response']['1.000000']['total']=tmp_after['response']['1.000000']['total']-tmp_before['response']['1.000000']['total']
			tmp_result['response']['10.000000']['total']=tmp_after['response']['10.000000']['total']-tmp_before['response']['10.000000']['total']
			tmp_result['response']['100.000000']['total']=tmp_after['response']['100.000000']['total']-tmp_before['response']['100.000000']['total']
			tmp_result['response']['1000.000000']['total']=tmp_after['response']['1000.000000']['total']-tmp_before['response']['1000.000000']['total']
			tmp_result['response']['10000.000000']['total']=tmp_after['response']['10000.000000']['total']-tmp_before['response']['10000.000000']['total']
			tmp_result['response']['100000.000000']['total']=tmp_after['response']['100000.000000']['total']-tmp_before['response']['100000.000000']['total']
			tmp_result['response']['1000000.000000']['total']=tmp_after['response']['1000000.000000']['total']-tmp_before['response']['1000000.000000']['total']
			tmp_result['response']['TOO LONG']['total']=0

			tmp_result['response']['0.000001']['count']=tmp_after['response']['0.000001']['count']-tmp_before['response']['0.000001']['count']
			tmp_result['response']['0.000010']['count']=tmp_after['response']['0.000010']['count']-tmp_before['response']['0.000010']['count']
			tmp_result['response']['0.000100']['count']=tmp_after['response']['0.000100']['count']-tmp_before['response']['0.000100']['count']
			tmp_result['response']['0.001000']['count']=tmp_after['response']['0.001000']['count']-tmp_before['response']['0.001000']['count']
			tmp_result['response']['0.010000']['count']=tmp_after['response']['0.010000']['count']-tmp_before['response']['0.010000']['count']
			tmp_result['response']['0.100000']['count']=tmp_after['response']['0.100000']['count']-tmp_before['response']['0.100000']['count']
			tmp_result['response']['1.000000']['count']=tmp_after['response']['1.000000']['count']-tmp_before['response']['1.000000']['count']
			tmp_result['response']['10.000000']['count']=tmp_after['response']['10.000000']['count']-tmp_before['response']['10.000000']['count']
			tmp_result['response']['100.000000']['count']=tmp_after['response']['100.000000']['count']-tmp_before['response']['100.000000']['count']
			tmp_result['response']['1000.000000']['count']=tmp_after['response']['1000.000000']['count']-tmp_before['response']['1000.000000']['count']
			tmp_result['response']['10000.000000']['count']=tmp_after['response']['10000.000000']['count']-tmp_before['response']['10000.000000']['count']
			tmp_result['response']['100000.000000']['count']=tmp_after['response']['100000.000000']['count']-tmp_before['response']['100000.000000']['count']
			tmp_result['response']['1000000.000000']['count']=tmp_after['response']['1000000.000000']['count']-tmp_before['response']['1000000.000000']['count']
			tmp_result['response']['TOO LONG']['count']=tmp_after['response']['TOO LONG']['count']-tmp_before['response']['TOO LONG']['count']
			
			tmp_result['response']['query_response_time_ninety_five_percent'],tmp_result['response']['query_response_time_avg'],total_count=util.get_some_percent(tmp_result['response'],FIELD.NINETY_FIVE_PERCENT)

			tmp_result['response']['0.000001']['percent']        = round(float(tmp_result['response']['0.000001']['count'])/total_count,5)
			tmp_result['response']['0.000010']['percent']        = round(float(tmp_result['response']['0.000010']['count'])/total_count,5)
			tmp_result['response']['0.000100']['percent']        = round(float(tmp_result['response']['0.000100']['count'])/total_count,5)
			tmp_result['response']['0.001000']['percent']        = round(float(tmp_result['response']['0.001000']['count'])/total_count,5)
			tmp_result['response']['0.010000']['percent']        = round(float(tmp_result['response']['0.010000']['count'])/total_count,5)
			tmp_result['response']['0.100000']['percent']        = round(float(tmp_result['response']['0.100000']['count'])/total_count,5)
			tmp_result['response']['1.000000']['percent']        = round(float(tmp_result['response']['1.000000']['count'])/total_count,5)
			tmp_result['response']['10.000000']['percent']       = round(float(tmp_result['response']['10.000000']['count'])/total_count,5)
			tmp_result['response']['100.000000']['percent']      = round(float(tmp_result['response']['100.000000']['count'])/total_count,5)
			tmp_result['response']['1000.000000']['percent']     = round(float(tmp_result['response']['1000.000000']['count'])/total_count,5)
			tmp_result['response']['10000.000000']['percent']    = round(float(tmp_result['response']['10000.000000']['count'])/total_count,5)
			tmp_result['response']['100000.000000']['percent']   = round(float(tmp_result['response']['100000.000000']['count'])/total_count,5)
			tmp_result['response']['1000000.000000']['percent']  = round(float(tmp_result['response']['1000000.000000']['count'])/total_count,5)
			tmp_result['response']['TOO LONG']['percent']        = round(float(tmp_result['response']['TOO LONG']['count'] )/total_count,5)
		
#		else:
#			if len(tmp_before['response'])!= len(tmp_after['response']):
#				pass
#			else:
#				pass
#		tmp_result['response']['query_response_time_ninety_five_percent'],tmp_result['response']['query_response_time_avg'],total_count=util.get_some_percent(tmp_result['response'],FIELD.NINETY_FIVE_PERCENT)

		out_status(tmp_result,atime,queue)
		#return tmp_result
		tmp_before=tmp_after
		time.sleep(interval)


if __name__ == '__main__':
	get_mysql_status('127.0.0.1',3306,'root','',queue='',interval=5)
#	cursor = get_mysql_cursor('127.0.0.1',3306,'root','')
#	if cursor == 1:
#		print 'error'
#	mysql_version = get_mysql_version(cursor)	
#	print mysql_version
#	tmp_before=get_mysql_status_mariadb_10(cursor)
#	time.sleep(5)
#	while 1:
#		tmp_after=get_mysql_status_mariadb_10(cursor)
#		##status
#		tmp_result={}
#		tmp_result['status']={}
#		tmp_result['status']['BYTES_SENT']=tmp_after['status']['BYTES_SENT']-tmp_before['status']['BYTES_SENT']
#		tmp_result['status']['BYTES_RECEIVED']=tmp_after['status']['BYTES_RECEIVED']-tmp_before['status']['BYTES_RECEIVED']
#		tmp_result['status']['COM_SELECT']=tmp_after['status']['COM_SELECT']-tmp_before['status']['COM_SELECT']
#
#		tmp_result['status']['COM_INSERT']=tmp_after['status']['COM_INSERT']-tmp_before['status']['COM_INSERT']
#		tmp_result['status']['COM_UPDATE']=tmp_after['status']['COM_UPDATE']-tmp_before['status']['COM_UPDATE']
#		tmp_result['status']['COM_DELETE']=tmp_after['status']['COM_DELETE']-tmp_before['status']['COM_DELETE']
#
#		tmp_result['status']['INNODB_BUFFER_POOL_READS']=tmp_after['status']['INNODB_BUFFER_POOL_READS']-tmp_before['status']['INNODB_BUFFER_POOL_READS']
#		tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']=tmp_after['status']['INNODB_BUFFER_POOL_READ_REQUESTS']-tmp_before['status']['INNODB_BUFFER_POOL_READ_REQUESTS']
#		#innodb_buffer_pool_read_hit
#		#(1-INNODB_BUFFER_POOL_READS/INNODB_BUFFER_POOL_READ_REQUESTS)*100
#		
#		tmp_result['status']['INNODB_BUFFER_POOL_READ_HIT']=100 if tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS'] ==0 else round((tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']-tmp_result['status']['INNODB_BUFFER_POOL_READS'])/tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']*100,4)
#		#round((tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']-tmp_result['status']['INNODB_BUFFER_POOL_READS'])/tmp_result['status']['INNODB_BUFFER_POOL_READ_REQUESTS']*100,4)
#
#		tmp_result['status']['INNODB_BUFFER_POOL_WRITE_REQUESTS']=tmp_after['status']['INNODB_BUFFER_POOL_WRITE_REQUESTS']-tmp_before['status']['INNODB_BUFFER_POOL_WRITE_REQUESTS']
#
#		tmp_result['status']['INNODB_ROWS_INSERTED']=tmp_after['status']['INNODB_ROWS_INSERTED']-tmp_before['status']['INNODB_ROWS_INSERTED']
#		tmp_result['status']['INNODB_ROWS_DELETED']=tmp_after['status']['INNODB_ROWS_DELETED']-tmp_before['status']['INNODB_ROWS_DELETED']
#		tmp_result['status']['INNODB_ROWS_UPDATED']=tmp_after['status']['INNODB_ROWS_UPDATED']-tmp_before['status']['INNODB_ROWS_UPDATED']
#		tmp_result['status']['INNODB_ROWS_READ']=tmp_after['status']['INNODB_ROWS_READ']-tmp_before['status']['INNODB_ROWS_READ']
#
#		tmp_result['status']['THREADS_CREATED']=tmp_after['status']['THREADS_CREATED']-tmp_before['status']['THREADS_CREATED']
#		tmp_result['status']['THREADS_CONNECTED']=tmp_after['status']['THREADS_CONNECTED']-tmp_before['status']['THREADS_CONNECTED']
#		tmp_result['status']['THREADS_RUNNING']=tmp_after['status']['THREADS_RUNNING']-tmp_before['status']['THREADS_RUNNING']
#		tmp_result['status']['THREADS_CACHED']=tmp_after['status']['THREADS_CACHED']-tmp_before['status']['THREADS_CACHED']
#
#		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_TOTAL']=tmp_after['status']['INNODB_BUFFER_POOL_PAGES_TOTAL']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_TOTAL']
#		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_DATA']=tmp_after['status']['INNODB_BUFFER_POOL_PAGES_DATA']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_DATA']
#		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_FREE']=tmp_after['status']['INNODB_BUFFER_POOL_PAGES_FREE']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_FREE']
#		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_FLUSHED']=tmp_after['status']['INNODB_BUFFER_POOL_PAGES_FLUSHED']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_FLUSHED']
#		tmp_result['status']['INNODB_BUFFER_POOL_PAGES_DIRTY']=tmp_after['status']['INNODB_BUFFER_POOL_PAGES_DIRTY']-tmp_before['status']['INNODB_BUFFER_POOL_PAGES_DIRTY']
#		tmp_result['status']['INNODB_DATA_READ']=tmp_after['status']['INNODB_DATA_READ']-tmp_before['status']['INNODB_DATA_READ']
#		tmp_result['status']['INNODB_DATA_READS']=tmp_after['status']['INNODB_DATA_READS']-tmp_before['status']['INNODB_DATA_READS']
#
#		##innodb file read bytes per request
#		tmp_result['status']['INNODB_DATA_READ_PER_REQUEST']=0 if tmp_result['status']['INNODB_DATA_READS'] == 0 else round(tmp_result['status']['INNODB_DATA_READ']/tmp_result['status']['INNODB_DATA_READS']/1024,4)
#
#		tmp_result['status']['INNODB_DATA_WRITES']=tmp_after['status']['INNODB_DATA_WRITES']-tmp_before['status']['INNODB_DATA_WRITES']
#		tmp_result['status']['INNODB_DATA_WRITTEN']=tmp_after['status']['INNODB_DATA_WRITTEN']-tmp_before['status']['INNODB_DATA_WRITTEN']
#
#		##innodb physical write
#		tmp_result['status']['INNODB_DATA_WRITE_PER_REQUEST']=0 if tmp_result['status']['INNODB_DATA_WRITTEN'] == 0 else round(tmp_result['status']['INNODB_DATA_WRITES']/tmp_result['status']['INNODB_DATA_WRITTEN']/1024,4)
#
#		tmp_result['status']['INNODB_OS_LOG_FSYNCS']=tmp_after['status']['INNODB_OS_LOG_FSYNCS']-tmp_before['status']['INNODB_OS_LOG_FSYNCS']
#		tmp_result['status']['INNODB_OS_LOG_WRITTEN']=tmp_after['status']['INNODB_OS_LOG_WRITTEN']-tmp_before['status']['INNODB_OS_LOG_WRITTEN']
#
#		tmp_result['status']['CONNECTIONS']=tmp_after['status']['CONNECTIONS']-tmp_before['status']['CONNECTIONS']
#
#		tmp_result['status']['INNODB_LSN_CURRENT']=tmp_after['status']['INNODB_LSN_CURRENT']-tmp_before['status']['INNODB_LSN_CURRENT']
#		tmp_result['status']['INNODB_LSN_FLUSHED']=tmp_after['status']['INNODB_LSN_FLUSHED']-tmp_before['status']['INNODB_LSN_FLUSHED']
#		tmp_result['status']['INNODB_LSN_LAST_CHECKPOINT']=tmp_after['status']['INNODB_LSN_LAST_CHECKPOINT']-tmp_before['status']['INNODB_LSN_LAST_CHECKPOINT']
#
#		##LSN unflushed
#		tmp_result['status']['LSN_UNFLUSHED']=tmp_result['status']['INNODB_LSN_CURRENT']-tmp_result['status']['INNODB_LSN_FLUSHED']
#		##LSN uncheckpoint
#		tmp_result['status']['LSN_UNCHECKPOINT']=tmp_result['status']['INNODB_LSN_FLUSHED']-tmp_result['status']['INNODB_LSN_LAST_CHECKPOINT']
#
#		tmp_result['status']['INNODB_ROW_LOCK_TIME']=tmp_after['status']['INNODB_ROW_LOCK_TIME']-tmp_before['status']['INNODB_ROW_LOCK_TIME']
#		tmp_result['status']['INNODB_ROW_LOCK_CURRENT_WAITS']=tmp_after['status']['INNODB_ROW_LOCK_CURRENT_WAITS']-tmp_before['status']['INNODB_ROW_LOCK_CURRENT_WAITS']
#		tmp_result['status']['INNODB_S_LOCK_OS_WAITS']=tmp_after['status']['INNODB_S_LOCK_OS_WAITS']-tmp_before['status']['INNODB_S_LOCK_OS_WAITS']
#		tmp_result['status']['INNODB_S_LOCK_SPIN_ROUNDS']=tmp_after['status']['INNODB_S_LOCK_SPIN_ROUNDS']-tmp_before['status']['INNODB_S_LOCK_SPIN_ROUNDS']
#		tmp_result['status']['INNODB_S_LOCK_SPIN_WAITS']=tmp_after['status']['INNODB_S_LOCK_SPIN_WAITS']-tmp_before['status']['INNODB_S_LOCK_SPIN_WAITS']
#		tmp_result['status']['INNODB_X_LOCK_OS_WAITS']=tmp_after['status']['INNODB_X_LOCK_OS_WAITS']-tmp_before['status']['INNODB_X_LOCK_OS_WAITS']
#		tmp_result['status']['INNODB_X_LOCK_SPIN_ROUNDS']=tmp_after['status']['INNODB_X_LOCK_SPIN_ROUNDS']-tmp_before['status']['INNODB_X_LOCK_SPIN_ROUNDS']
#		tmp_result['status']['INNODB_X_LOCK_SPIN_WAITS']=tmp_after['status']['INNODB_X_LOCK_SPIN_WAITS']-tmp_before['status']['INNODB_X_LOCK_SPIN_WAITS']
#
#		tmp_result['status']['OPEN_TABLES']=tmp_after['status']['OPEN_TABLES']-tmp_before['status']['OPEN_TABLES']
#		tmp_result['status']['OPEN_FILES']=tmp_after['status']['OPEN_FILES']-tmp_before['status']['OPEN_FILES']
#		tmp_result['status']['OPENED_VIEWS']=tmp_after['status']['OPENED_VIEWS']-tmp_before['status']['OPENED_VIEWS']
#
#		tmp_result['status']['KEY_READS']=tmp_after['status']['KEY_READS']-tmp_before['status']['KEY_READS']
#		tmp_result['status']['KEY_READ_REQUESTS']=tmp_after['status']['KEY_READ_REQUESTS']-tmp_before['status']['KEY_READ_REQUESTS']
#		tmp_result['status']['KEY_WRITE_REQUESTS']=tmp_after['status']['KEY_WRITE_REQUESTS']-tmp_before['status']['KEY_WRITE_REQUESTS']
#		tmp_result['status']['KEY_WRITES']=tmp_after['status']['KEY_WRITES']-tmp_before['status']['KEY_WRITES']
#
#		tmp_result['status']['INNODB_LOG_WAITS']=tmp_after['status']['INNODB_LOG_WAITS']-tmp_before['status']['INNODB_LOG_WAITS']
#		tmp_result['status']['INNODB_LOG_WRITE_REQUESTS']=tmp_after['status']['INNODB_LOG_WRITE_REQUESTS']-tmp_before['status']['INNODB_LOG_WRITE_REQUESTS']
#		tmp_result['status']['INNODB_LOG_WRITES']=tmp_after['status']['INNODB_LOG_WRITES']-tmp_before['status']['INNODB_LOG_WRITES']
#
#		tmp_result['status']['TABLE_LOCKS_IMMEDIATE']=tmp_after['status']['TABLE_LOCKS_IMMEDIATE']-tmp_before['status']['TABLE_LOCKS_IMMEDIATE']
#		tmp_result['status']['TABLE_LOCKS_WAITED']=tmp_after['status']['TABLE_LOCKS_WAITED']-tmp_before['status']['TABLE_LOCKS_WAITED']
#
#		tmp_result['status']['THREADPOOL_IDLE_THREADS']=tmp_after['status']['THREADPOOL_IDLE_THREADS']-tmp_before['status']['THREADPOOL_IDLE_THREADS']
#		tmp_result['status']['THREADPOOL_THREADS']=tmp_after['status']['THREADPOOL_THREADS']-tmp_before['status']['THREADPOOL_THREADS']
#
#		tmp_result['status']['INNODB_MASTER_THREAD_ACTIVE_LOOPS']=tmp_after['status']['INNODB_MASTER_THREAD_ACTIVE_LOOPS']-tmp_before['status']['INNODB_MASTER_THREAD_ACTIVE_LOOPS']
#		tmp_result['status']['INNODB_MASTER_THREAD_IDLE_LOOPS']=tmp_after['status']['INNODB_MASTER_THREAD_IDLE_LOOPS']-tmp_before['status']['INNODB_MASTER_THREAD_IDLE_LOOPS']
#
#		tmp_result['status']['INNODB_MEM_TOTAL']=tmp_after['status']['INNODB_MEM_TOTAL']-tmp_before['status']['INNODB_MEM_TOTAL']
#		tmp_result['status']['INNODB_MEM_ADAPTIVE_HASH']=tmp_after['status']['INNODB_MEM_ADAPTIVE_HASH']-tmp_before['status']['INNODB_MEM_ADAPTIVE_HASH']
#		tmp_result['status']['INNODB_MEM_DICTIONARY']=tmp_after['status']['INNODB_MEM_DICTIONARY']-tmp_before['status']['INNODB_MEM_DICTIONARY']
#		tmp_result['status']['INNODB_HISTORY_LIST_LENGTH']=tmp_after['status']['INNODB_HISTORY_LIST_LENGTH']-tmp_before['status']['INNODB_HISTORY_LIST_LENGTH']
#		tmp_result['status']['HANDLER_COMMIT']=tmp_after['status']['HANDLER_COMMIT']-tmp_before['status']['HANDLER_COMMIT']
#		tmp_result['status']['HANDLER_ROLLBACK']=tmp_after['status']['HANDLER_ROLLBACK']-tmp_before['status']['HANDLER_ROLLBACK']
#		tmp_result['status']['HANDLER_SAVEPOINT']=tmp_after['status']['HANDLER_SAVEPOINT']-tmp_before['status']['HANDLER_SAVEPOINT']
#		tmp_result['status']['HANDLER_MRR_INIT']=tmp_after['status']['HANDLER_MRR_INIT']-tmp_before['status']['HANDLER_MRR_INIT']
#		tmp_result['status']['HANDLER_UPDATE']=tmp_after['status']['HANDLER_UPDATE']-tmp_before['status']['HANDLER_UPDATE']
#		tmp_result['status']['HANDLER_DELETE']=tmp_after['status']['HANDLER_DELETE']-tmp_before['status']['HANDLER_DELETE']
#		tmp_result['status']['HANDLER_READ_FIRST']=tmp_after['status']['HANDLER_READ_FIRST']-tmp_before['status']['HANDLER_READ_FIRST']
#		tmp_result['status']['HANDLER_READ_KEY']=tmp_after['status']['HANDLER_READ_KEY']-tmp_before['status']['HANDLER_READ_KEY']
#		tmp_result['status']['HANDLER_READ_NEXT']=tmp_after['status']['HANDLER_READ_NEXT']-tmp_before['status']['HANDLER_READ_NEXT']
#		tmp_result['status']['HANDLER_READ_NEXT']=tmp_after['status']['HANDLER_READ_NEXT']-tmp_before['status']['HANDLER_READ_NEXT']
#		tmp_result['status']['HANDLER_READ_PREV']=tmp_after['status']['HANDLER_READ_PREV']-tmp_before['status']['HANDLER_READ_PREV']
#		tmp_result['status']['HANDLER_READ_RND']=tmp_after['status']['HANDLER_READ_RND']-tmp_before['status']['HANDLER_READ_RND']
#		tmp_result['status']['HANDLER_READ_RND_NEXT']=tmp_after['status']['HANDLER_READ_RND_NEXT']-tmp_before['status']['HANDLER_READ_RND_NEXT']
#
#		tmp_result['status']['SELECT_FULL_JOIN']=tmp_after['status']['SELECT_FULL_JOIN']-tmp_before['status']['SELECT_FULL_JOIN']
#		tmp_result['status']['SELECT_FULL_RANGE_JOIN']=tmp_after['status']['SELECT_FULL_RANGE_JOIN']-tmp_before['status']['SELECT_FULL_RANGE_JOIN']
#		tmp_result['status']['SELECT_RANGE']=tmp_after['status']['SELECT_RANGE']-tmp_before['status']['SELECT_RANGE']
#		tmp_result['status']['SELECT_RANGE_CHECK']=tmp_after['status']['SELECT_RANGE_CHECK']-tmp_before['status']['SELECT_RANGE_CHECK']
#		tmp_result['status']['SELECT_SCAN']=tmp_after['status']['SELECT_SCAN']-tmp_before['status']['SELECT_SCAN']
#
#		tmp_result['status']['CREATED_TMP_DISK_TABLES']=tmp_after['status']['CREATED_TMP_DISK_TABLES']-tmp_before['status']['CREATED_TMP_DISK_TABLES']
#		tmp_result['status']['CREATED_TMP_TABLES']=tmp_after['status']['CREATED_TMP_TABLES']-tmp_before['status']['CREATED_TMP_TABLES']
#
#		tmp_result['status']['EMPTY_QUERIES']=tmp_after['status']['EMPTY_QUERIES']-tmp_before['status']['EMPTY_QUERIES']
#		tmp_result['status']['EXECUTED_EVENTS']=tmp_after['status']['EXECUTED_EVENTS']-tmp_before['status']['EXECUTED_EVENTS']
#		tmp_result['status']['COM_EMPTY_QUERY']=tmp_after['status']['COM_EMPTY_QUERY']-tmp_before['status']['COM_EMPTY_QUERY']
#		tmp_result['status']['EMPTY_QUERIES']=tmp_after['status']['EMPTY_QUERIES']-tmp_before['status']['EMPTY_QUERIES']
#
#		##variables
#		tmp_result['variables']=tmp_after['variables']
#
#
#		##processlist
#		tmp_result['processlist']=tmp_after['processlist']
#		
#		##response
#		tmp_result['response']={}
#		if tmp_before['response']['query_response_time_range_base'] == '10' and tmp_before['response']['query_response_time_range_base'] == tmp_after['response']['query_response_time_range_base']:
#			tmp_result['response']['0.000001']={}
#			tmp_result['response']['0.000010']={}
#			tmp_result['response']['0.000100']={}
#			tmp_result['response']['0.001000']={}
#			tmp_result['response']['0.010000']={}
#			tmp_result['response']['0.100000']={}
#			tmp_result['response']['1.000000']={}
#			tmp_result['response']['10.000000']={}
#			tmp_result['response']['100.000000']={}
#			tmp_result['response']['1000.000000']={}
#			tmp_result['response']['10000.000000']={}
#			tmp_result['response']['100000.000000']={}
#			tmp_result['response']['1000000.000000']={}
#			tmp_result['response']['TOO LONG']={}
#
#			tmp_result['response']['0.000001']['total']=tmp_after['response']['0.000001']['total']-tmp_before['response']['0.000001']['total']
#			tmp_result['response']['0.000010']['total']=tmp_after['response']['0.000010']['total']-tmp_before['response']['0.000010']['total']
#			tmp_result['response']['0.000100']['total']=tmp_after['response']['0.000100']['total']-tmp_before['response']['0.000100']['total']
#			tmp_result['response']['0.001000']['total']=tmp_after['response']['0.001000']['total']-tmp_before['response']['0.001000']['total']
#			tmp_result['response']['0.010000']['total']=tmp_after['response']['0.010000']['total']-tmp_before['response']['0.010000']['total']
#			tmp_result['response']['0.100000']['total']=tmp_after['response']['0.100000']['total']-tmp_before['response']['0.100000']['total']
#			tmp_result['response']['1.000000']['total']=tmp_after['response']['1.000000']['total']-tmp_before['response']['1.000000']['total']
#			tmp_result['response']['10.000000']['total']=tmp_after['response']['10.000000']['total']-tmp_before['response']['10.000000']['total']
#			tmp_result['response']['100.000000']['total']=tmp_after['response']['100.000000']['total']-tmp_before['response']['100.000000']['total']
#			tmp_result['response']['1000.000000']['total']=tmp_after['response']['1000.000000']['total']-tmp_before['response']['1000.000000']['total']
#			tmp_result['response']['10000.000000']['total']=tmp_after['response']['10000.000000']['total']-tmp_before['response']['10000.000000']['total']
#			tmp_result['response']['100000.000000']['total']=tmp_after['response']['100000.000000']['total']-tmp_before['response']['100000.000000']['total']
#			tmp_result['response']['1000000.000000']['total']=tmp_after['response']['1000000.000000']['total']-tmp_before['response']['1000000.000000']['total']
#			tmp_result['response']['TOO LONG']['total']=0
#
#			tmp_result['response']['0.000001']['count']=tmp_after['response']['0.000001']['count']-tmp_before['response']['0.000001']['count']
#			tmp_result['response']['0.000010']['count']=tmp_after['response']['0.000010']['count']-tmp_before['response']['0.000010']['count']
#			tmp_result['response']['0.000100']['count']=tmp_after['response']['0.000100']['count']-tmp_before['response']['0.000100']['count']
#			tmp_result['response']['0.001000']['count']=tmp_after['response']['0.001000']['count']-tmp_before['response']['0.001000']['count']
#			tmp_result['response']['0.010000']['count']=tmp_after['response']['0.010000']['count']-tmp_before['response']['0.010000']['count']
#			tmp_result['response']['0.100000']['count']=tmp_after['response']['0.100000']['count']-tmp_before['response']['0.100000']['count']
#			tmp_result['response']['1.000000']['count']=tmp_after['response']['1.000000']['count']-tmp_before['response']['1.000000']['count']
#			tmp_result['response']['10.000000']['count']=tmp_after['response']['10.000000']['count']-tmp_before['response']['10.000000']['count']
#			tmp_result['response']['100.000000']['count']=tmp_after['response']['100.000000']['count']-tmp_before['response']['100.000000']['count']
#			tmp_result['response']['1000.000000']['count']=tmp_after['response']['1000.000000']['count']-tmp_before['response']['1000.000000']['count']
#			tmp_result['response']['10000.000000']['count']=tmp_after['response']['10000.000000']['count']-tmp_before['response']['10000.000000']['count']
#			tmp_result['response']['100000.000000']['count']=tmp_after['response']['100000.000000']['count']-tmp_before['response']['100000.000000']['count']
#			tmp_result['response']['1000000.000000']['count']=tmp_after['response']['1000000.000000']['count']-tmp_before['response']['1000000.000000']['count']
#			tmp_result['response']['TOO LONG']['count']=tmp_after['response']['TOO LONG']['count']-tmp_before['response']['TOO LONG']['count']
#			
#			tmp_result['response']['query_response_time_ninety_five_percent'],tmp_result['response']['query_response_time_avg'],total_count=util.get_some_percent(tmp_result['response'],FIELD.NINETY_FIVE_PERCENT)
#
#			tmp_result['response']['0.000001']['percent']        = round(float(tmp_result['response']['0.000001']['count'])/total_count,5)
#			tmp_result['response']['0.000010']['percent']        = round(float(tmp_result['response']['0.000010']['count'])/total_count,5)
#			tmp_result['response']['0.000100']['percent']        = round(float(tmp_result['response']['0.000100']['count'])/total_count,5)
#			tmp_result['response']['0.001000']['percent']        = round(float(tmp_result['response']['0.001000']['count'])/total_count,5)
#			tmp_result['response']['0.010000']['percent']        = round(float(tmp_result['response']['0.010000']['count'])/total_count,5)
#			tmp_result['response']['0.100000']['percent']        = round(float(tmp_result['response']['0.100000']['count'])/total_count,5)
#			tmp_result['response']['1.000000']['percent']        = round(float(tmp_result['response']['1.000000']['count'])/total_count,5)
#			tmp_result['response']['10.000000']['percent']       = round(float(tmp_result['response']['10.000000']['count'])/total_count,5)
#			tmp_result['response']['100.000000']['percent']      = round(float(tmp_result['response']['100.000000']['count'])/total_count,5)
#			tmp_result['response']['1000.000000']['percent']     = round(float(tmp_result['response']['1000.000000']['count'])/total_count,5)
#			tmp_result['response']['10000.000000']['percent']    = round(float(tmp_result['response']['10000.000000']['count'])/total_count,5)
#			tmp_result['response']['100000.000000']['percent']   = round(float(tmp_result['response']['100000.000000']['count'])/total_count,5)
#			tmp_result['response']['1000000.000000']['percent']  = round(float(tmp_result['response']['1000000.000000']['count'])/total_count,5)
#			tmp_result['response']['TOO LONG']['percent']        = round(float(tmp_result['response']['TOO LONG']['count'] )/total_count,5)
#		
##		else:
##			if len(tmp_before['response'])!= len(tmp_after['response']):
##				pass
##			else:
##				pass
##		tmp_result['response']['query_response_time_ninety_five_percent'],tmp_result['response']['query_response_time_avg'],total_count=util.get_some_percent(tmp_result['response'],FIELD.NINETY_FIVE_PERCENT)
#
#		print total_count
#		print tmp_result
#		tmp_before=tmp_after
#		time.sleep(5)
