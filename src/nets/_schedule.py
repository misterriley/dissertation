'''
Created on Mar 22, 2021

@author: bleem
'''

from numpy import random

from nets import _constants
from nets._target_class import TargetClass


class Schedule(object):
    '''
    classdocs
    '''

    def __init__(self, schedule_type, schedule_scale, target_class_index, target_class_min, target_class_max, FDF, hyperparams):
        self.schedule_type = schedule_type
        self.schedule_scale = schedule_scale
        self.next_scheduled_consequence = 0
        self.last_obtained_consequence = 0
        self.set_up_next_consequence()

        self.__target_class = TargetClass(target_class_index, target_class_min, target_class_max, hyperparams)
        self.__FDF = FDF
        self.__reinforcers = 0
        self.__num_behaviors = 0

        self.__nm_magnitude = hyperparams.get_nm_magnitude_const() / (hyperparams.get_nm_magnitude_const() + self.__FDF)
        self.__nm_suppression = hyperparams.get_nm_suppression_const() / (hyperparams.get_nm_suppression_const() + self.__FDF)
        self.__net_one_magnitude = hyperparams.get_net_one_magnitude_const() / (hyperparams.get_net_one_magnitude_const() + self.__FDF)
        self.__net_two_magnitude = (hyperparams.get_net_two_magnitude_const() / (hyperparams.get_net_two_magnitude_const() + self.__FDF)) / (2 * hyperparams.get_net_hidden_nodes() * (hyperparams.get_net_two_hidden_node_firing_prob() ** 2))
        self.__nq_magnitude = 40 / self.__FDF

    def get_schedule_type(self):
        return self.schedule_type

    def get_schedule_scale(self):
        return self.schedule_scale

    def set_up_next_consequence(self):
        self.next_scheduled_consequence = (random.exponential(self.schedule_scale) + self.last_obtained_consequence)

    def get_consequence(self, time_index = 0):

        comparison_point = 0
        self.__num_behaviors += 1

        if self.schedule_type == _constants.SCHEDULE_TYPE_VI:
            comparison_point = time_index
        elif self.schedule_type == _constants.SCHEDULE_TYPE_VR:
            comparison_point = self.__num_behaviors
        else:
            assert False

        ret = False
        if comparison_point >= self.next_scheduled_consequence:
            self.last_obtained_consequence = comparison_point
            self.set_up_next_consequence()
            ret = True
        return ret

    def get_FDF(self):
        return self.__FDF

    def get_schedule(self):
        return self.__schedule

    def get_target_class(self):
        return self.__target_class

    def get_magnitude(self, net_type):
        if net_type == _constants.NET_TYPE_ONE:
            return self.__net_one_magnitude
        elif net_type == _constants.NET_TYPE_TWO:
            return self.__net_two_magnitude
        elif net_type == _constants.NET_TYPE_NULL_MARKOV:
            return self.__nm_magnitude
        elif net_type == _constants.NET_TYPE_NULL_Q:
            return self.__nq_magnitude

    def get_nm_suppression(self):
        return self.__nm_suppression


if __name__ == '__main__':
        # print("Schedule created")
        schedule = Schedule(_constants.SCHEDULE_TYPE_VR, 60)
        for tick in range(10000):
            behavior_in_range = random.uniform() < .1
            if behavior_in_range:
                print("hit " + str(schedule.get_consequence(tick)))
            else:
                print("miss")

        print("behaviors: " + str(schedule.get_num_behaviors()))
        print("consequences: " + str(schedule.get_num_consequences()))
