'''
Created on Mar 22, 2021

@author: bleem
'''

# A target class in the ETBD consists of a range of contiguous values that all generate the same outcome.
# A bitfield in this class refers to an array of integer bits.


class TargetClass(object):
    '''
    classdocs
    '''

    def __init__(self, target_class_index, min_, max_, hyperparams):

        assert min_ <= max_

        self.__target_class_index = target_class_index

        self.__min = min_
        self.__max = max_
        self.__min_bits = TargetClass.convert_to_bitfield(self.__min, hyperparams)
        self.__max_bits = TargetClass.convert_to_bitfield(self.__max, hyperparams)

    def get_size(self):
        return self.__max - self.__min + 1

    def get_target_class_index(self):
        return self.__target_class_index

    def get_min(self):
        return self.__min

    def get_max(self):
        return self.__max

    def get_min_bitfield(self):
        return self.__min_bits

    def get_max_bitfield(self):
        return self.__max_bits

    def contains(self, value):
        return value >= self.get_min() and value <= self.get_max()

    def contains_bitfield(self, bitfield, hyperparams):
        return TargetClass.compare_bitfields(self.get_min_bitfield(), bitfield, hyperparams) <= 0 and TargetClass.compare_bitfields(self.get_max_bitfield(), bitfield, hyperparams) >= 0

    # if field1 > field2, returns 1; if field1 < field2, returns -1; if field1 == field2, returns 0
    # all fields are assumed to be of length equal to _constants.ENV_BITS
    @staticmethod
    def compare_bitfields(field1, field2, hyperparams):
        for i in range(hyperparams.get_env_bits()):
            if field1[i] == field2[i]:
                continue
            elif field1[i] < field2[i]:
                return -1
            else:
                return 1

        return 0

    @staticmethod
    def convert_to_bitfield(value, hyperparams):
        bitstring = [0] * hyperparams.get_env_bits()
        mask = 1
        for i in range(0, hyperparams.get_env_bits()):
            bitstring[hyperparams.get_env_bits() - i - 1] = 1 if (value & mask) else 0
            mask = mask << 1
        return bitstring


if __name__ == "__main__":
    tc = TargetClass(55, 138)
    for i in range(54, 200):
        bitstring = TargetClass.convert_to_bitfield(i)
        print(str(i) + " " + str(tc.contains_bitfield(bitstring)))
