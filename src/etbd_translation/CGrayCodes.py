'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''

from etbd_translation.BinaryConvertBoolean import BinaryConvertBoolean


class CGrayCodes(object):
	'''
	classdocs
	'''

	@staticmethod
	def binary_to_gray_booleans(blnBinaryBits):
		assert len(blnBinaryBits) == 11

		# 'Converts a binary number represented as a Boolean array to Gray code represented as a Boolean array.

		blnGrayBits = [None] * len(blnBinaryBits)

		blnGrayBits[1] = blnBinaryBits[1]
		for i in range(2, len(blnBinaryBits)):
			blnGrayBits[i] = blnBinaryBits[i] ^ blnBinaryBits[i - 1]

		return blnGrayBits

	@staticmethod
	def gray_to_binary_booleans(blnGrayBits):
		assert len(blnGrayBits) == 11
		raise NotImplementedError

	@staticmethod
	def integer_to_gray(intToConvert):
		raise NotImplementedError

	@staticmethod
	def gray_to_integer(blnGrayBits):
		assert len(blnGrayBits) == 11
		raise NotImplementedError


if __name__ == '__main__':
	for i in range(10):
		blnBits = BinaryConvertBoolean.convert_from_base_10(i)
		grayBits = CGrayCodes.binary_to_gray_booleans(blnBits)

		print(blnBits)
		print(grayBits)
		print("")
