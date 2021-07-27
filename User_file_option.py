'''
Created on 2020年3月25日

@author: admin

function:摇动臂，选择文件存储
'''
import xlwt,xlrd
import random
import pandas as pd
import numpy as np

class User_file_option(object):
    def __init__(self,user_id,best_arm,expect_reward_estimate=[]):
        self.expect_reward_estimate=expect_reward_estimate               #目前为止的奖励值
        print("self.user_expect_reward_estimate="+str(self.expect_reward_estimate))
        self.best_arm=best_arm                     #需要拉动的手臂
        self.user_id=user_id
        
    def option(self): 
        sum=0.0
        p=self.expect_reward_estimate                             #每个手臂需要拉动的数量，存储分配
        data_request=[]       #数据请求次数
        data_label=[]         #数据标签
        data_size=[]          #数据大小
        data_id=[]            #数据id
        data_cache_size=0     #控制cache大小不超过存储器容量上限
        id_again1=0
        cache_maxsize=5000    #存储器最大容量
        type1=[]
        type2=[]
        type3=[]
        type4=[]
        type5=[]
        cache=[]              #存储选中的内容
        data_req={}           #存储相关数据，准备排序
        rb= xlrd.open_workbook('C:\document\cache.xls',encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        rwb=xlwt.Workbook()
        rws =rwb.add_sheet('contents')
        
        for i in range(rs.nrows):
            data_id.append(rs.cell_value(i, 0))
            data_size.append(rs.cell_value(i, 1))
            data_request.append(rs.cell_value(i, 2))
            data_label.append(rs.cell_value(i, 3))
        #把数据按照数据标签分隔开
        df = pd.DataFrame(
            {'id': data_id, 'size': data_size, 'type': data_label,
             'data_request': data_request})  # 将数据转换为pandas格式，按照请求次数进行排序
        ds = df.sort_values(by='data_request', ascending=False)
        data = np.array(ds).tolist()
        for item in data:
            if item[2] == 'type1':
                type1.append(item[0])
            if item[2] == 'type2':
                type2.append(item[0])
            if item[2] == 'type3':
                type3.append(item[0])
            if item[2] == 'type4':
                type4.append(item[0])
            if item[2] == 'type5':
                type5.append(item[0])

        #按照概率存储器excel1存储数据到缓存器
        for i in range(1000000):
            if data_cache_size<=cache_maxsize:
                control_parameter=random.random()          #control_parameter 表示一个控制参数
                if control_parameter>=0 and control_parameter<p[0] and len(type1)!=0:
                    control_parameter1 = random.random()
                    #if control_parameter1 > 0.2 :
                    id_again=type1[0]
                    #else:
                    id_again=random.choice(type1)
                    id_again1=int(id_again)
                    type1.remove(id_again)                     #删除已经选择的内容，防止重复
                    data_cache_size=data_cache_size+data_size[id_again1-1]
                    cache.append(id_again1)
                if control_parameter>=p[0] and control_parameter<(p[0]+p[1]) and len(type2)!=0:
                    control_parameter1 = random.random()
                    #if control_parameter1 > 0.2:
                    id_again = type2[0]
                    #else:
                    id_again = random.choice(type2)
                    id_again1=int(id_again)
                    type2.remove(id_again)
                    data_cache_size=data_cache_size+data_size[id_again1-1]
                    cache.append(id_again1)
                if control_parameter>=(p[0]+p[1])and control_parameter<(p[0]+p[1]+p[2]) and len(type3)!=0:
                    control_parameter1 = random.random()
                    #if control_parameter1 > 0.2:
                    id_again = type3[0]
                    #else:
                    id_again = random.choice(type3)
                    id_again1=int(id_again)
                    type3.remove(id_again)
                    data_cache_size=data_cache_size+data_size[id_again1-1]
                    cache.append(id_again1)
                if control_parameter>=(p[0]+p[1]+p[2]) and control_parameter<(p[0]+p[1]+p[2]+p[3]) and len(type4)!=0:
                    control_parameter1 = random.random()
                    #if control_parameter1 > 0.2:
                    id_again = type4[0]
                    #else:
                    id_again = random.choice(type4)
                    id_again1=int(id_again)
                    type4.remove(id_again)
                    data_cache_size=data_cache_size+data_size[id_again1-1]
                    cache.append(id_again1)
                if control_parameter>=(p[0]+p[1]+p[2]+p[3]) and control_parameter<=1 and len(type5)!=0:
                    control_parameter1 = random.random()
                    #if control_parameter1 > 0.2:
                    id_again = type5[0]
                    #else:
                    id_again = random.choice(type5)
                    id_again1=int(id_again)
                    type5.remove(id_again)
                    data_cache_size=data_cache_size+data_size[id_again1-1]
                    cache.append(id_again1)
            else:
                break
        s=0
        inx=0
        for j in cache:
            j = int(j)
            for item in range(0, len(data_id)):
                if data_id[item] == j:
                    inx = item
                    break
            # print(j)
            # print("data_id[j-1]=" + str(data_id[inx]))
            # print("data_size[j-1]=" + str(data_size[inx]))
            rws.write(s,0,data_id[inx])
            rws.write(s,1,data_size[inx])
            rws.write(s,2,data_request[inx])
            rws.write(s,3,data_label[inx])
            s+=1
        path='C:\\document\\user'+str(self.user_id)+'_cache.xls'
        rwb.save(path)   
