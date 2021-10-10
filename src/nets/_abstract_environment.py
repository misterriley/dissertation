'''
Created on May 20, 2021

@author: bleem
'''

from nets._behavior_record import BehaviorRecord


class AbstractEnvironment(object):
    '''
    classdocs
    '''

    def __init__(self, repetition_index):
        self.__repetition_index = repetition_index

        self.__net_type = None

        self.__behavior_record = None
        self.__schedules = {0: None}
        self.__runs = []

    def get_mutation_rate(self):
        raise ValueError()

    def set_mutation_rate(self, _):
        raise ValueError()

    def set_net_type(self, net_type):
        self.__net_type = net_type

    def get_schedule(self, index):
        return self.__schedules.get(index, None)

    def get_net_type(self):
        return self.__net_type

    def get_behavior_record(self):
        return self.__behavior_record

    def put_new_behavior_record(self, run_data):
        self.__behavior_record = BehaviorRecord(run_data, self.__schedules[1], self.__schedules[2], self)

    def set_schedule(self, tc_index, schedule):
        self.__schedules[tc_index] = schedule

    def get_tc_index_for_behavior(self, bitfield, hyperparams):
        raise ValueError()

    def get_schedule_for_tc_index(self, tc_index):
        return self.__schedules[tc_index]

    def get_repetition_index(self):
        return self.__repetition_index

    def add_run(self, run_data):
        self.__runs.append(run_data)

    def get_runs(self):
        return self.__runs

    def get_run(self, index):
        return self.__runs[index]

    def get_schedule_for_behavior(self, output, _):
        return self.__schedules.get(output)

