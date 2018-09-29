# -*- coding:utf-8 -*-
"""
Created on 2018-09-14 10:12:16

Author: Xiong Zecheng (295322781@qq.com)
"""
from prettytable import PrettyTable
from hmm.model import Model

class Viterbi():
    def __init__(self,modelpath):
        m = Model()
        self.observations,\
        self.states,\
        self.start_probability,\
        self.transition_probability,\
        self.emission_probability = m.load_model(modelpath)

    # 维特比算法 obs_seq-观测序列
    def poccess(self,observations):
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
        if start_max==0:
            default_max = -1
            for state in self.states:
                if self.start_probability[state] > default_max:
                    default_max = self.start_probability[state]
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
            if max == 0:
                default_max = -1
                for state in self.states:
                    transited_p = 0
                    for i in range(len(self.states)):
                        transited_p += v[-1][i] * self.transition_probability[self.states[i]][state]
                    if transited_p > default_max:
                        default_max = transited_p
                        max_state = state
            v.append(state_p)
            hidden_state.append(max_state)

        # self.print_table(v)
        return hidden_state

    def print_table(self,v):
        table = PrettyTable()
        table.add_column("",list(self.states))
        for i in range(len(v)):
            table.add_column(str(i),list(map(lambda x:'%.5f'%x,v[i])))
        print(table)

if __name__ == "__main__":
    v=Viterbi("hmm/model.txt")
    print(v.poccess(["i","want","four","month","to","chicago"]))