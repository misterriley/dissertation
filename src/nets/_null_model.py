'''
Created on Apr 12, 2021

@author: bleem
'''

import numpy

from nets import _constants


class NullModelQ(object):

    def __init__(self, hyperparams, null_environment, experiment_data):
        self.__last_output = None
        self.__last_action_index = None
        self.__null_environment = null_environment

        tc1_size = experiment_data.get_target_class_data(1).get_size()
        tc2_size = experiment_data.get_target_class_data(2).get_size()

        assert tc1_size == tc2_size

        env_size = 2 ** hyperparams.get_env_bits()
        self.q_values = numpy.zeros(int(env_size / tc2_size))

        self.__reinforcer_applied_to_last_action = False

    def get_max_value_action(self):
        max_indices = [i for i, x in enumerate(self.q_values) if x == max(self.q_values)]
        return numpy.random.choice(max_indices)

    def get_random_action(self):
        return numpy.random.choice(range(len(self.q_values)))

    def get_boltzmann_action(self, inverse_temp):
        likelihoods = numpy.exp((self.q_values - max(self.q_values)) * inverse_temp)
        probs = likelihoods / sum(likelihoods)
        return numpy.random.choice(range(len(self.q_values)), p = probs)

    def get_hyperbolic_action(self, constant, power):
        likelihoods = 1 / (1 + (constant * (max(self.q_values) - self.q_values))) ** power
        probs = likelihoods / sum(likelihoods)
        return numpy.random.choice(range(len(self.q_values)), p = probs)

    def get_linear_action(self, linear_constants):
        slope, cutoff = linear_constants
        x_vals = max(self.q_values) - self.q_values
        min_x = cutoff
        min_y = 1 + slope * cutoff

        likelihoods = numpy.where(x_vals < min_x, 1 + slope * (x_vals), min_y)
        probs = likelihoods / sum(likelihoods)
        return numpy.random.choice(range(len(self.q_values)), p = probs)

    def get_quadratic_action(self, abc_tuple):
        a, b, c = abc_tuple
        x_vals = max(self.q_values) - self.q_values
        min_x = -1 * b / (2 * a)
        min_y = a * min_x ** 2 + b * min_x + c

        likelihoods = numpy.where(x_vals < min_x, a * x_vals ** 2 + b * x_vals + c, min_y)
        probs = likelihoods / sum(likelihoods)
        return numpy.random.choice(range(len(self.q_values)), p = probs)

    def generate_output(self, hyperparams):
        self.__reinforcer_applied_to_last_action = False

        if hyperparams.get_policy_type() == _constants.POLICY_TYPE_MAX:
            self.__last_action_index = self.get_max_value_action()
        elif hyperparams.get_policy_type() == _constants.POLICY_TYPE_EPSILON_GREEDY:
            if numpy.random.random() < hyperparams.get_epsilon():
                self.__last_action_index = self.get_random_action()
            else:
                self.__last_action_index = self.get_max_value_action()
        elif hyperparams.get_policy_type() == _constants.POLICY_TYPE_BOLTZMANN:
            self.__last_action_index = self.get_boltzmann_action(hyperparams.get_inverse_temp())
        elif hyperparams.get_policy_type() == _constants.POLICY_TYPE_HYPERBOLIC:
            self.__last_action_index = self.get_hyperbolic_action(hyperparams.get_h_policy_constant(), hyperparams.get_h_policy_exponent())
        elif hyperparams.get_policy_type() == _constants.POLICY_TYPE_LINEAR:
            self.__last_action_index = self.get_linear_action(hyperparams.get_l_policy_tuple())
        elif hyperparams.get_policy_type() == _constants.POLICY_TYPE_QUADRATIC:
            self.__last_action_index = self.get_quadratic_action(hyperparams.get_q_policy_tuple())
        elif hyperparams.get_policy_type() == _constants.POLICY_TYPE_EPSILON_BOLTZMANN:
            if numpy.random.random() < hyperparams.get_epsilon():
                self.__last_action_index = self.get_random_action()
            else:
                self.__last_action_index = self.get_boltzmann_action(hyperparams.get_inverse_temp())
        else:
            assert False

        self.__last_output = self.convert_action_to_operant_index(self.__last_action_index)
        return self.__last_output

    def apply_reinforcer(self, hyperparams, operant):
        self.__reinforcer_applied_to_last_action = True
        self.update_q_value_of_last_action(operant.get_magnitude(_constants.NET_TYPE_NULL_Q), hyperparams)

    def update_q_value_of_last_action(self, rt, hyperparams):
        last_action = self.__last_action_index
        last_action_old_q = self.q_values[last_action]
        max_q = max(self.q_values)
        last_action_new_q = last_action_old_q + hyperparams.get_learning_rate() * (rt + hyperparams.get_discount_rate() * max_q - last_action_old_q)
        self.q_values[last_action] = last_action_new_q

    def apply_mutation(self, hyperparams):
        if not self.__reinforcer_applied_to_last_action:
            self.update_q_value_of_last_action(0, hyperparams)
            self.__reinforcer_applied_to_last_action = True

    def convert_action_to_operant_index(self, value):
        if value == 1 or value == 2:
            return value
        else:
            return 0


