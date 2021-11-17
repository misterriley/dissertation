

'''
Created on Mar 22, 2021

@author: bleem
'''

from timeit import default_timer as timer
import winsound

from sklearn.linear_model import LinearRegression
import numpy

from nets import _constants
from nets._environment import Environment
from nets._etbd import ETBD
from nets._hyperparams import Hyperparams
from nets._io import IO
from nets._net import Net
from nets._null_environment import NullEnvironment
from nets._null_model import NullModelMarkov, NullModelQ
from nets._schedule import Schedule
import multiprocessing as mp


def run_sensitivity_analysis(hyperparams):

    experiment_data = IO.read_experiment_file(hyperparams)
    fieldnames = ["MUTATION RATE (NET TYPE 1)", "a"]
    sens_dict_list = []
    for x in [x / 2000 for x in range(1, 101)]:

        hyperparams.set_net_two_hidden_node_firing_prob(x)
        hyperparams.renorm_net_two_reinforcement_strength()

        return_dict = run_experiment(experiment_data, hyperparams)
        sensitivity = calculate_sensitivity(return_dict)
        sens_dict_list.append({fieldnames[0]:x, fieldnames[1]:sensitivity})
        # print(str(x) + " " + str(sensitivity))

    IO.write_sensitivity_analysis(sens_dict_list, fieldnames)


def run_experiment(experiment_data, hyperparams, print_status, pool):

    manager = mp.Manager()
    return_dict = manager.dict()
    args_list = []

    if experiment_data.is_sequential():
        for repetition_index in range(experiment_data.get_run_repititions()):

            if experiment_data.get_net_type() == _constants.NET_TYPE_NULL_Q:
                environment = build_environment(experiment_data, repetition_index, True)
                net = NullModelQ(hyperparams, environment, experiment_data)
            elif experiment_data.get_net_type() == _constants.NET_TYPE_NULL_MARKOV:
                environment = build_environment(experiment_data, repetition_index, True)
                net = NullModelMarkov(hyperparams, environment, experiment_data)
            elif experiment_data.get_net_type() == _constants.NET_TYPE_ETBD:
                environment = build_environment(experiment_data, repetition_index)
                net = ETBD(hyperparams)
            else:
                environment = build_environment(experiment_data, repetition_index)
                net = Net(experiment_data.get_net_type(), hyperparams)

            for run_data in experiment_data.get_runs():
                environment.add_run(run_data)

            args_list.append((environment, net, experiment_data, return_dict, hyperparams, print_status))

    else:
        for run_data in experiment_data.get_runs():
            for repetition_index in range(experiment_data.get_run_repititions()):
                if experiment_data.get_net_type() == _constants.NET_TYPE_NULL_Q:
                    environment = build_environment(experiment_data, repetition_index, True)
                    net = NullModelQ(hyperparams, environment, experiment_data)
                elif experiment_data.get_net_type() == _constants.NET_TYPE_NULL_MARKOV:
                    environment = build_environment(experiment_data, repetition_index, True)
                    net = NullModelMarkov(hyperparams, environment, experiment_data)
                elif experiment_data.get_net_type() == _constants.NET_TYPE_ETBD:
                    environment = build_environment(experiment_data, repetition_index)
                    net = ETBD(hyperparams)
                else:
                    environment = build_environment(experiment_data, repetition_index)
                    net = Net(experiment_data.get_net_type(), hyperparams)

                environment.add_run(run_data)
                args_list.append((environment, net, experiment_data, return_dict, hyperparams, print_status))

    if print_status:
        print(str(len(args_list)) + " task(s) assigned")

    if(hyperparams.run_multithreaded()):
        pool.starmap(do_one_repetition, args_list)
    else:
        pool.starmap_async(do_one_repetition, args_list)

    return return_dict


def build_environment(experiment_data, repetition_index, is_null_model = False):

    if is_null_model:
        environment = NullEnvironment(repetition_index)
    else:
        environment = Environment(repetition_index)
    environment.set_net_type(experiment_data.get_net_type())
    environment.set_mutation_rate(experiment_data.get_mutation_rate())

    return environment


