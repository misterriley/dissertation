'''
Created on May 24, 2021

@author: bleem
'''

from playsound import playsound

from etbd_translation.CRunConcurrent import CRunConcurrent
from etbd_translation.ExperimentParameters import ExperimentParameters


GREEN = "Green"


class frmExperiment(object):
	'''
	classdocs 
	'''

	def __init__(self, frmOrganism):
		'''
		Constructor
		'''
		self.m_intExpNum = 0
		self.m_structExpInfo = []
		self.m_intGenerations = []
		self.m_intRepetitions = []
		self.m_strOutputPath = []
		self.m_strFileStub = []
		self.m_frmOrganism = frmOrganism
		self.m_status = None

	def add_experiments(self, json_data):

		# Should probably do this load here

		# Dim test As Integer
		# test = frmConcSchedules.txtPheno1Hi.Text

		self.m_intExpNum = json_data.get_num_experiments()
		for exp_index in range(0, self.m_intExpNum):
			num_schedules = json_data.get_num_schedules(exp_index)
			self.m_structExpInfo.append(ExperimentParameters(num_schedules))
			self.m_strOutputPath.append(json_data.get_output_path(exp_index))
			self.m_strFileStub.append(json_data.get_file_stub(exp_index))
			self.m_intGenerations.append(json_data.get_generations(exp_index))
			self.m_intRepetitions.append(json_data.get_repetitions(exp_index))

			# Reads experimental info from the form and loads it into a data structure.  Note that only one SD is allowed for now.
			# Note that the PunishmentMag is not checked to ensure that it is in the range, 0 to 1.

			# Dim structExperimentInfo As ExperimentParameters <--This is now declared as a Public structure.  ExperimentParameters is declared in CRunParameters

			# Dim intN As Integer #Number of rows (conditions) in the dataviewgrid
			# Dim dblSchedValues1(), dblSchedValues2() As Double
			# Dim exp_index As Integer
			# Dim strSchedValues1 As String = "" #For reading from structExperimentInfo
			# Dim strSchedValues2 As String = "" #For reading from structExperimentInfo

			self.m_structExpInfo[exp_index].set_sd(json_data.get_sd(exp_index))
			self.m_structExpInfo[exp_index].set_sched_type_1(json_data.get_sched_type_1(exp_index))
			self.m_structExpInfo[exp_index].set_sched_type_2(json_data.get_sched_type_2(exp_index))
			self.m_structExpInfo[exp_index].set_t_1_lo(json_data.get_t_1_lo(exp_index))
			self.m_structExpInfo[exp_index].set_t_1_hi(json_data.get_t_1_hi(exp_index))
			self.m_structExpInfo[exp_index].set_t_2_lo(json_data.get_t_2_lo(exp_index))
			self.m_structExpInfo[exp_index].set_t_2_hi(json_data.get_t_2_hi(exp_index))

			# These If...Then blocks are for punishment
			if json_data.punish_RI_is_enabled():
				self.m_structExpInfo[exp_index].set_equal_punishment_ri(json_data.get_equal_punishment_ri(exp_index))
				self.m_structExpInfo[exp_index].set_mut_func_param(json_data.get_mut_func_param(exp_index))

			else:
				# This ensures that there will be no lingering punishment info after a "Clear" operation
				self.m_structExpInfo[exp_index].set_equal_punishment_ri(0)

			if json_data.prop_punish_is_enabled(exp_index):
				self.m_structExpInfo[exp_index].set_proportion_punishment(json_data.get_proportion_punishment(exp_index))  # The reciprocal of this value (0 to 1) times the reinforcement RI value
				# 																							  				gives the punishment RI value.  Not any more (7/2018).
				# 																							  				Now it is the factor that when multiplied by the RI
				# 																							  				reinforcement value gives the RI punishment value.
				self.m_structExpInfo[exp_index].set_mut_func_param(json_data.get_mut_func_param(exp_index))
			else:
				# I guess this ensures the same as in the previous If...Then block
				self.m_structExpInfo[exp_index].set_proportion_punishment(0)

			if json_data.punish_1_RI_is_enabled(exp_index):
				self.m_structExpInfo[exp_index].set_single_punishment_ri(json_data.get_single_punishment_ri(exp_index))
				self.m_structExpInfo[exp_index].set_mut_func_param(json_data.get_mut_func_param(exp_index))
			else:
				# I guess this ensures the same as in the previous If...Then blocks
				self.m_structExpInfo[exp_index].set_single_punishment_ri(0)

			# exp_index now equals intN
			# raise AssertionError(CStr(exp_index))

			# TODO - start here

			# Load the arrays into the data structure.
			for schedule_index in range(json_data.get_num_schedules(exp_index)):
				self.m_structExpInfo[exp_index].set_sched_mag_1(schedule_index, json_data.get_mag_1(exp_index, schedule_index))
				self.m_structExpInfo[exp_index].set_sched_mag_2(schedule_index, json_data.get_mag_2(exp_index, schedule_index))
				self.m_structExpInfo[exp_index].set_sched_value_1(schedule_index, json_data.get_sched_value_1(exp_index, schedule_index))
				self.m_structExpInfo[exp_index].set_sched_value_2(schedule_index, json_data.get_sched_value_2(exp_index, schedule_index))

	def clear(self):

		self.m_frmOrganism.clear_organism()
		self.m_frmOrganism.set_exists(False)

	def load_organism(self):

		if self.m_frmOrganism.exists():
			myOrganism = None
			myOrganism = self.m_frmOrganism.get_creature()  # '<--frmOrganism is now a Global variable (in Global declarations class)
		else:
			raise RuntimeError("You didn't build an organism!")

		# 'MsgBox(CStr(myOrganism.Item(0).BehaviorsInfo.MutationInfo.Rate))
		# 'Stop

		self.m_status = GREEN

		# 'Try
		# '	myOrganism = frmOrganism.Creature '<--frmOrganism is now a Global variable (in Global declarations class)
		# 'Catch ex As Exception ' The exception occurs in the organism code and does not pass through here.
		# '	MsgBox("Make sure you built an organism correctly")
		# 'End Try

		# 'myOrganism.SDColor = Organism.SDColor.Yellow 'Looks like this might be working after all!
		# 'Try writing some stuff out from myOrganism.  See how the info box is written on the frmOrganism form

		# 'Test read...The organism is ready to run.  Don't have to read this off until writing the data.  It all appears to be working well.
		# 'Dim stuLocalBehaviorsInfo As BehaviorsInfo <---Module level structure
		# 'For testing, otherwise don't need stuLocalBehaviorsInfo
		myOrganism.get_item(0).get_behaviors_info()

		#'MsgBox("Discriminative stimulus: " & stuLocalBehaviorsInfo.SDID.ToString) '  It's woikin'!!!
		#'MsgBox("Number of behavior in population: " & stuLocalBehaviorsInfo.NumBehaviors.ToString) '  It's woikin'!!!
		#'MsgBox("Low Phenotype = " & stuLocalBehaviorsInfo.LowPhenotype.ToString & "; High Phenotype = " & stuLocalBehaviorsInfo.HighPhenotype.ToString) '  It's woikin'!!!
		#'MsgBox("Fitness landscape: " & stuLocalBehaviorsInfo.SelectionInfo.FitnessLandscape.ToString) '  It's woikin'!!!
		#'----------------------------------------------------------------------------------------------------------------------

	def run(self, json_data):

		self.add_experiments(json_data)
		self.load_organism()

		for i in range(0, self.m_intExpNum):
			print("starting experiment " + str(i))
			# Run the experiment and write the data.
			objRunExperiment = CRunConcurrent(self.m_frmOrganism.get_creature(), json_data, i, self.m_structExpInfo[i])
			objRunExperiment.giddyup()
			print("finishing experiment " + str(i))

		playsound("./22Fillywhinnygrunt2000.wav")  # as Jack would have wanted
		print("Done giddyuped!")

