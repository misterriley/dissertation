'''
Created on Mar 22, 2021

@author: bleem
'''

import multiprocessing

from nets import _constants


class Hyperparams(object):

    __NET_OUTPUT_NODES = 10
    __ENV_BITS = __NET_OUTPUT_NODES

    # corresponds to the population size in the ETBD
    __NET_HIDDEN_NODES = 100

    __NET_ONE_NUM_FIRING_HIDDEN_NODES = 2

    __NET_MUTATION_PROB = .10  # value from the ETBD; only used for calculating constants for nets

    __NET_TWO_HIDDEN_NODE_FIRING_PROB = .05

    __NUM_HELPER_THREADS = multiprocessing.cpu_count()
    __RUN_MULTITHREADED = True

    # Only used for the Q-type null agent
    __POLICY_TYPE = _constants.POLICY_TYPE_EPSILON_GREEDY
    __LEARNING_RATE = 0.9
    __DISCOUNT_RATE = 0.99

    # Parameter for epsilon-greedy policy
    __EPSILON = 0.14
    # Parameter for Boltzmann policy
    __INVERSE_TEMP = 1.888
    # Parameter for hyperbolic policy
    __H_POLICY_CONSTANT = 164
    __H_POLICY_EXPONENT = 0.777
    # Parameter for linear policy
    __L_POLICY_MIN_POINT = (.6, .1)
    # Parameters for quadratic policy
    __Q_POLICY_MIN_POINT = (.012, .023)

    __NM_MAGNITUDE_CONST = 2
    __NM_SUPPRESSION_CONST = 81
    __NET_ONE_MAGNITUDE_CONST = 12.5
    __NET_TWO_MAGNITUDE_CONST = 6.8
    __NET_TWO_MAGNITUDE_MULTIPLIER = 0.037

    __NET_ONE_MUTATION_MULTIPLIER = 1

    def __init__(self):

        self.__nm_mutation = 0  # Hyperparams.__NM_MUTATION
        self.__net_mutation_prob = 0  # Hyperparams.__NET_MUTATION_PROB
        self.__net_one_mutation_prob = 0  # Hyperparams.__NET_ONE_MUTATION_PROB
        self.__net_one_mutation_multiplier = Hyperparams.__NET_ONE_MUTATION_MULTIPLIER
        self.__net_two_mutation_strength = 0  # Hyperparams.__NET_TWO_MUTATION_STRENGTH

        self.__net_output_nodes = Hyperparams.__NET_OUTPUT_NODES
        self.__env_bits = Hyperparams.__ENV_BITS
        self.__net_hidden_nodes = Hyperparams.__NET_HIDDEN_NODES
        self.__net_one_num_firing_hidden_nodes = Hyperparams.__NET_ONE_NUM_FIRING_HIDDEN_NODES
        self.__net_two_hidden_node_firing_prob = Hyperparams.__NET_TWO_HIDDEN_NODE_FIRING_PROB
        self.__num_helper_threads = Hyperparams.__NUM_HELPER_THREADS
        self.__run_multithreaded = Hyperparams.__RUN_MULTITHREADED
        self.__epsilon = Hyperparams.__EPSILON
        self.__inverse_temp = Hyperparams.__INVERSE_TEMP
        self.__policy_type = Hyperparams.__POLICY_TYPE
        self.__learning_rate = Hyperparams.__LEARNING_RATE
        self.__discount_rate = Hyperparams.__DISCOUNT_RATE
        self.__h_policy_constant = Hyperparams.__H_POLICY_CONSTANT
        self.__h_policy_exponent = Hyperparams.__H_POLICY_EXPONENT
        self.__l_policy_slope = 0
        self.__l_policy_cutoff = 0
        self.set_l_policy_min_point(Hyperparams.__L_POLICY_MIN_POINT)

        self.__q_policy_min_point = None
        self.__q_policy_a = 0
        self.__q_policy_b = 0
        self.__q_policy_c = 0
        self.set_q_policy_min_point(Hyperparams.__Q_POLICY_MIN_POINT)

        self.__nm_magnitude_const = Hyperparams.__NM_MAGNITUDE_CONST
        self.__nm_suppression_const = Hyperparams.__NM_SUPPRESSION_CONST
        self.__net_two_magnitude_const = Hyperparams.__NET_TWO_MAGNITUDE_CONST
        self.__net_two_magnitude_multiplier = Hyperparams.__NET_TWO_MAGNITUDE_MULTIPLIER
        self.__net_one_magnitude_const = Hyperparams.__NET_ONE_MAGNITUDE_CONST

        self.set_mutation_rate(Hyperparams.__NET_MUTATION_PROB)

    def get_net_one_mutation_multiplier(self):
        return self.__net_one_mutation_multiplier

    def set_net_one_mutation_multiplier(self, value):
        self.__net_one_mutation_multiplier = value

    def get_net_one_magnitude_const(self):
        return self.__net_one_magnitude_const

    def set_net_one_magnitude_const(self, value):
        self.__net_one_magnitude_const = value

    def get_nm_magnitude_const(self):
        return self.__nm_magnitude_const

    def get_nm_suppression_const(self):
        return self.__nm_suppression_const

    def get_net_two_magnitude_const(self):
        return self.__net_two_magnitude_const

    def get_net_two_magnitude_multiplier(self):
        return self.__net_two_magnitude_multiplier

    def set_nm_magnitude_const(self, value):
        self.__nm_magnitude_const = value

    def set_nm_suppression_const(self, value):
        self.__nm_suppression_const = value

    def set_net_two_magnitude_const(self, value):
        self.__net_two_magnitude_const = value

    def set_net_two_magnitude_multiplier(self, value):
        self.__net_two_magnitude_multiplier = value

    def get_q_policy_tuple(self):
        return (self.__q_policy_a, self.__q_policy_b, self.__q_policy_c)

    def set_q_policy_min_point(self, point):
        point_x, point_y = point
        self.__q_policy_c = 1
        self.__q_policy_a = (1 - point_y) / (point_x ** 2)
        self.__q_policy_b = -2 * point_x * self.__q_policy_a

    def get_l_policy_tuple(self):
        return (self.__l_policy_slope, self.__l_policy_cutoff)

    def set_l_policy_min_point(self, point):
        point_x, point_y = point
        self.__l_policy_slope = (point_y - 1) / point_x
        self.__l_policy_cutoff = point_x

    def get_h_policy_exponent(self):
        return self.__h_policy_exponent

    def set_h_policy_exponent(self, value):
        self.__h_policy_exponent = value

    def get_h_policy_constant(self):
        return self.__h_policy_constant

    def set_h_policy_constant(self, value):
        self.__h_policy_constant = value

    def get_discount_rate(self):
        return self.__discount_rate

    def set_discount_rate(self, value):
        self.__discount_rate = value

    def get_learning_rate(self):
        return self.__learning_rate

    def set_learning_rate(self, value):
        self.__learning_rate = value

    def get_policy_type(self):
        return self.__policy_type

    def set_policy_type(self, value):
        self.__policy_type = value

    def get_epsilon(self):
        return self.__epsilon

    def get_inverse_temp(self):
        return self.__inverse_temp

    def set_epsilon(self, value):
        self.__epsilon = value

    def set_inverse_temp(self, value):
        self.__inverse_temp = value

    def set_run_multithreaded(self, value):
        self.__run_multithreaded = value

    def run_multithreaded(self):
        return self.__run_multithreaded

    def set_mutation_rate(self, value):
        self.__net_mutation_prob = value
        self.__nm_mutation = 1 - value / (self.get_net_output_nodes() / 2)
        self.__net_one_mutation_prob = value * self.__net_one_mutation_multiplier / self.get_net_output_nodes()
        # print(self.__net_one_mutation_prob)
        self.__net_two_mutation_strength = self.get_nm_mutation()

    def get_nm_nt_suppression(self):
        return self.__nm_nt_suppression

    def set_nm_nt_suppression(self, value):
        self.__nm_nt_suppression = value

    def get_nm_mutation(self):
        return self.__nm_mutation

    def set_nm_mutation(self, value):
        self.__nm_mutation = value

    def get_experiment_list_file(self):
        return self.__experiment_list_file

    def set_experiment_list_file(self, value):
        self.__experiment_list_file = value

    def get_net_output_nodes(self):
        return self.__net_output_nodes

    def get_env_bits(self):
        return self.__env_bits

    def get_net_hidden_nodes(self):
        return self.__net_hidden_nodes

    def get_net_one_num_firing_hidden_nodes(self):
        return self.__net_one_num_firing_hidden_nodes

    def get_net_mutation_prob(self):
        return self.__net_mutation_prob

    def get_net_one_mutation_prob(self):
        return self.__net_one_mutation_prob

    def get_net_two_mutation_strength(self):
        return self.__net_two_mutation_strength

    def get_net_two_hidden_node_firing_prob(self):
        return self.__net_two_hidden_node_firing_prob

    def get_num_helper_threads(self):
        return self.__num_helper_threads

    def set_net_output_nodes(self, value):
        self.__net_output_nodes = value

    def set_env_bits(self, value):
        self.__env_bits = value

    def set_net_hidden_nodes(self, value):
        self.__net_hidden_nodes = value

    def set_net_one_num_firing_hidden_nodes(self, value):
        self.__net_one_num_firing_hidden_nodes = value

    def set_net_mutation_prob(self, value):
        self.__net_mutation_prob = value

    def set_net_one_mutation_prob(self, value):
        self.__net_one_mutation_prob = value

    def set_net_two_mutation_strength(self, value):
        self.__net_two_mutation_strength = value

    def set_net_two_hidden_node_firing_prob(self, value):
        self.__net_two_hidden_node_firing_prob = value

    def set_num_helper_threads(self, value):
        self.__num_helper_threads = value

