'''
Created on Apr 6, 2021

@author: bleem
'''


class ScheduleData(object):
    '''
    classdocs
    '''

    def __init__(self, schedule_index, scale, FDF):
        self.__schedule_index = schedule_index
        self.__scale = scale
        self.__FDF = FDF

    def get_scale(self):
        return self.__scale

    def get_FDF(self):
        return self.__FDF

    def get_schedule_index(self):
        return self.__schedule_index
