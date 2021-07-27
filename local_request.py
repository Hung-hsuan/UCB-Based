'''
Created on 2020年9月9日

@author: Hung-hsuan
'''


import xlrd
from RSU_request import  RSU_request
class User_request():
    
    def __init__(self,user_id,request_id):
        self.user_id=user_id         #本地此处文件，标识是哪个用户
        self.request_id=request_id
        #存储local文件
        self.data_id=[]
        self.data_size=[]
        self.data_label=[]
        self.data_request=[]
        if user_id >=0 and user_id <25:
            path='C:\\document\\user'+str(self.user_id)+'_cache.xls'
            rb= xlrd.open_workbook(path,encoding_override="utf-8")
            rs = rb.sheet_by_name('contents')
            for i in range(rs.nrows):
                self.data_id.append(rs.cell_value(i, 0))
                self.data_size.append(rs.cell_value(i, 1))
                self.data_request.append(rs.cell_value(i, 2))
                self.data_label.append(rs.cell_value(i, 3))
    
    def get_file1(self):
        if self.user_id >= 0 and self.user_id < 25:
            flag=0      #标识是否命中
            for item in self.data_id:
                item=int(item)
                if item == self.request_id:
                    return 1
            if flag==0:
                rsu_request=RSU_request(self.user_id,self.request_id)
                local_request=rsu_request.get_file2()
                if(local_request==2):
                    return 2
                elif(local_request==3):
                    return 3
                else:
                    return 0
        else:
            rsu_request = RSU_request(self.user_id, self.request_id)
            local_request = rsu_request.get_file2()
            if (local_request == 2):
                return 2
            elif (local_request == 3):
                return 3
            else:
                return 0
            
         
        
