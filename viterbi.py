# -*- coding:utf-8 -*-
"""
Created on 2018-09-14 10:12:16

Author: Xiong Zecheng (295322781@qq.com)
"""
from prettytable import PrettyTable
from model import Model

class Viterbi():
    def __init__(self):
        m = Model()
        self.observations,\
        self.states,\
        self.start_probability,\
        self.transition_probability,\
        self.emission_probability = m.load_model()

    # 维特比算法 obs_seq-观测序列
    def poccess(self,*observations):
        # 隐状态序列
        hidden_state = list()
        # 路径概率表
        v = list()

        # 初始状态概率
        start_p = list()
        start_max = -1
        max_start_state = ""
        for state in self.states:
            p = self.start_probability[state] * self.emission_probability[state][observations[0]]
            start_p.append(p)
            if p > start_max:
                start_max = p
                max_start_state = state
        v.append(start_p)
        hidden_state.append(max_start_state)

        for obs in observations[1:]:
            state_p = list()
            max = -1
            max_state = ""
            for state in self.states:
                transited_p = 0
                for i in range(len(self.states)):
                    transited_p += v[-1][i] * self.transition_probability[self.states[i]][state]
                p = transited_p * self.emission_probability[state][obs]
                state_p.append(p)
                if p > max:
                    max = p
                    max_state = state
            v.append(state_p)
            hidden_state.append(max_state)

        observations_p=sum(v[-1])
        self.print_table(v)
        print(hidden_state)
        print("观测序列概率："+str('%.5f'%observations_p))

    def print_table(self,v):
        table = PrettyTable()
        table.add_column("",list(self.states))
        for i in range(len(v)):
            table.add_column(str(i),list(map(lambda x:'%.5f'%x,v[i])))
        print(table)

if __name__ == "__main__":
    v=Viterbi()
    v.poccess("i","want","four","month","to","chicago")