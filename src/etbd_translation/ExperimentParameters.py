'''
Created on May 25, 2021

@author: bleem
'''


class ExperimentParameters(object):
    '''
    classdocs
    '''

    def init(self):
        '''
        Constructor
        '''

        # This is for concurrent schedules
        self.m_SD = None
        self.m_SchedType1 = None
        self.m_SchedType2 = None
        self.m_Mag1 = None  # Note that only integer magnitudes are permitted for now.  The organism expects these as doubles!
        self.m_Mag2 = None
        self.m_T1Lo = None  # These are the lo and Hi phenotypes for the 2 target classes.
        self.m_T1Hi = None
        self.m_T2Lo = None
        self.m_T2Hi = None
        self.m_SchedValues1 = None  # Note that only integer schedule values are permitted for now.  The schedule objects expect these as doubles!
        self.m_SchedValues2 = None
        self.m_EqualPunishmentRI = None
        self.m_SinglePunishmentRI = None
        self.m_PunishmentMag = None  # 0 to 1
        self.m_MutFuncParam = None
        self.m_ProportionPunishment = None

    def get_sched_values_1(self):
        return self.m_SchedValues1

    def get_sched_values_2(self):
        return self.m_SchedValues2

    def set_sched_values_1(self, array_values):
        self.m_SchedValues1 = array_values

    def set_sched_values_2(self, array_values):
        self.m_SchedValues2 = array_values

    def get_sd(self):
        return self.m_SD

    def get_sched_type_1(self):
        return self.m_SchedType1

    def get_sched_type_2(self):
        return self.m_SchedType2

    def get_mag_1(self):
        return self.m_Mag1

    def get_mag_2(self):
        return self.m_Mag2

    def get_t_1_lo(self):
        return self.m_T1Lo

    def get_t_1_hi(self):
        return self.m_T1Hi

    def get_t_2_lo(self):
        return self.m_T2Lo

    def get_t_2_hi(self):
        return self.m_T2Hi

    def get_equal_punishment_ri(self):
        return self.m_EqualPunishmentRI

    def get_single_punishment_ri(self):
        return self.m_SinglePunishmentRI

    def get_punishment_mag(self):
        return self.m_PunishmentMag

    def get_mut_func_param(self):
        return self.m_MutFuncParam

    def get_proportion_punishment(self):
        return self.m_ProportionPunishment

    def set_sd(self, value):
        self.m_SD = value

    def set_sched_type_1(self, value):
        self.m_SchedType1 = value

    def set_sched_type_2(self, value):
        self.m_SchedType2 = value

    def set_mag_1(self, value):
        self.m_Mag1 = value

    def set_mag_2(self, value):
        self.m_Mag2 = value

    def set_t_1_lo(self, value):
        self.m_T1Lo = value

    def set_t_1_hi(self, value):
        self.m_T1Hi = value

    def set_t_2_lo(self, value):
        self.m_T2Lo = value

    def set_t_2_hi(self, value):
        self.m_T2Hi = value

    def set_equal_punishment_ri(self, value):
        self.m_EqualPunishmentRI = value

    def set_single_punishment_ri(self, value):
        self.m_SinglePunishmentRI = value

    def set_punishment_mag(self, value):
        self.m_PunishmentMag = value

    def set_mut_func_param(self, value):
        self.m_MutFuncParam = value

    def set_proportion_punishment(self, value):
        self.m_ProportionPunishment = value

