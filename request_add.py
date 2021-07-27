'''
Created on 2020年9月20日

@author: Hung-hsuan

function:当RSU中文件命中时，更新文件的时间
'''
import xlrd,xlwt

class Request_add():

    def __init__(self,request_id):
        self.request_id=request_id
        #存储local文件
        self.data_id=[]
        self.data_size=[]
        self.data_label=[]
        self.data_time=[]
        self.data_request=[]
        path='C:\document\cache.xls'
        rb= xlrd.open_workbook(path,encoding_override="utf-8")
        rs = rb.sheet_by_name('contents')
        rb1= xlwt.Workbook()
        rs1 = rb1.add_sheet('contents')
        index=0
        for i in range(rs.nrows):
            self.data_id.append(rs.cell_value(i, 0))
            self.data_size.append(rs.cell_value(i, 1))
            self.data_request.append(rs.cell_value(i, 2))
            self.data_label.append(rs.cell_value(i, 3))
        for j in range(len(self.data_id)):
            if self.data_id[j]==self.request_id:
                index=j
                break
        self.data_request[index]=self.data_request[index]+1

        s=0
        inx=0
        for i in self.data_id:
            i=int(i)
            for j in range(len(self.data_id)):
                if self.data_id[j]==i:
                    inx=j
            inx=int(inx)
            #print(self.data_time[inx-1])
            rs1.write(s,0,self.data_id[inx])
            rs1.write(s,1,self.data_size[inx])
            rs1.write(s,2,self.data_request[inx])
            rs1.write(s,3,self.data_label[inx])
            s+=1
        rb1.save('C:\document\cache.xls')