class NullModelMarkov(object):
    '''
    classdocs
    '''

    # This class is a simple Markov-chain approximation to the ETBD.
    # It contains three ranges of values, corresponding to two target classes and a set of non-target behaviors.
    # Emissions are either "1", "2" or "0" with probabilities determined by the relative size of the classes.
    # A reinforced behavior for a target class will increase the size of that class by adding a constant to the log-odds
    # that this class will be chosen at the next interval. A mutation event corresponds to multiplying the log-odds for that
    # target class by a positive constant less than one. The log-odds associated with each target class do not interact
    # with each other.
    #
    # This class implements the same usable methods as both Net and Environment.

    def __init__(self, hyperparams, null_environment):

        self.__last_output = None
        self.__mutation_rate = hyperparams.get_net_mutation_prob()
        self.__null_environment = null_environment

        tc1_size = null_environment.get_operant_for_tc_index(1).get_target_class().get_size()
        tc2_size = null_environment.get_operant_for_tc_index(2).get_target_class().get_size()

        self.__tc1_prob = self.__tc1_initial_prob = tc1_size / (2 ** hyperparams.get_env_bits())
        self.__tc2_prob = self.__tc2_initial_prob = tc2_size / (2 ** hyperparams.get_env_bits())

    def generate_output(self, _):
        rand = numpy.random.uniform()

        if rand < self.__tc1_prob:
            self.__last_output = 1
        elif rand < self.__tc1_prob + self.__tc2_prob:
            self.__last_output = 2
        else:
            self.__last_output = 0

        return self.__last_output

    def apply_reinforcer(self, _, operant):
        op_index = self.__null_environment.get_index_for_operant(operant)
        assert(op_index != 0)

        reinforcement_magnitude = operant.get_magnitude(_constants.NET_TYPE_NULL_MARKOV)
        suppression_magnitude = operant.get_nm_suppression()

        if op_index == 1:
            delta_1 = (1 - self.__tc1_prob)
            self.__tc1_prob = 1 - delta_1 * (1 - reinforcement_magnitude)
            self.__tc2_prob *= (1 - suppression_magnitude)
        elif op_index == 2:
            delta_2 = (1 - self.__tc2_prob)
            self.__tc2_prob = 1 - delta_2 * (1 - reinforcement_magnitude)

            self.__tc1_prob *= (1 - suppression_magnitude)

    def apply_mutation(self, hyperparams):
        excess_1 = self.__tc1_prob - self.__tc1_initial_prob
        excess_2 = self.__tc2_prob - self.__tc2_initial_prob

        self.__tc1_prob = self.__tc1_initial_prob + excess_1 * hyperparams.get_nm_mutation()
        self.__tc2_prob = self.__tc2_initial_prob + excess_2 * hyperparams.get_nm_mutation()
