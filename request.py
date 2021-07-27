'''
Created on 2020年9月16日

@author: Hung-hsuan

Function: 分用户请求数据
'''

from user import User
import random
from local_request import  User_request
from request_add import Request_add
from Zipf import Zipf
import xlrd

class request():
    
    def __init__(self,num,user,arms):
        self.num=num                                           #用户数
        self.user=user
        self.arms=arms
        self.user_request_num = [[] for i in range(self.num)]
        self.type1 = []
        self.type2 = []
        self.type3 = []
        self.type4 = []
        self.type5 = []
        rb = xlrd.open_workbook('C:\document\cache.xls', encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        for i in range(rs.nrows):
            if rs.cell_value(i, 3)=='type1':
                self.type1.append(rs.cell_value(i, 0))
            if rs.cell_value(i, 3)=='type2':
                self.type2.append(rs.cell_value(i, 0))
            if rs.cell_value(i, 3)=='type3':
                self.type3.append(rs.cell_value(i, 0))
            if rs.cell_value(i, 3)=='type4':
                self.type4.append(rs.cell_value(i, 0))
            if rs.cell_value(i, 3)=='type5':
                self.type5.append(rs.cell_value(i, 0))


    def send_request(self,i):
        total_request_num=0                                          #记录每个周期的总请求
        user_id1=[]
        user_result={}
        result=[] 
        for k in range(self.num):                                #self.user[i][k] 表示第i个用户在周期k的请求次数
            #print(self.user[k][i]) 
            total_request_num= total_request_num+self.user[k][i]
        #print('total_request_num='+str(total_request_num))
        sum=0
        #把用户存在列表中，方便删除
        for em in range(self.num):
            user_id1.append(em)
            #确定哪个用户请求
        zipf1 = Zipf()
        zipf = zipf1.get_zipf(1000)
        for item in range(0,1000000):            #这个1000000是一个足够大的数，后面会break
        #模拟zipf请求
            flag=0
            sum=0
            if user_id1:
                user_id=random.choice(user_id1)
                #print("user_id="+str(user_id))
                if self.user[user_id][i] != 0:
                    self.user[user_id][i]=self.user[user_id][i]-1
                    control_parameter = random.random()
                    request_id = 0
                    for l in range(-1, 998):
                        if sum < control_parameter and control_parameter < (sum + zipf[l + 1]):
                            request_id = l + 2
                            break
                        else:
                            sum = sum + zipf[l+1]
                    #print("self.user_request_num=" + str(self.user_request_num))
                    if self.user_request_num[user_id]:
                        for em in self.user_request_num[user_id]:
                            #print("item ="+str(item)+"------------"+str(em))
                            em=int(em)
                            if em==request_id:
                                flag=1
                                break
                        if flag==0:
                            request_id=int(request_id)
                            self.user_request_num[user_id].append(request_id)
                            user_request1=User_request(user_id,request_id)
                            Request_add(request_id)
                            #将用户请求命中情况存储在字典dict1中，字典被格式化，每个键可以对应多个值
                            ppp=user_request1.get_file1()
                            user_result.setdefault(user_id,[]).append(ppp)
                            result.append(ppp)
                    else:
                        self.user_request_num[user_id].append(request_id)
                else:
                    user_id1.remove(user_id)                   #删除用户请求数为0的用户，表示用户请求完成
            else:
                break
        print("self.user_request_num="+str(self.user_request_num))
        return total_request_num,user_result,result                        #返回命中情况