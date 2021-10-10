'''
Created on May 19, 2021

@author: bleem
'''

import numpy


class BehaviorRecord(object):
    '''
    classdocs
    '''

    def __init__(self, run_data, schedule1, schedule2, environment):
        self.__b1 = 0
        self.__b2 = 0
        self.__r1 = 0
        self.__r2 = 0
        self.__changeovers = 0

        self.__environment = environment
        self.__run_data = run_data
        self.__schedule1 = schedule1
        self.__schedule2 = schedule2

        assert type(run_data).__name__ == "RunData"

    def get_schedule(self, index):
        if index == 1:
            return self.__schedule1
        elif index == 2:
            return self.__schedule2
        assert False

    def get_run_data(self):
        return self.__run_data

    def get_environment(self):
        return self.__environment

    def get_log_B1_over_B2(self):
        if self.__b1 * self.__b2 == 0: return None
        return numpy.log10(self.__b1 / self.__b2)

    def get_log_R1_over_R2(self):
        if self.__r1 * self.__r2 == 0: return None
        return numpy.log10(self.__r1 / self.__r2)

    def get_log_M1_over_M2(self):
        fdf1 = self.get_schedule(1).get_FDF()
        fdf2 = self.get_schedule(2).get_FDF()
        return numpy.log10(fdf2 / fdf1)

    def get_FDF(self, tc_index):
        return self.get_schedule(tc_index).get_FDF()

    def increment_changeovers(self):
        self.__changeovers += 1

    def get_changeovers(self):
        return self.__changeovers

    def increment_reinforcers(self, tc_index):
        if tc_index == 1:
            self.__r1 += 1
        elif tc_index == 2:
            self.__r2 += 1
        else:
            assert False

    def increment_behaviors(self, tc_index):
        if tc_index == 1:
            self.__b1 += 1
        elif tc_index == 2:
            self.__b2 += 1
        else:
            assert False

    def get_reinforcers(self, tc_index):
        if tc_index == 1:
            return self.__r1
        elif tc_index == 2:
            return self.__r2
        else:
            assert False
        return self.__reinforcers

    def get_behaviors(self, tc_index):
        if tc_index == 1:
            return self.__b1
        elif tc_index == 2:
            return self.__b2
        else:
            assert False
