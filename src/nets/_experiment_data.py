'''
Created on Apr 5, 2021

@author: bleem
'''


class ExperimentData(object):
    '''
    classdocs
    '''

    def __init__(self, run_duration, burn_in, run_repetitions, net_type, mutation_rate, sequential):
        self.__run_duration = run_duration
        self.__burn_in = burn_in
        self.__run_repetitions = run_repetitions
        self.__net_type = net_type
        self.__mutation_rate = mutation_rate
        self.__sequential = sequential

        self.__target_classes = {}
        self.__runs = []

    def get_mutation_rate(self):
        return self.__mutation_rate

    def get_run_duration(self):
        return self.__run_duration

    def get_run_repititions(self):
        return self.__run_repetitions

    def get_net_type(self):
        return self.__net_type

    def set_target_class_data(self, index, value):
        self.__target_classes[index] = value

    def get_target_class_data(self, index):
        return self.__target_classes[index]

    def get_target_classes(self):
        return self.__target_classes

    def add_run(self, run_data):
        self.__runs.append(run_data)

    def get_runs(self):
        return self.__runs

    def get_burn_in(self):
        return self.__burn_in

    def is_sequential(self):
        return self.__sequential

