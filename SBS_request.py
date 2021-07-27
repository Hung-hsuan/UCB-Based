'''
Created on 2020年9月17日

@author: Hung-hsuan

Function:向基站请求数据
'''

import xlrd,xlwt

class SBS_request():

    def __init__(self,user_id,request_id):
        self.user_id=user_id         #本地此处文件，标识是哪个用户
        self.request_id=request_id
        #存储local文件
        self.data_id=[]
        self.data_size=[]
        self.data_label=[]
        self.data_request=[]
        self.i=0
        path='C:\document\cache1.xls'
        rb= xlrd.open_workbook(path,encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')


        for i in range(rs.nrows):
            self.data_id.append(rs.cell_value(i, 0))
            self.data_size.append(rs.cell_value(i, 1))
            self.data_request.append(rs.cell_value(i, 2))
            self.data_label.append(rs.cell_value(i, 3))
        #print(self.request_id)
    def get_file3(self):
        #print("self.request_id=" + str(self.request_id))
        flag=0                #标识是否命中
        for item in self.data_id:
            item=int(item)
            if item == self.request_id:
                return 3
        if flag==0:
            #print(self.request_id)
            return 0