def reset_environment_schedule(environment, experiment_data, run_data, return_dict, hyperparams, print_status):
    if run_data is not None:
        schedule_data_1 = run_data.get_schedule(1)
        schedule_data_2 = run_data.get_schedule(2)

        target_class_1 = experiment_data.get_target_classes()[1]
        target_class_2 = experiment_data.get_target_classes()[2]

        schedule_1 = Schedule(target_class_1.get_schedule_type(), schedule_data_1.get_scale(), 1, target_class_1.get_min(), target_class_1.get_max(), schedule_data_1.get_FDF(), hyperparams)
        schedule_2 = Schedule(target_class_2.get_schedule_type(), schedule_data_2.get_scale(), 2, target_class_2.get_min(), target_class_2.get_max(), schedule_data_2.get_FDF(), hyperparams)

        environment.set_schedule(1, schedule_1)
        environment.set_schedule(2, schedule_2)
    behavior_record = environment.get_behavior_record()
    if behavior_record is not None:
        k = str(behavior_record.get_run_data().get_run_index()) + " " + str(environment.get_repetition_index())
        return_dict[k] = behavior_record
        if len(return_dict) % 10 == 0 and print_status:
            print(f"completed schedule {len(return_dict)}")

    if run_data is not None:
        environment.put_new_behavior_record(run_data)


def do_one_repetition(environment, net, experiment_data, return_dict, hyperparams, print_status):

    last_schedule = None

    sequence_length = len(experiment_data.get_runs()) if experiment_data.is_sequential() else 1
    num_ticks = sequence_length * experiment_data.get_run_duration()

    initial_run = environment.get_runs()[0]
    reset_environment_schedule(environment, experiment_data, initial_run, return_dict, hyperparams, print_status)

    schedule_start = -1 * experiment_data.get_burn_in()
    for time_index in range(schedule_start, num_ticks):

        register_data = time_index >= 0

        if time_index > 0 and time_index % experiment_data.get_run_duration() == 0:
            run_index = int(time_index / experiment_data.get_run_duration())
            next_run = experiment_data.get_runs()[run_index]
            reset_environment_schedule(environment, experiment_data, next_run, return_dict, hyperparams, print_status)
            last_schedule = None
            schedule_start = time_index

        output = net.generate_output(hyperparams)
        tc_index = environment.get_tc_index_for_behavior(output, hyperparams)

        if tc_index is not None:

            schedule = environment.get_schedule_for_tc_index(tc_index)
            behavior_record = environment.get_behavior_record()
            if register_data:
                behavior_record.increment_behaviors(tc_index)

            if schedule.get_consequence(time_index - schedule_start):
                net.apply_reinforcer(hyperparams, schedule)
                if register_data:
                    behavior_record.increment_reinforcers(tc_index)

            if register_data and last_schedule != schedule:
                if last_schedule is not None:
                    behavior_record.increment_changeovers()
                last_schedule = schedule

        net.apply_mutation(hyperparams)

    reset_environment_schedule(environment, None, None, return_dict, hyperparams, print_status)


def run_exp_two_phase_two_one(hyperparams, print_status, pool):

    experiment_data = IO.read_experiment_file("experiment_2_2_1.json", print_status)
    if experiment_data is not None:
        hyperparams.set_mutation_rate(experiment_data.get_mutation_rate())
        return_dict = run_experiment(experiment_data, hyperparams, print_status, pool)
        IO.write_results_exp_2(return_dict)


def run_exp_two_phase_two_two(hyperparams, print_status, pool):
    experiment_data = IO.read_experiment_file("experiment_2_2_2.json", print_status)
    if experiment_data is not None:
        hyperparams.set_mutation_rate(experiment_data.get_mutation_rate())
        return_dict = run_experiment(experiment_data, hyperparams, print_status, pool)
        IO.write_results_exp_2(return_dict)


def run_exp_two_phase_one(hyperparams, print_status, pool):

    experiment_data = IO.read_experiment_file("experiment_2_1.json", print_status)
    if experiment_data is not None:
        hyperparams.set_mutation_rate(experiment_data.get_mutation_rate())
        return_dict = run_experiment(experiment_data, hyperparams, print_status, pool)
        IO.write_results_exp_2(return_dict)


def run_exp_one(hyperparams, print_status, pool):

    experiment_data = IO.read_experiment_file("reinforcement_only.json", print_status)
    if experiment_data is not None:
        hyperparams.set_mutation_rate(experiment_data.get_mutation_rate())
        return_dict = run_experiment(experiment_data, hyperparams, print_status, pool)
        IO.write_results_exp_1(return_dict)


