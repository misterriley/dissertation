'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''


class BinaryConvertBoolean(object):

	@staticmethod
	def convert_from_base_10(intToConvert):
		# 'Accpet decimal integer, return binary number as Boolean array

		blnBits = [None]
		# Dim numBits As Integer

		while True:
			if intToConvert < 2:
				blnBits.append(bool(intToConvert))
				break
			else:
				blnBits.append(bool(intToConvert % 2))
				intToConvert = int(intToConvert / 2)

		to_reverse = blnBits[1:]
		to_reverse.reverse()

		# 'Boolean array was built in backwards order so it must be reversed.
		# '(Notice that the zeroth element in the array is not part of the bit sequence.)

		return blnBits[0:1] + to_reverse

	@staticmethod
	def convert_to_base_10(binToConvert):
		raise NotImplementedError
