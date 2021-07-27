"""
Created on 2020年9月01日

@author: admin
"""
import numpy as np
from user import User
from request import request
from file_option1 import Fileoption
from User_UCB1 import User_UCB1
import copy
import  xlwt,xlrd
import datetime
import time

class Model:
    def __init__(self, training_epochs=300):
        self.training_epochs = training_epochs               #周期数
        self.num=25                                           #用户数
        self.num1=30
        self.number=self.num+self.num1
        user_example=User()
        self.arms=[0,1,2,3,4]                                #定义5个手臂
        self.user=user_example.get_user(self.number,self.training_epochs)
        self.counts=[0,0,0,0,0]
        self.ucb_value=[0,0,0,0,0]                #记录reward
        self.user_counts = [[0 for i in range(len(self.arms))] for i in range(self.num)]
        self.ucb_value2 = [[0 for i in range(len(self.arms))] for i in range(self.num)]  # 创建一个二维数组存取reward
        self.user_expect_reward_estimate=[[0 for i in range(len(self.arms))] for i in range(self.num)]
        self.expect_reward_estimate = [1,1,1,1,1]


    def pull(self):
        ucb_value1=[0,0,0,0,0]
        self.ucb_value = [0,0,0,0,0]
        for arm in self.arms:
            if self.counts[arm]==0:
                self.ucb_value[arm]=1
                flag = 0
                return arm, flag
            # elif self.counts[arm]<2:
            #     self.ucb_value[arm] = 1
            #     flag=0
            #     return arm,flag


        self.ucb_value=copy.deepcopy(self.expect_reward_estimate)
        total_counts=np.sum(self.counts)
        print("total_counts="+str(total_counts))
