'''
Created on Mar 22, 2021

@author: bleem
'''

from timeit import default_timer as timer

import numpy

from nets import _constants
from nets._hyperparams import Hyperparams


class Net(object):
    '''
    classdocs
    '''

    def __init__(self, net_type, hyperparams):

        # indicator of the type of net; type one is a binary synapse valued Boltzmann machine with a step activation function
        # type two has real valued synapses and a logistic activation function
        self.net_type = net_type

        # real-valued synapse matrix, dimension is h x o (h = num hidden, o = num output)
        synapse_matrix_shape = (hyperparams.get_net_hidden_nodes(), hyperparams.get_net_output_nodes())
        if self.net_type == _constants.NET_TYPE_ONE:
            # the type one net should be randomized to have 1s and -1s in the synapse array
            self.synapses = 2 * numpy.random.binomial(1, .5, size = synapse_matrix_shape) - 1
        elif self.net_type == _constants.NET_TYPE_TWO:
            # the type two net should have zeroes everywhere
            self.synapses = numpy.zeros(synapse_matrix_shape, dtype = float)
        else:
            self.assertFalse()

        # initialize the hidden and output nodes to zero
        self.hidden_nodes = numpy.zeros(hyperparams.get_net_hidden_nodes(), dtype = float)
        self.output_nodes = numpy.zeros(hyperparams.get_net_output_nodes(), dtype = float)

        # an internal array for use in matrix multiplication
        self.raw_outputs = numpy.zeros(hyperparams.get_net_output_nodes(), dtype = float)

    def get_net_type(self):
        return self.net_type

    def generate_output(self, hyperparams):
        # first generate a random set of hidden neurons to fire according to the rules of the network
        self.generate_hiddens(hyperparams)

        # now build the raw outputs, which will then be passed through the activation function
        numpy.matmul(self.hidden_nodes, self.synapses, out = self.raw_outputs)

        if self.net_type == _constants.NET_TYPE_ONE:
            # lambda functions with explicit logical operators don't work when applied
            # across an array, so we must use numpy.where()
            #
            # the activation for net one is a step function
            # y = 1  if x > 0
            # y = .5 if x == 0
            # y = 0  if x < 0
            activation = lambda x: numpy.where(x > 0, 1, numpy.where(x < 0, 0, .5))

        elif self.net_type == _constants.NET_TYPE_TWO:
            # logistic sigmoid activation function for net two
            # the -4 creates a derivative of y'= 1 at x = 0, which simplifies the math elsewhere
            activation = lambda x: 1 / (1 + numpy.exp(-4 * x))

        else:
            self.assertFalse()

        # now apply the activation function to the raw output and fire based on these probabilities
        probs = activation(self.raw_outputs)
        rands = numpy.random.uniform(size = hyperparams.get_net_output_nodes())
        self.output_nodes = (probs > rands).astype(int)
        return self.output_nodes

    def generate_hiddens(self, hyperparams):

        if self.net_type == _constants.NET_TYPE_ONE:

            # for type one, we have exactly two nodes that fire
            self.hidden_nodes.fill(0)
            on_bits = numpy.random.choice(range(len(self.hidden_nodes)), hyperparams.get_net_one_num_firing_hidden_nodes(), replace = False)
            self.hidden_nodes[on_bits] = 1

        elif self.net_type == _constants.NET_TYPE_TWO:

            # for type two, each node fires independently
            while(True):
                self.hidden_nodes = numpy.random.binomial(1, hyperparams.get_net_two_hidden_node_firing_prob(), size = hyperparams.get_net_hidden_nodes())

                # ensure that there's at least one hidden node fired
                if sum(self.hidden_nodes) > 0:
                    break

        else:
            self.assertFalse()

    def apply_reinforcer(self, hyperparams, schedule, output = None, hiddens = None, apply_mutation = False):

        if output == None:
            output = self.output_nodes

        if hiddens == None:
            hiddens = self.hidden_nodes

        if self.net_type == _constants.NET_TYPE_ONE:

            # for net type one, reinforcement probabilistically flips some synapses toward the output
            target_weights = numpy.array([2 * output - 1, ] * hyperparams.get_net_hidden_nodes())
            rands = numpy.random.uniform(size = target_weights.shape)
            self.synapses = numpy.where(rands < schedule.get_magnitude(_constants.NET_TYPE_ONE), target_weights, self.synapses)

        elif self.net_type == _constants.NET_TYPE_TWO:

            # the encoding of the outputs in synapse space: 1 --> 1, 0 --> -1
            synapse_shift = [2 * output - 1]

            # the direction of the shift is the output masked by the hidden firing pattern, which is the outer product
            # this rule is discussed in the appendix
            target_weights = numpy.outer(hiddens, synapse_shift)
            delta = target_weights * schedule.get_magnitude(_constants.NET_TYPE_TWO)

            # for net type two, reinforcement shifts all weights toward the output, so long as the hidden neuron has fired
            self.synapses += delta

        else:
            self.assertFalse()

        if apply_mutation:
            self.apply_mutation(hyperparams)

    def apply_mutation(self, hyperparams):

        if self.net_type == _constants.NET_TYPE_ONE:

            # mutation in net one means randomly flipping some weights 1 --> -1 or -1 --> 1
            target_weights = self.synapses * -1
            rands = numpy.random.uniform(size = target_weights.shape)
            self.synapses = numpy.where(rands < hyperparams.get_net_one_mutation_prob(), target_weights, self.synapses)

        elif self.net_type == _constants.NET_TYPE_TWO:

            # mutation in net two means contracting the synapse matrix toward zero
            self.synapses = self.synapses * hyperparams.get_net_two_mutation_strength()

        else:
            self.assertFalse()


if __name__ == '__main__':
    hp = Hyperparams()
    net = Net(_constants.NET_TYPE_TWO, hp)
    start = timer()
    for _ in range(20000):
        net.generate_output(hp)
        net.apply_reinforcer()
        net.apply_mutation()
    end = timer()
    print(end - start)
