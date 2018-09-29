# -*- coding:utf-8 -*-
"""
Created on 2018-09-23 19:58:47

Author: Xiong Zecheng (295322781@qq.com)
"""
class Model():
    def load_model(self,path):
        f = open(path, "r")
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

    def build_model(self,path,observations,states,start_probability,transition_probability,emission_probability):
        f = open(path, 'w')
        f.write(" ".join(observations) + "\n")
        f.write(" ".join(states) + "\n")

        f.write(str(start_probability[0]))
        for p in start_probability[1:]:
            f.write(" " + str(p))
        f.write("\n")

        f.write(str(transition_probability[0, 0]))
        for p in transition_probability[0, 1:]:
            f.write(" " + str(p))
        for p_line in transition_probability[1:]:
            f.write("," + str(p_line[0]))
            for p in p_line[1:]:
                f.write(" " + str(p))
        f.write("\n")

        f.write(str(emission_probability[0, 0]))
        for p in emission_probability[0, 1:]:
            f.write(" " + str(p))
        for p_line in emission_probability[1:]:
            f.write("," + str(p_line[0]))
            for p in p_line[1:]:
                f.write(" " + str(p))

if __name__ == "__main__":
    m = Model()
    model = m.load_model("model.txt")
    d = dict()
    for key in model[3]:
        dd = dict()
        for inkey in model[3][key]:
            if model[3][key][inkey]!=0:
                dd[inkey]=model[3][key][inkey]
        d[key]=dd
    for key in d:
        print(key+":",end="")
        print(d[key])