#         bonus = [self.ucb_value[arm]+np.sqrt((3*np.log(total_counts))/(2*self.counts[arm])) for arm in self.arms]
#         m=max(bonus)
        for arm in self.arms:
            bonus = np.sqrt((2*np.log(total_counts))/(self.counts[arm]))
            print("self.ucb_value[arm]="+str(self.ucb_value[arm]))
            ucb_value1[arm] = self.ucb_value[arm] + 1.2 * bonus
            print(bonus)
        print("ucb_value1=" + str(ucb_value1))
        best_arm = ucb_value1.index(max(ucb_value1))
        flag=1
        return best_arm,flag

    def ucb1(self):
        user_hit = [[] for i in range(self.training_epochs)]
        edge_hit = []
        rwb = xlwt.Workbook()
        rws = rwb.add_sheet('contents')
        rwb1 = xlwt.Workbook()
        rws1 = rwb1.add_sheet('contents')
        user_result={}                                  #存储每个用户请求的命中情况
        result=[]                                       #存储所有的命中情况
        user_id2=copy.deepcopy(self.user)                                #要用deepcopy啊兄嘚
        total_user_request=0
        total_counts=0  #计数
        m=0
        total_request_num=0
        #self.expect_reward_estimate = [1,1,1,1,1]
        #获取时间戳
        t1 = datetime.datetime.now().microsecond
        t2 = time.mktime(datetime.datetime.now().timetuple())  # mktime用于返回时间戳

        for i in range(self.training_epochs):
            best_arm,flag=Model.pull(self)
            self.counts[best_arm]=self.counts[best_arm]+1
            # 收集反馈的奖励数据
            print('第'+str(i)+'个周期----------best_arm'+str(best_arm))
            print("UCB-----self.ucb_value=" + str(self.ucb_value))
            fileoption=Fileoption(best_arm,self.ucb_value)         #存储文件
            fileoption.option()

            #更新期望奖励估计            # req=request(self.num,self.user,self.arms)                 #请求文件
            # total_request_num,user_result,result=req.send_request(i)
            # 把用户数，命中情况，周期数和用户臂的选择情况传到User_UCB1中
            user_ucb1=User_UCB1(self.num,self.number,i,self.user_counts,self.ucb_value2,user_id2)
            self.user_expect_reward_estimate,self.user_counts,self.ucb_value2,total_request_num,user_result,result=user_ucb1.ucb1(self.user_expect_reward_estimate)
            print("user_result=" + str(user_result))
            sum_sbs=0                                               #记录SBS命中个数
            sum_rsu=0                                               #记录RSU命中个数
            sum_user=0
            total_user_request = 0                                  #总的请求次数
            for j in result:
                if j==3:
                    sum_sbs=sum_sbs+1
                elif j==2:
                    sum_rsu=sum_rsu+1
            for m in range(self.num):
                for item in user_result[m]:
                    if item == 1:
                        sum_user=sum_user+1
                #print('user_result[m]='+str(self.user_result[m]))
                #print("user_id2["+str(m)+"]["+str(i)+"]="+str(user_id2[m][i]))
                print("USER"+str(m)+"的本地请求命中率为："+str((sum_user/user_id2[m][i])*100)+"%")
                user_hit[i].append(sum_user/user_id2[m][i])
                #print("sum_user="+str(sum_user))
                total_user_request=sum_user+total_user_request
                sum_user=0
            print("total_user_request="+str(total_user_request))
            print("total_request_num=" + str(total_request_num))
            print("sum_rsu=" + str(sum_rsu))
            print("sum_sbs=" + str(sum_sbs))
            sbs_cache_hit=sum_sbs/(total_request_num-sum_rsu-total_user_request)
            edge_hit.append(sbs_cache_hit)
            print("SBS的命中率为："+str((sbs_cache_hit)*100)+"%")
            print("RSU的命中率为："+str((sum_rsu/(total_request_num-total_user_request))*100)+"%")
            if flag==0:
                self.expect_reward_estimate[best_arm]=sbs_cache_hit
                #print("UCB1------expect_reward_estimate="+str(self.expect_reward_estimate))
            else:
                self.ucb_value=copy.deepcopy(self.expect_reward_estimate)
                d_value = self.ucb_value[best_arm]*10-sbs_cache_hit*10
                print("d_vaue=" +str(d_value))
                #self.ucb_value[best_arm] = self.ucb_value[best_arm] + d_vaue
                #self.ucb_value[best_arm] =((self.ucb_value[best_arm] * self.counts[best_arm] + sbs_cache_hit*100)/(self.counts[best_arm] + 1))+d_vaue
                self.ucb_value[best_arm] = self.ucb_value[best_arm]*10 +(d_value/(self.counts[best_arm]+1))
                self.expect_reward_estimate = copy.deepcopy(self.ucb_value)
                #归一化
                sum=0
                for em in self.expect_reward_estimate:
                    sum=sum+em
                for i in self.arms:
                    if self.expect_reward_estimate[i] < 0:
                        self.expect_reward_estimate[i]=0.01
                    self.expect_reward_estimate[i]=self.expect_reward_estimate[i]/sum
            print("UCB1-----self.ucb_value=" + str(self.ucb_value))
            print("UCB1-----self.counts=" + str(self.counts))
            total_counts=total_counts+1
            print("----------------------------")
        t3 = datetime.datetime.now().microsecond
        t4 = time.mktime(datetime.datetime.now().timetuple())
        str_time = (t4 - t2) * 1000 + (t3 - t1) / 1000
        print("str_time=" + str(str_time))
        i=0
        for k in range(0,len(user_hit)):
            for j in range(0,len(user_hit[k])):
                rws.write(j, k+1, user_hit[k][j])
        rwb.save('C:\\result\\ucb1\\user_hit.xls')

        for m in range(0,len(edge_hit)):
            rws1.write(m+1, 0, edge_hit[m])


        rwb1.save('C:\\result\\ucb1\\edge_hit.xls')
        print(datetime.datetime.now())
if __name__ == '__main__':
    model=Model()
    model.ucb1()
