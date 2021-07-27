'''
Created on 2021年5月24日

@author: Hung-hsuan

function:test
'''
import time
import datetime


t1=datetime.datetime.now().microsecond
t2=time.mktime(datetime.datetime.now().timetuple())     # mktime用于返回时间戳

time.sleep(6)

t3=datetime.datetime.now().microsecond
t4=time.mktime(datetime.datetime.now().timetuple())

str_time=(t4-t2)*1000+(t3-t1)/1000
print("str_time="+str(str_time))