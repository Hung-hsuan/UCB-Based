'''
Created on 2020年8月1日

@author: Hung-hsuan
'''
from request import request


class Reward:
    def __init__(self,best_arm,expect_reward_estimate=[]):
        self.expect_reward_estimate=expect_reward_estimate
        self.best_arm=best_arm
        
    def get_reward(self):
        myclass=MyClass(self.best_arm,self.expect_reward_estimate)
        self.request_hit=myclass.__getitem__()
        return self.request_hit
        
        