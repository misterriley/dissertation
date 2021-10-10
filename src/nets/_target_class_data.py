'''
Created on Apr 6, 2021

@author: bleem
'''


class TargetClassData(object):
    '''
    classdocs
    '''

    def __init__(self, target_class_index, min_, max_, schedule_type):
        self.__target_class_index = target_class_index
        self.__min = min_
        self.__max = max_
        self.__schedule_type = schedule_type

    def get_min(self):
        return self.__min

    def get_max(self):
        return self.__max

    def get_schedule_type(self):
        return self.__schedule_type

    def get_target_class_index(self):
        return self.__target_class_index

    def get_size(self):
        return self.__max - self.__min + 1
