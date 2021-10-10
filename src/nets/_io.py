'''
Created on Apr 5, 2021

@author: bleem
'''

import csv
import json
import time

import easygui

from nets import _constants
from nets._experiment_data import ExperimentData
from nets._run_data import RunData
from nets._schedule_data import ScheduleData
from nets._target_class_data import TargetClassData


class IO(object):
    '''
    classdocs
    '''

    @staticmethod
    def write_sensitivity_analysis(sens_dict_list, fieldnames):
        outfile_name = "./outputs/sensitivity_" + str(IO.get_time_stamp()) + ".csv"

        with open(outfile_name, 'w', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()

            for sens_dict in sens_dict_list:
                writer.writerow(sens_dict)

    @staticmethod
    def get_time_stamp():
        return int(time.time()) % 1000000

    @staticmethod
    def write_results_exp_2(br_dict):
        first_br = br_dict[next(iter(br_dict))]

        timestamp = IO.get_time_stamp()
        outfile_name = f"./outputs/Experiment 2/EXP_2_NET_{first_br.get_environment().get_net_type()}_{timestamp}.csv"

        with open(outfile_name, 'w', newline = '') as f:
            print("writing results to " + outfile_name)
            fieldnames = ["net_type", "run_index", "repetition_index", "mutation_rate", "Sch 1", "R1", "B1",
                        "Sch 2", "R2", "B2", "Larger Ratio/Smaller Ratio", "Preference for Smaller Ratio", "Max Preference"]

            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()

            for k in br_dict:
                br = br_dict[k]
                env = br.get_environment()

                b1 = br.get_behaviors(1)
                b2 = br.get_behaviors(2)

                schedule1 = br.get_schedule(1)
                schedule2 = br.get_schedule(2)

                scale1 = schedule1.get_schedule_scale()
                scale2 = schedule2.get_schedule_scale()

                output_dict = {"net_type": env.get_net_type(), "run_index": br.get_run_data().get_run_index(), "repetition_index": env.get_repetition_index(), "mutation_rate":env.get_mutation_rate(),
                               "B1": b1, "R1": br.get_reinforcers(1),
                               "B2": b2, "R2": br.get_reinforcers(2)}

                output_dict["Sch 1"] = schedule1.get_schedule_type() + " " + str(scale1)
                output_dict["Sch 2"] = schedule2.get_schedule_type() + " " + str(scale2)
                output_dict["Larger Ratio/Smaller Ratio"] = scale2 / scale1
                output_dict["Preference for Smaller Ratio"] = b1 / (b1 + b2)
                output_dict["Max Preference"] = max(b1, b2) / (b1 + b2)

                writer.writerow(output_dict)

    @staticmethod
    def write_results_exp_1(br_dict):

        first_br = br_dict[next(iter(br_dict))]

        timestamp = IO.get_time_stamp()
        outfile_name = f"./outputs/Experiment 1/EXP_1_NET_{first_br.get_environment().get_net_type()}_MUT_{first_br.get_environment().get_mutation_rate()}_{timestamp}.csv"

        with open(outfile_name, 'w', newline = '') as f:
            print("writing results to " + outfile_name)
            fieldnames = ["net_type", "run_index", "repetition_index", "mutation_rate", "Sch 1", "R1", "M1", "B1",
                        "Sch 2", "R2", "M2", "B2", "interaction", "log(R1/R2)", "log(M1/M2)", "log(B1/B2)", "am", "ar", "ai", "log(b)",
                        "(log(M1/M2))^2", "(log(R1/R2)) * (log(M1/M2))", "(log(R1/R1))^2", "Changeovers",
                        "A", "B", "C", "G", "B^2 - 4AC"]
            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()
            regression_added = False

            for k in br_dict:
                br = br_dict[k]
                env = br.get_environment()
                sch1 = env.get_schedule_for_tc_index(1)
                sch2 = env.get_schedule_for_tc_index(2)

                output_dict = {"net_type": env.get_net_type(), "run_index": br.get_run_data().get_run_index(), "repetition_index": env.get_repetition_index(), "mutation_rate":env.get_mutation_rate(),
                               "B1": br.get_behaviors(1), "R1": br.get_reinforcers(1), "M1": _constants.DEFAULT_FDF / br.get_FDF(1),
                               "B2": br.get_behaviors(2), "R2": br.get_reinforcers(2), "M2": _constants.DEFAULT_FDF / br.get_FDF(2)}

                output_dict["Sch 1"] = sch1.get_schedule_type() + " " + str(sch1.get_schedule_scale())
                output_dict["Sch 2"] = sch2.get_schedule_type() + " " + str(sch2.get_schedule_scale())

                output_dict["log(B1/B2)"] = br.get_log_B1_over_B2()
                output_dict["log(R1/R2)"] = br.get_log_R1_over_R2()
                output_dict["interaction"] = br.get_log_R1_over_R2() * br.get_log_M1_over_M2()
                output_dict["log(M1/M2)"] = br.get_log_M1_over_M2()

                output_dict["(log(R1/R1))^2"] = br.get_log_R1_over_R2() ** 2
                output_dict["(log(M1/M2))^2"] = br.get_log_M1_over_M2() ** 2
                output_dict["(log(R1/R2)) * (log(M1/M2))"] = br.get_log_R1_over_R2() * br.get_log_M1_over_M2()

                output_dict["Changeovers"] = br.get_changeovers()

                if not regression_added:
                    num_rows = len(br_dict)
                    max_row = 1 + num_rows

                    output_dict["am"] = f'=LINEST(P2:P{max_row},M2:O{max_row},TRUE,TRUE)'
                    output_dict["A"] = f'=LINEST(X2:X{max_row},U2:W{max_row},TRUE,TRUE)'
                    output_dict["B^2 - 4AC"] = "=Z2^2 - 4 * Y2 * AA2"

                    regression_added = True

                writer.writerow(output_dict)

    @staticmethod
    def read_experiment_file(input_file = None, print_status = False):

        if input_file is None:
            input_file = easygui.fileopenbox(filetypes = ["*.json"])

        if input_file is None:
            return None

        with open(input_file,) as exp_file:
            if print_status:
                print("reading from " + input_file)
            data = json.load(exp_file)
            return IO.convert_to_experiment(data)

    @staticmethod
    def convert_to_experiment(data):

        target_class_1_min = data["target_class_1_min"]
        target_class_1_max = data["target_class_1_max"]

        target_class_2_min = data["target_class_2_min"]
        target_class_2_max = data["target_class_2_max"]

        schedule_1_type = data["schedule_1_type"]
        schedule_2_type = data["schedule_2_type"]

        run_duration = data["run_duration"]
        burn_in = data["burn_in"]
        run_repetitions = data["run_repetitions"]
        net_type = data["net_type"]
        mutation_rate = data["mutation_rate"]
        sequential = data["sequential"]

        experiments = data["experiments"]
        ret = ExperimentData(run_duration, burn_in, run_repetitions, net_type, mutation_rate, sequential)

        target_class_data_1 = TargetClassData(1, target_class_1_min, target_class_1_max, schedule_1_type)
        target_class_data_2 = TargetClassData(2, target_class_2_min, target_class_2_max, schedule_2_type)

        ret.set_target_class_data(1, target_class_data_1)
        ret.set_target_class_data(2, target_class_data_2)

        FDF = data.get("FDF", _constants.DEFAULT_FDF)

        for i in range(len(experiments)):
            experiment = experiments[i]

            schedule_1_scale = experiment["schedule_1_scale"]
            FDF_1 = experiment.get("FDF_1", FDF)

            schedule_1_data = ScheduleData(1, schedule_1_scale, FDF_1)

            schedule_2_scale = experiment["schedule_2_scale"]
            FDF_2 = experiment.get("FDF_2", FDF)

            schedule_2_data = ScheduleData(2, schedule_2_scale, FDF_2)

            run_data = RunData(i)
            run_data.set_schedule(1, schedule_1_data)
            run_data.set_schedule(2, schedule_2_data)

            ret.add_run(run_data)

        return ret


if __name__ == '__main__':
    IO.read_experiment_file()
