'''
Created on 2020年9月15日

@author: Hung-hsuan

function:用户类
'''

import numpy as np
import random

class User():
    def __init__(self):
        self.user=[]
        
    def get_user(self,num,size):
        for i in range(0,num):
            lam=int(random.randint(20,30))
            self.user.append(np.random.poisson(lam=lam, size=size))
        return self.user
    
    