'''
Created on May 26, 2021

@author: bleem
'''

from etbd_translation.JSONData import JSONData
from etbd_translation.frmBuildOrganism import frmBuildOrganism
from etbd_translation.frmExperiment import frmExperiment

if __name__ == '__main__':

	data = JSONData.load_file("../../exp_files/experiment_1.json", print_status = True)
	for exp_index in range(data.get_num_experiments()):
		org_builder = frmBuildOrganism()
		org_builder.create_a_population(data)
		exp_runner = frmExperiment(org_builder)
		exp_runner.run(data)
