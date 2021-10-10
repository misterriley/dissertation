'''
Created on Apr 6, 2021

@author: bleem
'''
# an experiment consists of multiple runs; each run consists of an environment with one or more operants that persists until a condition is met


class RunData(object):
    '''
    classdocs
    '''

    def __init__(self, run_index):
        self.__schedules = {}
        self.__run_index = run_index

    def set_schedule(self, index, value):
        self.__schedules[index] = value

    def get_schedule(self, index):
        return self.__schedules[index]

    def get_run_index(self):
        return self.__run_index

