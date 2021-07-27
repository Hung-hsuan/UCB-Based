'''
Created on 2020年9月17日

@author: Hung-hsuan
'''
import xlrd,xlwt
import datetime
from SBS_request import  SBS_request
from RSU_file_cache import RSU_file_cache
import pandas as pd
import numpy as np

class RSU_request():
    
    def __init__(self,user_id,request_id):
        self.user_id=user_id         #本地此处文件，标识是哪个用户
        self.request_id=request_id
        #存储local文件
        self.data_id=[]
        self.data_size=[]
        self.data_label=[]
        self.data_time=[]
        self.data_id1=[]
        self.data_size1=[]
        self.data_label1=[]
        self.data_time1={}
        self.max_cache=1000              #RSU最大存储大小
        path='C:\document\RSU_cache.xls'
        rb= xlrd.open_workbook(path,encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        for i in range(rs.nrows):
            self.data_id.append(rs.cell_value(i, 0))
            self.data_size.append(rs.cell_value(i, 1))
            self.data_label.append(rs.cell_value(i, 3))
            self.data_time.append(rs.cell_value(i, 4))
        #存储总数据
        path='C:\document\cache.xls'
        rb1= xlrd.open_workbook(path,encoding_override="utf-8")
        rs1 = rb1.sheet_by_name('contents')
        for i in range(rs1.nrows):
            self.data_id1.append(rs1.cell_value(i, 0))
            self.data_size1.append(rs1.cell_value(i, 1))
            self.data_label1.append(rs1.cell_value(i, 3))

    def get_file2(self):
        rb1= xlwt.Workbook()
        rs1 = rb1.add_sheet('contents')
        data_sort=[]                                                    #存储按时间排序后的data_id
        data_time2={}
        rsu_cache=0
        flag=0
        for item in self.data_id:
#             for em in range(len(self.data_id)):
#                 if self.data_id[em]==item:
#                     index=em                                                #index表示此时请求的用户id在数组中的索引
            item=int(item)
            if item == self.request_id:                                     #如果命中
                '''此处需要对RSU文件进行操作'''
                time1=datetime.datetime.now()
                day = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S')          #将获取的时间编程string形式
                RSU_file_cache(self.request_id,day)     #更新文件请求的时间
                flag=1
                return 2
        if flag==0:                                            #如果未命中，则继续向SBS发出请求
                #对文件请求时间进行排序，以便根据文件大小进行替换文件
                #self.data_time.sort(key=None, reverse=False)                #默认升序
            df=pd.DataFrame({'id':self.data_id,'size':self.data_size,'time':self.data_time})    #将数据转换为pandas格式，按照时间进行排序
            ds=df.sort_values('time')
            data=np.array(ds).tolist()                                   #再把数据转换为array格式
            fg=0
            for item in data:
                #data_sort[item[0]]=item[3]
                em=item[0]
                for im in data_sort:
                    im=int(im)
                    if im==em:
                        fg=1
                if fg==0:
                    data_sort.append(em)                                           #将id存储在列表中,按时间排好序的id
                    data_time2[em] = item[2]
            #print(data_sort)
            sum=0
            inx = 0
            #对文件进行替换
            for i in data_sort:                          #计算未替换前存储器中所有文件大小
                i=int(i)
                for j in range(0,len(self.data_id1)):
                    if self.data_id1[j]==i:
                        inx=j
                        #print("i=" + str(i) + "----data_size1[i]=" + str(self.data_size1[inx]))
                        sum=sum+self.data_size1[inx]
                        break
            k=0          #记录self.request_id在data_id1中的索引下标
            for j in range(0,len(self.data_id1)):
                if self.data_id1[j]==self.request_id:
                    k=j
            if sum+self.data_size1[k] > self.max_cache:   #判断加上新文件是否超过存储器大小
                for i in data_sort:
                    i=int(i)
                    for j in range(0, len(self.data_id1)):
                        if self.data_id1[j] == i:
                            inx = j
                            #print("i="+str(i)+"----data_size1[i]="+str(self.data_size1[i]))
                            sum=sum-self.data_size1[inx]
                            data_sort.remove(i)                  #删除被替换文件
                            break
                    if sum+self.data_size1[k] < self.max_cache:     #如果加上新请求文件大小小于最大存储
                        lg=0
                        for item in data_sort:
                            item = int(item)
                            if item == self.request_id:
                                lg = 1
                                break
                        if lg == 0:
                            data_sort.append(self.request_id)                 #添加文件到存储器
                            time1 = datetime.datetime.now()
                            day1 = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S')
                            data_time2[self.request_id]=day1
                            break
            else:
                ag=0
                for item in data_sort:
                    item=int(item)
                    if item==self.request_id:
                        ag=1
                        break
                if ag==0:
                    data_sort.append(self.request_id)
                    time1 = datetime.datetime.now()
                    day1 = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S')
                    data_time2[self.request_id] = day1
            #print("data_sort=" + str(data_sort))
            s=0
            for i in data_sort:
                i=int(i)
                for j in range(len(self.data_id1)):
                    if self.data_id1[j]==i:
                        inx=j
                        inx=int(inx)                                        #inx表示data_id对应的索引
                # print(i)
                # print("data_id[j-1]=" + str(self.data_id1[inx]))
                # print("data_size[j-1]=" + str(self.data_size1[inx]))
                rs1.write(s,0,self.data_id1[inx])
                rs1.write(s,1,self.data_size1[inx])
                rs1.write(s,2,0)
                rs1.write(s,3,self.data_label1[inx])
                rs1.write(s,4,data_time2[i])
                s=s+1
            rb1.save('C:\document\RSU_cache.xls')
            sbs_request=SBS_request(self.user_id,self.request_id)      #将请求发到SBS
            rsu_cache=sbs_request.get_file3()
            return rsu_cache
