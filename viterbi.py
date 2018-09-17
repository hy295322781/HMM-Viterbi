# -*- coding:utf-8 -*-
"""
Created on 2018-09-14 10:12:16

Author: Xiong Zecheng (295322781@qq.com)
"""
states = ('Rainy', 'Sunny')

observations = ('walk', 'shop', 'clean')

start_probability = {'Rainy': 0.6, 'Sunny': 0.4}

transition_probability = {
    'Rainy': {'Rainy': 0.7, 'Sunny': 0.3},
    'Sunny': {'Rainy': 0.4, 'Sunny': 0.6},
}

emission_probability = {
    'Rainy': {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
    'Sunny': {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
}

#维特比算法 obs_seq-观测序列
def viterbi(obs_seq):
    #隐状态序列
    hidden_state=[]
    #路径概率表
    v=[]

    #初始状态概率
    start_p=[]
    start_max=-1
    max_start_state=""
    for key in start_probability:
        p=start_probability[key]*emission_probability[key][obs_seq[0]]
        start_p.append(p)
        if p>start_max:
            start_max=p
            max_start_state=key
    v.append(start_p)
    hidden_state.append(max_start_state)

    for obs in obs_seq[1:]:
        state_p=[]
        max=-1
        max_state = ""
        for state in states:
            transited_p=0
            for i in range(len(states)):
                transited_p+=v[-1][i]*transition_probability[states[i]][state]
            p=transited_p*emission_probability[state][obs]
            state_p.append(p)
            if p > max:
                max = p
                max_state = state
        v.append(start_p)
        hidden_state.append(max_state)

    return hidden_state

if __name__ == "__main__":
    print(viterbi(["shop","shop","clean"]))