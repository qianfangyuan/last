# -*- coding: utf-8 -*-
get_response_total_time=lambda x: 0 if x =='TOO LONG' else  float(x)

def get_some_percent(response_time,percent=0.95):
	lcount=[]
	ltotal=[]
	lcount_sum=0
	ltotal_sum=0
	save_float=5
	result_save_float=0
	dpercent=round((1-percent)/2,save_float)
	lopercent=0
	lapercent=0
	lo=0
	la=0
	for i in sorted(response_time.keys()):
		lcount.append(response_time[i]['count'])
		ltotal.append(response_time[i]['total'])
		lcount_sum=lcount_sum+response_time[i]['count']
		ltotal_sum=ltotal_sum+response_time[i]['total']
	save_total=dpercent*lcount_sum
	if save_total == 0:
		return 0,0
	for i in range(1,len(lcount)):
		if sum(lcount[:i]) > save_total:
			lo=i-1
			lopercent=round(1-(sum(lcount[:i])-save_total)/lcount[lo],save_float)
			break
	for i in range(1,len(lcount)):
		if sum(lcount[-i:]) > save_total:
			la=len(lcount)-i
			lapercent=round(1-(sum(lcount[-i:])-save_total)/lcount[la],save_float)
			break
	if lo== la:
		return round( ltotal[lo]*(1-lopercent-lapercent)/(lcount_sum*percent),result_save_float),round(ltotal_sum/lcount_sum,result_save_float),lcount_sum
	elif lo+1 == la:
		return round( (ltotal[lo]*(1-lopercent)+ltotal[la]*(1-lapercent))/(lcount_sum*percent),result_save_float ),round(ltotal_sum/lcount_sum,result_save_float),lcount_sum
	else:
		return round( (sum(ltotal[lo+1:la])+ltotal[lo]*(1-lopercent)+ltotal[la]*(1-lapercent) ) / (lcount_sum*percent),result_save_float),round(ltotal_sum/lcount_sum,result_save_float),lcount_sum

def get_percent(response_time):
	lcount=[]
	ltotal=[]
	lcount_sum=0
	ltotal_sum=0
	save_float=6
	dpercent=round((1-percent)/2,save_float)
	lopercent=0
	lapercent=0
	lo=0
	la=0
	for i in response_time:
		lcount.append(int(i[1]))
		ltotal.append(get_response_total_time(i[2].strip()))
		lcount_sum=lcount_sum+int(i[1])
		ltotal_sum=ltotal_sum+get_response_total_time(i[2])
	save_total=dpercent*lcount_sum
	for i in range(1,len(lcount)):
		if sum(lcount[:i]) > save_total:
			lo=i-1
			lopercent=round(1-(sum(lcount[:i])-save_total)/lcount[lo],save_float)
			break
	for i in range(1,len(lcount)):
		if sum(lcount[-i:]) > save_total:
			la=len(lcount)-i
			lapercent=round(1-(sum(lcount[-i:])-save_total)/lcount[la],save_float)
			break
	if lo== la:
		return round( ltotal[lo]*(1-lopercent-lapercent)/(lcount_sum*percent),save_float),round(ltotal_sum/lcount_sum,save_float)
	elif lo+1 == la:
		return round( (ltotal[lo]*(1-lopercent)+ltotal[la]*(1-lapercent))/(lcount_sum*percent),save_float ),round(ltotal_sum/lcount_sum,save_float)
	else:
		return round( (sum(ltotal[lo+1:la])+ltotal[lo]*(1-lopercent)+ltotal[la]*(1-lapercent) ) / (lcount_sum*percent),save_float),round(ltotal_sum/lcount_sum,save_float)
			
if __name__ == '__main__':
	result_response=\
(('      0.000001', 0, '      0.000000'),\
 ('      0.000010', 0, '      0.000000'),\
 ('      0.000100', 19, '      0.001067'),\
 ('      0.001000', 29, '      0.010055'),\
 ('      0.010000', 5, '      0.022794'),\
 ('      0.100000', 0, '      0.000000'),\
 ('      1.000000', 0, '      0.000000'),\
 ('     10.000000', 0, '      0.000000'),\
 ('    100.000000', 0, '      0.000000'),\
 ('   1000.000000', 0, '      0.000000'),\
 ('  10000.000000', 0, '      0.000000'),\
 (' 100000.000000', 0, '      0.000000'),\
 ('1000000.000000', 0, '      0.000000'),\
 ('TOO LONG', 0, 'TOO LONG'))
	print get_ninety_five_percent(result_response)

