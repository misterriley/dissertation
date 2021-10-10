'''
Created on May 20, 2021

@author: bleem
'''

import numpy


class ETBD(object):
    '''
    classdocs
    '''

    POPULATION_SIZE = 100

    def __init__(self, hyperparams):
        self.__behaviors = numpy.random.binomial(1, .5, size = (ETBD.POPULATION_SIZE, hyperparams.get_net_output_nodes()))
        self.__children = numpy.zeros(shape = self.__behaviors.shape, dtype = int)
        self.__last_output = None
        self.__distance_buffer = numpy.zeros(shape = (2 ** (hyperparams.get_net_output_nodes() + 1)), dtype = int)
        self.__likelihoods_buffer = numpy.zeros(shape = (ETBD.POPULATION_SIZE))

    def generate_output(self, _):
        rand_index = numpy.random.randint(ETBD.POPULATION_SIZE)
        self.__last_output = self.__behaviors[rand_index]
        return self.__last_output

    def apply_mutation(self, hyperparams):
        mutation_bools = numpy.random.binomial(n = 1, p = hyperparams.get_net_mutation_prob(), size = ETBD.POPULATION_SIZE)

        for behavior_index in range(ETBD.POPULATION_SIZE):
            if mutation_bools[behavior_index] == 1:
                bit_index = numpy.random.randint(hyperparams.get_net_output_nodes())
                bit_val = self.__behaviors[behavior_index, bit_index]
                self.__behaviors[behavior_index, bit_index] = 1 - bit_val

    def apply_reinforcer(self, hyperparams, schedule):
        center = self.__last_output
        fdf = schedule.get_FDF()
        linear_term = -2 / (9 * fdf * fdf)
        constant_term = 2 / (3 * fdf)

        self.__distance_buffer[:-1] = 0
        self.__likelihoods_buffer[:-1] = 0

        # this is going to be called a lot - better cache it
        pop_range = numpy.arange(ETBD.POPULATION_SIZE)
        offset = int(len(self.__distance_buffer) / 2)

        for behavior_index in pop_range:
            behavior = self.__behaviors[behavior_index]
            diff = self.get_phenotype_diff(center, behavior, hyperparams)
            buffer_index = diff + offset
            if self.__distance_buffer[buffer_index] == 0:
                self.__distance_buffer[buffer_index] = 1
                likelihood = max(0, constant_term + linear_term * abs(diff))
                self.__likelihoods_buffer[behavior_index] = likelihood

        self.__likelihoods_buffer /= sum(self.__likelihoods_buffer)

        for child_index in pop_range:
            parent_indices = numpy.random.choice(pop_range, size = 2, replace = False, p = self.__likelihoods_buffer)
            muddah = self.__behaviors[parent_indices[0]]
            faddah = self.__behaviors[parent_indices[1]]

            rands = numpy.random.binomial(n = 1, p = .5, size = hyperparams.get_net_output_nodes())
            child = numpy.where(rands == 1, muddah, faddah)
            self.__children[child_index] = child

        self.__behaviors = self.__children

    def get_phenotype_diff(self, b1, b2, hyperparams):
        diff = 0
        multiplier = 1
        for i in range(hyperparams.get_net_output_nodes()):
            b1val = b1[-(i + 1)]
            b2val = b2[-(i + 1)]
            diff += (b1val - b2val) * multiplier
            multiplier <<= 1

        return diff
