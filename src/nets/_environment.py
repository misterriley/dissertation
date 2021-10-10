'''
Created on Mar 22, 2021

@author: bleem
'''

from nets._abstract_environment import AbstractEnvironment


class Environment(AbstractEnvironment):
    '''
    classdocs
    '''

    def __init__(self, repetition_index):
        super().__init__(repetition_index)
        self.__mutation_rate = None

    def get_mutation_rate(self):
        return self.__mutation_rate

    def set_mutation_rate(self, value):
        self.__mutation_rate = value

    def get_tc_index_for_behavior(self, bitfield, hyperparams):
        for tc_index in [1, 2]:
            schedule = self.get_schedule(tc_index)
            if schedule is not None and schedule.get_target_class().contains_bitfield(bitfield, hyperparams):
                return tc_index

        return None

