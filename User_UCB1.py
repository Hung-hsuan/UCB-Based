"""
Created on 2020年9月01日

@author: admin
"""
import numpy as np
from user import User
from request import request
from User_file_option import User_file_option
import copy

class User_UCB1:
    def __init__(self,num,number,period,user_conuts,ucb_value,user):
        self.num=num                                           #用户数
        self.number=number
        self.arms=[0,1,2,3,4]                                #定义5个手臂
        self.user_counts=user_conuts
        self.ucb_value=ucb_value                         #创建一个二维数组存取reward
        self.period=period                               #周期数
        #print("self.ucb_value[i]="+str(self.ucb_value))
        #print("self.user_counts="+str(self.counts))
        self.user_expect_reward_estimate = [[0 for i in range(len(self.arms))] for i in range(self.num)]
        self.user=user
        #print("self.user=" + str(self.user))

    def pull(self,id,user_expect_reward_estimate):
        ucb_value1=[[0 for i in range(len(self.arms))] for i in range(self.num)]
        self.ucb_value = [[0 for i in range(len(self.arms))] for i in range(self.num)]
        for arm in self.arms:
            if self.user_counts[id][arm]==0:
                self.ucb_value[id][arm]=1
                flag = 0
                return arm,flag
            # elif self.user_counts[id][arm]<2:
            #     self.ucb_value[id][arm] = 1
            #     flag=0
            #     return arm,flag
        self.ucb_value=copy.deepcopy(user_expect_reward_estimate)
        #归一化
        sum = 0
        for em in self.ucb_value[id]:
            sum = sum + em
        for j in self.arms:
            self.ucb_value[id][j] = self.ucb_value[id][j] / sum
        total_counts=np.sum(self.user_counts[id])
#         bonus = [self.ucb_value[arm]+np.sqrt((3*np.log(total_counts))/(2*self.counts[arm])) for arm in self.arms]
#         m=max(bonus)
        print("self.ucb_value[id]=" + str(self.ucb_value[id]))
        for arm in self.arms:
            bonus = np.sqrt((2*np.log(total_counts))/(self.user_counts[id][arm]))
            #print("bonus=" + str(bonus))
            ucb_value1[id][arm] = self.ucb_value[id][arm] + bonus
        print("ucb_value1[id]="+str(ucb_value1[id]))
        best_arm = ucb_value1[id].index(max(ucb_value1[id]))
        flag=1
        return best_arm,flag    
            
    def ucb1(self,user_expect_reward_estimate):
        user_result = {}  # 存储每个用户请求的命中情况
        result = []  # 存储所有的命中情况
        total_request_num=0
        self.user_expect_reward_estimate=user_expect_reward_estimate
        for i in range(0,self.num):
            best_arm,flag=User_UCB1.pull(self,i,self.user_expect_reward_estimate)
            print('第' + str(i) + '个用户----------best_arm' + str(best_arm))
            #print("i="+str(i)+"----------"+"best_arm="+str(best_arm))
            #print("前self.counts[" + str(i) + "][" + str(best_arm) + "]=" + str(self.user_counts[i][best_arm]))
            self.user_counts[i][best_arm] = self.user_counts[i][best_arm] + 1
            #print('第' + str(i) + '个 User----------best_arm=' + str(best_arm))
            print("self.user_counts=" + str(self.user_counts))
            #print("self.counts["+str(i)+"]["+str(best_arm)+"]="+str(self.user_counts[i][best_arm]))
            # 收集反馈的奖励数据
            print("self.ucb_value[i]="+str(self.ucb_value[i]))
            fileoption=User_file_option(i,best_arm,self.ucb_value[i])         #存储文件
            fileoption.option()
        user_id3=copy.deepcopy(self.user)
        #请求
        req = request(self.number, user_id3, self.arms)  #请求文件
        total_request_num,user_result,result = req.send_request(self.period)
        for i in range(0, self.num):
            # 更新期望奖励估计
            sum_user=0
            for item in user_result[i]:
                if item == 1:
                    sum_user=sum_user+1
            user_cache_hit=sum_user/self.user[i][self.period]
            #print("user_cache_hit="+str(user_cache_hit))
            if flag==0:
                self.user_expect_reward_estimate[i][best_arm]=user_cache_hit
            else:
                self.ucb_value[i]=copy.deepcopy(self.user_expect_reward_estimate[i])
                d_vaue=user_cache_hit*10-self.ucb_value[i][best_arm]*10
                #print("d_vaue="+str(d_vaue))
                #self.ucb_value[i][best_arm]=self.ucb_value[i][best_arm]+d_vaue
                self.ucb_value[i][best_arm] =self.ucb_value[i][best_arm]*10 + (d_vaue /(self.user_counts[i][best_arm] + 1))
                #self.ucb_value[i][best_arm] =((self.ucb_value[i][best_arm] * self.user_counts[i][best_arm] + user_cache_hit*100)/(self.user_counts[i][best_arm] + 1))+d_vaue
                self.user_expect_reward_estimate[i] = copy.deepcopy(self.ucb_value[i])
                sum = 0
                for em in self.ucb_value[i]:
                    sum = sum + em
                for j in self.arms:
                    self.ucb_value[i][j] = self.ucb_value[i][j] / sum
        return self.user_expect_reward_estimate,self.user_counts,self.ucb_value,total_request_num,user_result,result
