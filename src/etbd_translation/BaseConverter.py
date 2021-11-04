'''
Created on May 23, 2021
Translated May 23, 2021

@author: bleem
'''


class BaseConverter(object):
	'''
	classdocs
	'''

	@staticmethod
	def convert_from_base_10(intToConvert, intBase):
		raise NotImplementedError

	@staticmethod
	def convert_to_base_10(intToConvert, intBase):
		raise NotImplementedError
