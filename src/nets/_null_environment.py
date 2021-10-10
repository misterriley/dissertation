'''
Created on May 10, 2021

@author: bleem
'''

from nets._abstract_environment import AbstractEnvironment


class NullEnvironment(AbstractEnvironment):
    '''
    classdocs
    '''

    def __init__(self, repetition_index):
        super().__init__(repetition_index)

    def get_mutation_rate(self):
        return None

    def set_mutation_rate(self, _):
        pass

    def get_tc_index_for_behavior(self, behavior, _):
        if behavior == 1 or behavior == 2:
            return behavior
        return None