def calculate_loss(hyperparams, reps, print_status, pool, file):
    experiment_data = IO.read_experiment_file(file, print_status)

    am_target = 0.68
    ar_target = 0.83

    # b_avg_target = 1030

    if experiment_data is not None:
        hyperparams.set_mutation_rate(experiment_data.get_mutation_rate())

        ret = numpy.zeros(4)

        for _ in range(reps):
            return_dict = run_experiment(experiment_data, hyperparams, print_status, pool)

            x = []
            y = []

            b_count = 0
            b_sum = 0

            for k in return_dict:
                br = return_dict[k]
                r = br.get_log_R1_over_R2()
                b = br.get_log_B1_over_B2()
                m = br.get_log_M1_over_M2()

                if r is not None and b is not None:
                    x.append([r, m])
                    y.append(b)

                b1 = br.get_behaviors(1)
                b2 = br.get_behaviors(2)

                if b1 is not None:
                    b_sum += b1
                    b_count += 1

                if b2 is not None:
                    b_sum += b2
                    b_count += 1

            try:
                if print_status:
                    print(f"{len(x)} points")
                linreg = LinearRegression().fit(x, y)

                ar = linreg.coef_[0]
                am = linreg.coef_[1]
                b_avg = b_sum / b_count
                loss = ((am - am_target) / .1) ** 2 + ((ar - ar_target) / .1) ** 2  # + ((b_avg - b_avg_target) / b_avg_target) ** 2
                exps = numpy.array([ar, am, b_avg, loss])

                ret += exps
            except ValueError:
                return None
        # if print_status:
            # print("loss avg = " + str(loss_sum / reps))

        # if reps > 1:

            # variance = (loss_sq_sum - (loss_sum ** 2) / reps) / (reps - 1)
            # SE = (variance / reps) ** .5
            # if print_status:
                # print("loss var = " + str(variance))
                # print("loss SE = " + str(SE))

    return ret / reps


def calculate_sensitivity(return_dict):

    x = []
    y = []

    for k in return_dict:
        environment = return_dict[k]
        r = environment.get_log_R1_over_R2()
        b = environment.get_log_B1_over_B2()

        if r is not None and b is not None:
            x.append([r])
            y.append(b)

    linreg = LinearRegression().fit(x, y)
    return linreg.coef_[0]


def parameter_sweep(hyperparams, pool):

    print("magn\tmut\tar\tam\tb_avg\tloss")

    min_loss = None

    for index in range(20):

        # h_const = 245
        # h_exp = .78
        # q_x = 0.8
        # q_y = 0.087

        # epsilon = 0.14
        # inverse_temp = 1.888  # / 50 * (2 * index + 41)  # 1.927
        # lr = 0.9

        magnitude_const = 11 + (index / 5)  # 2.0
        mutation_multiplier = 1  # .24

        # hyperparams.set_h_policy_constant(h_const)
        # hyperparams.set_h_policy_exponent(h_exp)
        # hyperparams.set_q_policy_min_point((q_x, q_y))

        # hyperparams.set_learning_rate(lr)
        # hyperparams.set_epsilon(epsilon)
        # hyperparams.set_inverse_temp(inverse_temp)

        hyperparams.set_net_one_magnitude_const(magnitude_const)
        hyperparams.set_net_one_mutation_multiplier(mutation_multiplier)

        exps = calculate_loss(hyperparams, 1, False, pool, "experiment_1.json")
        this_loss = exps[3]

        if min_loss == None:
            min_loss = this_loss
        else:
            min_loss = min(min_loss, this_loss)

        end_bit = "\t*" if this_loss == min_loss else ""
        if this_loss == min_loss:
            winsound.Beep(880, 200)

        print(f'{magnitude_const:.3f}\t{mutation_multiplier:.3f}\t{exps[0]:.3f}\t{exps[1]:.3f}\t{exps[2]:.1f}\t{exps[3]:.3f}\t' + end_bit)


def do_main_run(hyperparams, pool):
    run_exp_one(hyperparams, True, pool)
    run_exp_two_phase_one(hyperparams, True, pool)
    run_exp_two_phase_two_one(hyperparams, True, pool)
    run_exp_two_phase_two_two(hyperparams, True, pool)
    # parameter_sweep(hyperparams, pool)


if __name__ == '__main__':

    start = timer()
    hyperparams = Hyperparams()
    # hyperparams.set_run_multithreaded(False)

    with mp.Pool(processes = hyperparams.get_num_helper_threads()) as pool:
        do_main_run(hyperparams, pool)

    end = timer()
    print("finished with time " + str(end - start))
    winsound.Beep(440, 200)

