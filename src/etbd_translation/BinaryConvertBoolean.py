'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''


class BinaryConvertBoolean(object):

	@staticmethod
	def convert_from_base_10(intToConvert, num_bits):
		# 'Accept decimal integer, return binary number as Boolean array

		assert num_bits == 0 or 2 ** num_bits >= intToConvert

		blnBits = []
		# Dim numBits As Integer

		while True:
			if intToConvert < 2:
				blnBits.append(bool(intToConvert))
				break
			else:
				blnBits.append(bool(intToConvert % 2))
				intToConvert >>= 1

		if num_bits != 0 and len(blnBits) < num_bits:
			blnBits = [False] * (num_bits - len(blnBits)) + blnBits

		blnBits.reverse()

		# 'Boolean array was built in backwards order so it must be reversed.
		# '(Notice that the zeroth element in the array is not part of the bit sequence.)

		return [None] + blnBits

	@staticmethod
	def convert_to_base_10(blnBits):

		assert len(blnBits) == 11

		# Accept binary number as a Boolean array, return decimal integer.
		# Assumes that the 0th element in the array is not used.

		power = len(blnBits) - 1
		intOutput = 0

		for i in range(1, len(blnBits)):
			power -= 1
			intOutput += (blnBits[i]) * (2 ** power)

		return intOutput
