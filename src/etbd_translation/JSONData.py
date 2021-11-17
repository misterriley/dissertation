'''
Created on May 24, 2021

@author: bleem
'''
import json

import easygui

from etbd_translation import Constants


class JSONData(object):
	'''
	classdocs
	'''

	_EXPERIMENTS = "experiments"
	_STAR_JSON = "*.json"
	_SD = "SD"
	_SCHED_TYPE_1 = "schedule_1_type"
	_SCHED_TYPE_2 = "schedule_2_type"
	_MAG_1 = "FDF_1"
	_MAG_2 = "FDF_2"
	_T_1_LO = "target_class_1_min"
	_T_1_HI = "target_class_1_max"
	_T_2_LO = "target_class_2_min"
	_T_2_HI = "target_class_2_max"
	_PUNISH_RI_IS_ENABLED = "punish_ri_is_enabled"
	_EQUAL_PUNISHMENT_RI = "equal_punishment_ri"
	_MUT_FUNC_PARAM = "mut_func_param"
	_PROP_PUNISH_IS_ENABLED = "prop_punish_is_enabled"
	_PROPORTION_PUNISHMENT = "proportion_punishment"
	_PUNISH_1_RI_IS_ENABLED = "punish_1_ri_is_enabled"
	_SINGLE_PUNISHMENT_RI = "single_punishment_ri"
	_SCHED_VALUE_1 = "schedule_1_scale"
	_SCHED_VALUE_2 = "schedule_2_scale"
	_OUTPUT_PATH = "output_path"
	_FILE_STUB = "file_stub"
	_GENERATIONS = "run_duration"
	_REPETITIONS = "repetitions"
	_CHECK_IS_PUNISHMENT_OK = "check_is_punishment_ok"
	_USE_GRAY_CODES = "use_gray_codes"
	_DECAY_OF_TRANSFER = "decay_of_transfer"
	_FOMO_A = "fomo_a"
	_ADD_VISCOSITY = "add_viscosity"
	_VISCOSITY_TICKS = "viscosity_ticks"
	_VISCOSITY_SELECTED_INDEX = "viscosity_selected_index"
	_NUM_BEHAVIORS = "num_behaviors"
	_LOW_PHENOTYPE = "low_phenotype"
	_HIGH_PHENOTYPE = "high_phenotype"
	_PERCENT_TO_REPLACE = "percent_to_replace"
	_PERCENT_TO_REPLACE_2 = "percent_to_replace_2"
	_FITNESS_METHOD = "fitness_method"
	_FITNESS_LANDSCAPE = "fitness_landscape"
	_PUNISHMENT_METHOD = "punishment_method"
	_ALPHA = "alpha"
	_BETA_0 = "beta_0"
	_BETA_1 = "beta_1"
	_SELECTION_METHOD = "selection_method"
	_CONTINUOUS_FUNCTION_FORM = "continuous_function_form"
	_MATCHMAKING_METHOD = "matchmaking_method"
	_RECOMBINATION_METHOD = "recombination_method"
	_MUTATION_METHOD = "mutation_method"
	_MUTATION_RATE = "mutation_rate"
	_SCHEDULES = "schedules"

	_DEFAULT_MUTATION_RATE = 10
	_DEFAULT_MUTATION_METHOD = "BITFLIP BY INDIVIDUAL"
	_DEFAULT_RECOMBINATION_METHOD = "BITWISE"
	_DEFAULT_MATCHMAKING_METHOD = "SEARCH"
	_DEFAULT_CONTINUOUS_FUNCTION_FORM = "LINEAR"
	_DEFAULT_SELECTION_METHOD = "CONTINUOUS"
	_DEFAULT_BETA_1 = 1
	_DEFAULT_BETA_0 = 1
	_DEFAULT_ALPHA = 1
	_DEFAULT_PUNISHMENT_METHOD = "FORCED MUTATION"
	_DEFAULT_FITNESS_LANDSCAPE = "CIRCULAR"
	_DEFAULT_FITNESS_METHOD = "INDIVIDUAL"
	_DEFAULT_PERCENT_TO_REPLACE_2 = 100
	_DEFAULT_PERCENT_TO_REPLACE = 100
	_DEFAULT_HIGH_PHENOTYPE = 1023
	_DEFAULT_LOW_PHENOTYPE = 0
	_DEFAULT_NUM_BEHAVIORS = 100
	_DEFAULT_SD = Constants.SD_COLOR_RED
	_DEFAULT_SCHED_TYPE = "VI"
	_DEFAULT_MAG = 40
	_DEFAULT_T_1_LO = 471
	_DEFAULT_T_1_HI = 511
	_DEFAULT_T_2_LO = 512
	_DEFAULT_T_2_HI = 552
	_DEFAULT_PUNISH_RI_IS_ENABLED = False
	_DEFAULT_EQUAL_PUNISHMENT_RI = 0
	_DEFAULT_MUT_FUNC_PARAM = None
	_DEFAULT_PROP_PUNISH_IS_ENABLED = False
	_DEFAULT_PROPORTION_PUNISHMENT = 0
	_DEFAULT_PUNISH_1_RI_IS_ENABLED = False
	_DEFAULT_SINGLE_PUNISHMENT_RI = 0
	_DEFAULT_SCHED_VALUE = None
	_DEFAULT_OUTPUT_PATH = "."
	_DEFAULT_FILE_STUB = "experiment"
	_DEFAULT_GENERATIONS = 20500
	_DEFAULT_REPETITIONS = 1
	_DEFAULT_CHECK_IS_PUNISHMENT_OK = False
	_DEFAULT_USE_GRAY_CODES = False
	_DEFAULT_DECAY_OF_TRANSFER = 0
	_DEFAULT_FOMO_A = 1
	_DEFAULT_ADD_VISCOSITY = False
	_DEFAULT_VISCOSITY_TICKS = 0
	_DEFAULT_VISCOSITY_SELECTED_INDEX = 0

	def __init__(self, data_dict):
		self.data_dict = data_dict

	def get_num_experiments(self):
		return len(self.data_dict[JSONData._EXPERIMENTS])

	def get_sd(self, experiment_index = -1):
		return self.get_from_experiment(JSONData._SD, experiment_index, JSONData._DEFAULT_SD)

	def get_from_experiment(self, key, experiment_index, default = None):
		default = self.get(key, default)
		experiment = self.get_experiment(experiment_index)
		if experiment is None:
			return default
		return experiment.get(key, default)

	def get_num_schedules(self, experiment_index):
		experiment = self.get_experiment(experiment_index)
		if experiment is None:
			return 0
		schedules = experiment["schedules"]
		if schedules is None:
			return 0
		return len(schedules)

	def get_from_schedule(self, key, experiment_index, schedule_index, default = None):
		default = self.get(key, default)
		experiment = self.get_experiment(experiment_index)
		if experiment is None:
			return default
		default = self.get_from_experiment(key, experiment_index, default)
		schedules = experiment["schedules"]
		if schedules is None or schedule_index >= len(schedules) or schedule_index < 0:
			return default
		schedule = schedules[schedule_index]
		if schedule is None:
			return default
		return schedule.get(key, default)

	def get_schedule(self, schedule_index):
		raise NotImplementedError

	def get(self, key, default = None):
		return self.data_dict.get(key, default)

	def get_experiment(self, experiment_index):
		experiments = self.data_dict[JSONData._EXPERIMENTS]
		if experiments is None or experiment_index < 0 or experiment_index >= len(experiments):
			return None
		return experiments[experiment_index]

	def get_sched_type_1(self, experiment_index, schedule_index = -1):
		ret = self.get_from_schedule(JSONData._SCHED_TYPE_1, experiment_index, schedule_index, JSONData._DEFAULT_SCHED_TYPE)
		return self.convert_to_sched_type(ret)

	def get_sched_type_2(self, experiment_index, schedule_index = -1):
		ret = self.get_from_schedule(JSONData._SCHED_TYPE_2, experiment_index, schedule_index, JSONData._DEFAULT_SCHED_TYPE)
		return self.convert_to_sched_type(ret)

	def get_mag_1(self, experiment_index, schedule_index):
		return self.get_from_schedule(JSONData._MAG_1, experiment_index, schedule_index, JSONData._DEFAULT_MAG)

	def get_mag_2(self, experiment_index, schedule_index):
		return self.get_from_schedule(JSONData._MAG_2, experiment_index, schedule_index, JSONData._DEFAULT_MAG)

	def get_t_1_lo(self, experiment_index):
		return self.get_from_experiment(JSONData._T_1_LO, experiment_index, JSONData._DEFAULT_T_1_LO)

	def get_t_1_hi(self, experiment_index):
		return self.get_from_experiment(JSONData._T_1_HI, experiment_index, JSONData._DEFAULT_T_1_HI)

	def get_t_2_lo(self, experiment_index):
		return self.get_from_experiment(JSONData._T_2_LO, experiment_index, JSONData._DEFAULT_T_2_LO)

	def get_t_2_hi(self, experiment_index):
		return self.get_from_experiment(JSONData._T_2_HI, experiment_index, JSONData._DEFAULT_T_2_HI)

	def punish_RI_is_enabled(self):
		return self.get_from_experiment(JSONData._PUNISH_RI_IS_ENABLED, JSONData._DEFAULT_PUNISH_RI_IS_ENABLED)

	def get_equal_punishment_ri(self, experiment_index):
		return self.get_from_experiment(JSONData._EQUAL_PUNISHMENT_RI, experiment_index, JSONData._DEFAULT_EQUAL_PUNISHMENT_RI)

	def get_mut_func_param(self, experiment_index):
		return self.get_from_experiment(JSONData._MUT_FUNC_PARAM, experiment_index, JSONData._DEFAULT_MUT_FUNC_PARAM)

	def prop_punish_is_enabled(self, experiment_index):
		return self.get_from_experiment(JSONData._PROP_PUNISH_IS_ENABLED, experiment_index, JSONData._DEFAULT_PROP_PUNISH_IS_ENABLED)

	def get_proportion_punishment(self, experiment_index, schedule_index):
		return self.get_from_schedule(JSONData._PROPORTION_PUNISHMENT, experiment_index, schedule_index, JSONData._DEFAULT_PROPORTION_PUNISHMENT)

	def punish_1_RI_is_enabled(self, experiment_index):
		return self.get_from_experiment(JSONData._PUNISH_1_RI_IS_ENABLED, experiment_index, JSONData._DEFAULT_PUNISH_1_RI_IS_ENABLED)

	def get_equal_punishment_RI(self, experiment_index, schedule_index = -1):
		return self.get_from_schedule(JSONData._EQUAL_PUNISHMENT_RI, experiment_index, schedule_index, JSONData._DEFAULT_EQUAL_PUNISHMENT_RI)

	def get_single_punishment_RI(self, experiment_index, schedule_index = -1):
		return self.get_from_schedule(JSONData._SINGLE_PUNISHMENT_RI, experiment_index, schedule_index, JSONData._DEFAULT_SINGLE_PUNISHMENT_RI)

	def get_sched_value_1(self, experiment_index, schedule_index):
		return self.get_from_schedule(JSONData._SCHED_VALUE_1, experiment_index, schedule_index, JSONData._DEFAULT_SCHED_VALUE)

	def get_sched_value_2(self, experiment_index, schedule_index):
		return self.get_from_schedule(JSONData._SCHED_VALUE_2, experiment_index, schedule_index, JSONData._DEFAULT_SCHED_VALUE)

	def get_output_path(self, experiment_index):
		return self.get_from_experiment(JSONData._OUTPUT_PATH, experiment_index, JSONData._DEFAULT_OUTPUT_PATH)

	def get_file_stub(self, experiment_index):
		return self.get_from_experiment(JSONData._FILE_STUB, experiment_index, JSONData._DEFAULT_FILE_STUB)

	def get_generations(self, experiment_index):
		return self.get_from_experiment(JSONData._GENERATIONS, experiment_index, JSONData._DEFAULT_GENERATIONS)

	def get_repetitions(self, experiment_index):
		return self.get_from_experiment(JSONData._REPETITIONS, experiment_index, JSONData._DEFAULT_REPETITIONS)

	def check_is_punishment_ok(self):
		return self.get(JSONData._CHECK_IS_PUNISHMENT_OK, JSONData._DEFAULT_CHECK_IS_PUNISHMENT_OK)

	def use_gray_codes(self):
		return self.get(JSONData._USE_GRAY_CODES, JSONData._DEFAULT_USE_GRAY_CODES)

	def get_decay_of_transfer(self):
		return self.get(JSONData._DECAY_OF_TRANSFER, JSONData._DEFAULT_DECAY_OF_TRANSFER)

	def get_fomo_a(self):
		return self.get(JSONData._FOMO_A, JSONData._DEFAULT_FOMO_A)

	def add_viscosity(self):
		return self.get(JSONData._ADD_VISCOSITY, JSONData._DEFAULT_ADD_VISCOSITY)

	def get_viscosity_ticks(self, experiment_index):
		return self.get_from_experiment(JSONData._VISCOSITY_TICKS, experiment_index, JSONData._DEFAULT_VISCOSITY_TICKS)

	def get_viscosity_selected_index(self, experiment_index):
		return self.get_from_experiment(JSONData._VISCOSITY_SELECTED_INDEX, experiment_index, JSONData._DEFAULT_VISCOSITY_SELECTED_INDEX)

	def get_num_behaviors(self):
		return self.get(JSONData._NUM_BEHAVIORS, JSONData._DEFAULT_NUM_BEHAVIORS)

	def get_low_phenotype(self):
		return self.get(JSONData._LOW_PHENOTYPE, JSONData._DEFAULT_LOW_PHENOTYPE)

	def get_high_phenotype(self):
		return self.get(JSONData._HIGH_PHENOTYPE, JSONData._DEFAULT_HIGH_PHENOTYPE)

	def get_percent_to_replace(self):
		return self.get(JSONData._PERCENT_TO_REPLACE, JSONData._DEFAULT_PERCENT_TO_REPLACE)

	def get_percent_to_replace_2(self):
		return self.get(JSONData._PERCENT_TO_REPLACE_2, JSONData._DEFAULT_PERCENT_TO_REPLACE_2)

	def get_fitness_method(self):
		ret = self.get(JSONData._FITNESS_METHOD, JSONData._DEFAULT_FITNESS_METHOD)
		return self.convert_to_fitness_method(ret)

	def get_fitness_landscape(self):
		ret = self.get(JSONData._FITNESS_LANDSCAPE, JSONData._DEFAULT_FITNESS_LANDSCAPE)
		return self.convert_to_fitness_landscape(ret)

	def get_punishment_method(self):
		ret = self.get(JSONData._PUNISHMENT_METHOD, JSONData._DEFAULT_PUNISHMENT_METHOD)
		return self.convert_to_punishment_method(ret)

	def get_alpha(self):
		return self.get(JSONData._ALPHA, JSONData._DEFAULT_ALPHA)

	def get_beta_0(self):
		return self.get(JSONData._BETA_0, JSONData._DEFAULT_BETA_0)

	def get_beta_1(self):
		return self.get(JSONData._BETA_1, JSONData._DEFAULT_BETA_1)

	def get_selection_method(self):
		ret = self.get(JSONData._SELECTION_METHOD, JSONData._DEFAULT_SELECTION_METHOD)
		return self.convert_to_selection_method(ret)

	def get_continuous_function_form(self):
		ret = self.get(JSONData._CONTINUOUS_FUNCTION_FORM, JSONData._DEFAULT_CONTINUOUS_FUNCTION_FORM)
		return self.convert_to_continuous_function_form(ret)

	def get_matchmaking_method(self):
		ret = self.get(JSONData._MATCHMAKING_METHOD, JSONData._DEFAULT_MATCHMAKING_METHOD)
		return self.convert_to_matchmaking_method(ret)

	def get_crossover_points(self, experiment_index):
		return self.get_from_experiment(JSONData._CROSSOVER_POINTS, experiment_index, JSONData._DEFAULT_CROSSOVER_POINTS)

	def get_recombination_method(self):
		ret = self.get(JSONData._RECOMBINATION_METHOD, JSONData._DEFAULT_RECOMBINATION_METHOD)
		return self.convert_to_recombination_method(ret)

	def get_mutation_method(self):
		ret = self.get(JSONData._MUTATION_METHOD, JSONData._DEFAULT_MUTATION_METHOD)
		return self.convert_to_mutation_method(ret)

	def get_gaussian_mutation_sd(self, experiment_index):
		return self.get_from_experiment(JSONData._GAUSSIAN_MUTATION_SD, experiment_index, JSONData._DEFAULT_GAUSSIAN_MUTATION_SD)

	def get_mutation_boundary(self, experiment_index):
		return self.get_from_experiment(JSONData._MUTATION_BOUNDARY, experiment_index, JSONData._DEFAULT_MUTATION_BOUNDARY)

	def get_mutation_rate(self):
		return self.get(JSONData._MUTATION_RATE, JSONData._DEFAULT_MUTATION_RATE)

	def convert_to_mutation_method(self, value):
		if value == "BITFLIP BY INDIVIDUAL":
			return Constants.MUTATION_METHOD_BIT_FLIP_BY_INDIVIDUAL
		elif value == "BITFLIP BY BIT":
			return Constants.MUTATION_METHOD_BIT_FLIP_BY_BIT
		elif value == "GAUSSIAN":
			return Constants.MUTATION_METHOD_GAUSSIAN
		elif value == "RANDOM INDIVIDUAL":
			return Constants.MUTATION_METHOD_RANDOM_INDIVIDUAL
		else:
			raise AssertionError()

	def convert_to_recombination_method(self, value):
		if value == "BITWISE":
			return Constants.RECOMBINATION_METHOD_BITWISE
		elif value == "CLONE":
			return Constants.RECOMBINATION_METHOD_CLONE
		elif value == "CROSSOVER":
			return Constants.RECOMBINATION_METHOD_CROSSOVER
		else:
			raise AssertionError()

	def convert_to_matchmaking_method(self, value):
		if value == "MATING POOL":
			return Constants.MATCHMAKING_METHOD_MATING_POOL
		elif value == "SEARCH":
			return Constants.MATCHMAKING_METHOD_SEARCH
		else:
			raise AssertionError()

	def convert_to_continuous_function_form(self, value):
		if value == "EXPONENTIAL":
			return Constants.CONTINUOUS_FUNCTION_FORM_EXPONENTIAL
		elif value == "LINEAR":
			return Constants.CONTINUOUS_FUNCTION_FORM_LINEAR
		elif value == "NA":
			return Constants.CONTINUOUS_FUNCTION_FORM_NOT_APPLICABLE
		elif value == "UNIFORM":
			return Constants.CONTINUOUS_FUNCTION_FORM_UNIFORM
		else:
			raise AssertionError()

	def convert_to_selection_method(self, value):
		if value == "CONTINUOUS":
			return Constants.SELECTION_METHOD_CONTINUOUS
		elif value == "TOURNAMENT":
			return Constants.SELECTION_METHOD_TOURNAMENT
		elif value == "TRUNCATION":
			return Constants.SELECTION_METHOD_TRUNCATION
		else:
			raise AssertionError()

	def convert_to_punishment_method(self, value):
		if value == "FORCED MUTATION":
			return Constants.PUNISHMENT_METHOD_FORCED_MUTATION
		elif value == "REPEL FOLD":
			return Constants.PUNISHMENT_METHOD_REPEL_FOLD
		elif value == "REPEL WRAP":
			return Constants.PUNISHMENT_METHOD_REPEL_WRAP
		else:
			raise AssertionError()

	def convert_to_fitness_method(self, value):
		if value == "MIDPOINT":
			return Constants.FITNESS_METHOD_MIDPOINT
		elif value == "INDIVIDUAL":
			return Constants.FITNESS_METHOD_INDIVIDUAL
		elif value == "ENTIRE_CLASS":
			return Constants.FITNESS_METHOD_ENTIRE_CLASS
		else:
			raise AssertionError()

	def convert_to_fitness_landscape(self, value):
		if value == "CIRCULAR":
			return Constants.FITNESS_LANDSCAPE_CIRCULAR
		elif value == "FLAT":
			return Constants.FITNESS_LANDSCAPE_FLAT
		else:
			raise AssertionError()

	def convert_to_sched_type(self, value):
		if value == "RI" or value == "VI":
			return Constants.SCHED_TYPE_RI
		elif value == "RR" or value == "VR":
			return Constants.SCHED_TYPE_RR
		elif value == "PROB":
			return Constants.SCHED_TYPE_PROB
		elif value == "EXT":
			return Constants.SCHED_TYPE_EXT
		else:
			raise AssertionError()

	@staticmethod
	def load_file(input_file = None, print_status = False):
		if input_file is None:
			input_file = easygui.fileopenbox(default = "../../exp_files/*.json")

		if input_file is None:
			return None

		with open(input_file,) as exp_file:
			if print_status:
				print("reading from " + input_file)
			data = json.load(exp_file)
			return JSONData(data)
