# -*- coding:utf-8 -*-
"""
Created on 2018-09-23 19:58:47

Author: Xiong Zecheng (295322781@qq.com)
"""
class Model():
    def load_model(self):
        f = open("model.txt", "r")
        str_ob = f.readline().strip()
        str_st = f.readline().strip()
        str_sp = f.readline().strip()
        str_tp = f.readline().strip()
        str_ep = f.readline().strip()
        f.close()

        observations = tuple(str_ob.split(" "))
        states = tuple(str_st.split(" "))

        start_probability = dict()
        p_list = str_sp.split(" ")
        for i in range(len(p_list)):
            start_probability[states[i]] = float(p_list[i])

        transition_probability = dict()
        p_lists = str_tp.split(",")
        for i in range(len(p_lists)):
            p_list = p_lists[i].split(" ")
            d = dict()
            for j in  range(len(p_list)):
                d[states[j]] = float(p_list[j])
            transition_probability[states[i]] = d

        emission_probability = dict()
        p_lists = str_ep.split(",")
        for i in range(len(p_lists)):
            p_list = p_lists[i].split(" ")
            d = dict()
            for j in range(len(p_list)):
                d[observations[j]] = float(p_list[j])
            emission_probability[states[i]] = d

        return observations,states,start_probability,transition_probability,emission_probability