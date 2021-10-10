'''
Created on May 24, 2021

@author: bleem
'''

from etbd_translation.CRunConcurrent import CRunConcurrent
from etbd_translation.ExperimentParameters import ExperimentParameters


class frmExperiment(object):
    '''
    classdocs 
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.m_intExpNum = 0
        self.m_structExpInfo = [None]
        self.m_intGenerations = [None]
        self.m_intRepetitions = [None]
        self.m_strOutputPath = [None]
        self.m_strFileStub = [None]

    def add_experiments(self, json_data):

        # Should probably do this load here

        # Dim test As Integer
        # test = frmConcSchedules.txtPheno1Hi.Text

        self.m_intExpNum = json_data.get_num_experiments()
        for i in range(1, self.m_intExpNum + 1):
            self.m_structExpInfo.append(ExperimentParameters())
            self.m_strOutputPath.append(json_data.get_output_path(i))
            self.m_strFileStub.append(json_data.get_file_stub(i))
            self.m_intGenerations.append(json_data.get_generations(i))
            self.m_intRepetitions.append(json_data.get_repetitions(i))

            # Reads experimental info from the form and loads it into a data structure.  Note that only one SD is allowed for now.
            # Note that the PunishmentMag is not checked to ensure that it is in the range, 0 to 1.

            # Dim structExperimentInfo As ExperimentParameters <--This is now declared as a Public structure.  ExperimentParameters is declared in CRunParameters

            # Dim intN As Integer #Number of rows (conditions) in the dataviewgrid
            # Dim dblSchedValues1(), dblSchedValues2() As Double
            # Dim i As Integer
            # Dim strSchedValues1 As String = "" #For reading from structExperimentInfo
            # Dim strSchedValues2 As String = "" #For reading from structExperimentInfo

            self.m_structExpInfo[i].set_sd(json_data.get_sd(i))
            self.m_structExpInfo[i].set_sched_type_1(json_data.get_sched_type_1(i))
            self.m_structExpInfo[i].set_sched_type_2(json_data.get_sched_type_2(i))
            self.m_structExpInfo[i].set_mag_1(json_data.get_mag_1(i))
            self.m_structExpInfo[i].set_mag_2(json_data.get_mag_2(i))
            self.m_structExpInfo[i].set_t_1_lo(json_data.get_t_1_lo(i))
            self.m_structExpInfo[i].set_t_1_hi(json_data.get_t_1_hi(i))
            self.m_structExpInfo[i].set_t_2_lo(json_data.get_t_2_lo(i))
            self.m_structExpInfo[i].set_t_2_hi(json_data.get_t_2_hi(i))

            # These If...Then blocks are for punishment
            if json_data.punish_RI_is_enabled():
                self.m_structExpInfo[i].set_equal_punishment_ri(json_data.get_equal_punishment_ri(i))
                self.m_structExpInfo[i].set_mut_func_param(json_data.get_mut_func_param(i))

            else:
                # This ensures that there will be no lingering punishment info after a "Clear" operation
                self.m_structExpInfo[i].set_equal_punishment_ri(0)

            if json_data.prop_punish_is_enabled():
                self.m_structExpInfo[i].set_proportion_punishment(json_data.get_proportion_punishment(i))  # The reciprocal of this value (0 to 1) times the reinforcement RI value
                #                                                                                              gives the punishment RI value.  Not any more (7/2018).
                #                                                                                              Now it is the factor that when multiplied by the RI
                #                                                                                              reinforcement value gives the RI punishment value.
                self.m_structExpInfo[i].set_mut_func_param(json_data.get_mut_func_param(i))
            else:
                # I guess this ensures the same as in the previous If...Then block
                self.m_structExpInfo[i].set_proportion_punishment(0)

            if json_data.punish_1_RI_is_enabled():
                self.m_structExpInfo[i].set_single_punishment_ri(json_data.get_single_punishment_ri(i))
                self.m_structExpInfo[i].set_mut_func_param(json_data.get_mut_func_param(i))
            else:
                # I guess this ensures the same as in the previous If...Then blocks
                self.m_structExpInfo[i].set_single_punishment_ri(0)

            # i now equals intN
            # raise AssertionError(CStr(i))

            # Load the arrays into the data structure.
            self.m_structExpInfo[i].set_sched_values_1(json_data.get_dbl_sched_values_1())
            self.m_structExpInfo[i].set_sched_values_2(json_data.get_dbl_sched_values_2())

    def clear(self):

        self.m_frmOrganism.clear_organism()
        self.m_frmOrganism.set_exists(False)

    def run(self, an_organism, json_data):

        self.add_experiments(json_data)
        self.load_organism(json_data)

        for i in range(1, self.m_intExpNum + 1):
            # Run the experiment and write the data.
            objRunExperiment = CRunConcurrent(an_organism, self.m_structExpInfo[i], self.m_intRepetitions[i], self.m_intGenerations[i], self.m_strOutputPath[i], self.m_strFileStub[i])
            objRunExperiment.giddyup()

        print("Done giddyuped!")

