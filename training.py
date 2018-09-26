# -*- coding:utf-8 -*-
"""
Created on 2018-09-21 16:21:48

Author: Xiong Zecheng (295322781@qq.com)
"""
import pickle
import numpy
from model import Model

class ATIS():
    def __init__(self,path):
        f = open(path, 'rb')
        try:
            self.train_set, self.valid_set, self.test_set, self.dicts = pickle.load(f, encoding='latin1')
        except:
            self.train_set, self.valid_set, self.test_set, self.dicts = pickle.load(f)
        f.close()

    def train(self):
        idx2words = {}
        idx2labels = {}
        for key, value in self.dicts["words2idx"].items():
            idx2words[value] = key;
        for key, value in self.dicts["labels2idx"].items():
            idx2labels[value] = key;

        observations = list(self.dicts["words2idx"].keys())
        states = list(self.dicts["labels2idx"].keys())
        states_num = len(states)
        observations_num = len(observations)

        start_probability = list()
        total = 0
        for i in range(states_num):
            start_probability.append(0)
        for state_seq in self.train_set[2]:
            start_probability[states.index(idx2labels[state_seq[0]])] += 1
            total += 1
        for i in range(states_num):
            start_probability[i] /= total

        transition_probability = numpy.zeros((states_num, states_num))
        for state_seq in self.train_set[2]:
            for i in range(state_seq.size - 1):
                transition_probability[
                    states.index(idx2labels[state_seq[i]]), states.index(idx2labels[state_seq[i + 1]])] += 1
        for row in transition_probability:
            if sum(row) != 0:
                row /= sum(row)

        emission_probability = numpy.zeros((states_num, observations_num))
        for i in range(len(self.train_set[2])):
            for j in range(len(self.train_set[2][i])):
                emission_probability[states.index(idx2labels[self.train_set[2][i][j]]),
                                     observations.index(idx2words[self.train_set[0][i][j]])] += 1
        for row in emission_probability:
            if sum(row) != 0:
                row /= sum(row)

        model = Model()
        model.build_model(observations,states,start_probability,transition_probability,emission_probability)
        print("training success")

if __name__ == "__main__":
    atis = ATIS("data/atis.fold0.pkl")
    atis.train()