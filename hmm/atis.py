# -*- coding:utf-8 -*-
"""
Created on 2018-09-21 16:21:48

Author: Xiong Zecheng (295322781@qq.com)
"""
import pickle
import numpy
from hmm.model import Model
from viterbi import Viterbi

class ATIS():
    def __init__(self,path):
        f = open(path, 'rb')
        try:
            self.train_set, self.valid_set, self.test_set, self.dicts = pickle.load(f, encoding='latin1')
        except:
            self.train_set, self.valid_set, self.test_set, self.dicts = pickle.load(f)
        f.close()
        self.__idx2words = dict()
        self.__idx2labels = dict()
        for key, value in self.dicts["words2idx"].items():
            self.__idx2words[value] = key;
        for key, value in self.dicts["labels2idx"].items():
            self.__idx2labels[value] = key;

    def train(self):
        observations = list(self.dicts["words2idx"].keys())
        states = list(self.dicts["labels2idx"].keys())
        states_num = len(states)
        observations_num = len(observations)

        start_probability = list()
        total = 0
        for i in range(states_num):
            start_probability.append(0)
        for state_seq in self.train_set[2]:
            start_probability[states.index(self.__idx2labels[state_seq[0]])] += 1
            total += 1
        for i in range(states_num):
            start_probability[i] /= total

        transition_probability = numpy.zeros((states_num, states_num))
        for state_seq in self.train_set[2]:
            for i in range(state_seq.size - 1):
                transition_probability[
                    states.index(self.__idx2labels[state_seq[i]]), states.index(self.__idx2labels[state_seq[i + 1]])] += 1
        for row in transition_probability:
            if sum(row) != 0:
                row /= sum(row)

        emission_probability = numpy.zeros((states_num, observations_num))
        for i in range(len(self.train_set[2])):
            for j in range(len(self.train_set[2][i])):
                emission_probability[states.index(self.__idx2labels[self.train_set[2][i][j]]),
                                     observations.index(self.__idx2words[self.train_set[0][i][j]])] += 1
        for row in emission_probability:
            if sum(row) != 0:
                row /= sum(row)

        model = Model()
        model.build_model("model.txt",observations,states,start_probability,transition_probability,emission_probability)
        print("training success")

    def test(self):
        v = Viterbi("model.txt")
        predicted_slot_count = 0
        actual_slot_count = 0
        hit_count = 0
        test_set_size = len(self.test_set[0])

        print("poccessing...")
        for i in range(test_set_size):
            if i!=0 and i%100==0:
                print(str(i)+" done")
            sentence = list()
            for wordidx in self.test_set[0][i]:
                sentence.append(self.__idx2words[wordidx])
            predicted_seq = v.poccess(sentence)
            predicted_slot = extract_slot(predicted_seq)

            label_seq = list()
            for labelidx in self.test_set[2][i]:
                label_seq.append(self.__idx2labels[labelidx])
            actual_slot = extract_slot(label_seq)

            for item in predicted_slot:
                if item in actual_slot:
                    hit_count += 1
            predicted_slot_count += len(predicted_slot)
            actual_slot_count += len(actual_slot)

        print("test set size:"+str(test_set_size))
        print("predicted slot:"+str(predicted_slot_count)+" actual slot:"+str(actual_slot_count)+" hit:"+str(hit_count))
        print("Precision:"+str(hit_count/predicted_slot_count))
        print("Recall:" + str(hit_count / actual_slot_count))
        print("F1score:" + str(2*hit_count / (actual_slot_count+predicted_slot_count)))

def extract_slot(seq):
    slot = list()
    i = 0
    while i < len(seq):
        if seq[i].startswith("B"):
            slot_type = seq[i][2:]
            l = 1
            while i + l < len(seq) and seq[i + l] == "I-" + slot_type:
                l += 1
            slot.append((i,slot_type,l))  # (槽的位置,槽的类型,槽的长度)
            i = i + l
        else:
            i += 1
    return slot

if __name__ == "__main__":
    atis = ATIS("../data/atis.fold0.pkl")
    # atis.train()
    atis.test()