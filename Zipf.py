'''
Created on 2020年9月15日

@author: Hung-hsuan
'''
import math

class Zipf():
    #num表示生成多少zipf数
    def get_zipf(self,num):
        self.num=num
        a=0.8
        p=[]
        sum=0.0
        for i in range(1,self.num):
            for j in range(1,self.num):
                sum=sum+(math.pow(j, -a))
            fm=sum*(math.pow(i, a))
            sum=0
            s=1/fm
            p.append(s)
        return p