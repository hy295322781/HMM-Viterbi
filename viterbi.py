# -*- coding:utf-8 -*-
"""
Created on 2018-09-14 10:12:16

Author: Xiong Zecheng (295322781@qq.com)
"""
from prettytable import PrettyTable

class viterbi():
    observations = ('walk', 'shop', 'clean')
    states = ('Rainy', 'Sunny')
    start_probability = {'Rainy': 0.6, 'Sunny': 0.4}
    transition_probability = {
        'Rainy': {'Rainy': 0.7, 'Sunny': 0.3},
        'Sunny': {'Rainy': 0.4, 'Sunny': 0.6},
    }
    emission_probability = {
        'Rainy': {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
        'Sunny': {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
    }

    def __init__(self,*argv):
        if len(argv) == 1:
            self.observations = argv[0]
        elif len(argv)==5:
            self.observations = argv[0]
            self.states=argv[1]
            self.start_probability = argv[2]
            self.transition_probability = argv[3]
            self.emission_probability = argv[4]

    # 维特比算法 obs_seq-观测序列
    def poccess(self):
        # 隐状态序列
        hidden_state = []
        # 路径概率表
        v = []

        # 初始状态概率
        start_p = []
        start_max = -1
        max_start_state = ""
        for key in self.start_probability:
            p = self.start_probability[key] * self.emission_probability[key][self.observations[0]]
            start_p.append(p)
            if p > start_max:
                start_max = p
                max_start_state = key
        v.append(start_p)
        hidden_state.append(max_start_state)

        for obs in self.observations[1:]:
            state_p = []
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

        self.print_table(v)
        print(hidden_state)

    def print_table(self,v):
        table = PrettyTable()
        table.add_column("",list(self.states))
        for i in range(len(v)):
            table.add_column(str(i),list(map(lambda x:'%.5f'%x,v[i])))
        print(table)

if __name__ == "__main__":
    v=viterbi(("walk","clean","walk","shop","walk"))
    v.poccess()