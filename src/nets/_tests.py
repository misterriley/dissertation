'''
Created on Apr 12, 2021

@author: bleem
'''

import numpy

from nets import _constants
from nets._environment import Environment
from nets._hyperparams import Hyperparams
from nets._io import IO
from nets._net import Net
from nets._operant import Operant
from nets._schedule import Schedule


def build_environment(experiment_data, run_data, repetition_index, hyperparams):

    environment = Environment(run_data.get_run_index(), repetition_index)
    for tc_index in experiment_data.get_target_classes():
        target_class = experiment_data.get_target_classes()[tc_index]
        schedule_data = run_data.get_schedule(tc_index)
        schedule = Schedule(target_class.get_schedule_type(), schedule_data.get_scale())
        operant = Operant(tc_index, schedule, target_class.get_min(), target_class.get_max(), schedule_data.get_magnitude(), hyperparams)
        environment.add_operant(operant)

    return environment


TEST_LEN = 100000


def p_to_logit(p):
    return numpy.log(p / (1 - p))


def test_proportions(net, environment, hyperparams, tag):

    count_0 = 0
    count_1 = 0
    count_2 = 0

    for _ in range(0, TEST_LEN):
        output = net.generate_output(hyperparams)
        if environment.get_operant_for_tc_index(1).get_target_class().contains_bitfield(output, hyperparams):
            count_1 += 1
        elif environment.get_operant_for_tc_index(2).get_target_class().contains_bitfield(output, hyperparams):
            count_2 += 1
        else:
            count_0 += 1

    proportion_0, proportion_1, proportion_2 = count_0 / TEST_LEN, count_1 / TEST_LEN, count_2 / TEST_LEN
    # log_odds_0 = p_to_logit(proportion_0)
    # log_odds_1 = p_to_logit(proportion_1)
    # log_odds_2 = p_to_logit(proportion_2)
    print (tag + "\t" + str(proportion_0) + "\t" + str(proportion_1) + "\t" + str(proportion_2))


if __name__ == '__main__':

    hyperparams = Hyperparams()
    experiment_data = IO.read_experiment_file(hyperparams)
    net = Net(_constants.NET_TYPE_ONE, hyperparams)
    environment = build_environment(experiment_data, experiment_data.get_runs()[0], 0, hyperparams)
    op_1 = environment.get_operant_for_tc_index(1)
    op_2 = environment.get_operant_for_tc_index(2)

    reinforcers_found = 0

    test_proportions(net, environment, hyperparams, str(reinforcers_found))

    op_to_find = op_1

    while reinforcers_found < 10:

        output = net.generate_output(hyperparams)
        operant = environment.get_operant_for_behavior(output, hyperparams)

        if operant is not None and op_to_find == operant:

            net.apply_reinforcer(hyperparams, magnitude = 1)
            reinforcers_found += 1

            test_proportions(net, environment, hyperparams, str(reinforcers_found))

            # op_to_find = op_1 if op_to_find == op_2 else op_2

    """op_to_find = op_2

    mutations = 0

    test_proportions(net, environment, hyperparams, str(mutations))

    while mutations < 500:

        net.apply_mutation(hyperparams)
        mutations += 1
        test_proportions(net, environment, hyperparams, str(mutations))

    for mutation_count in range(101):

        net.apply_mutation(hyperparams)
        test_proportions(net, environment, hyperparams, str(mutation_count))"""

