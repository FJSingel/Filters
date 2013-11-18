"""
Created on Nov 14, 2013

@author: Frank Singel
FJS52@case.edu

This module manages the creation and function of filters.

"""

from __future__ import division

LIMITLESS = -1;

class Filter(object):
    """
    Parent class for other filters
    """
    def __init__(self, size):
        """
        Constructor
        memory_size is how many inputs are remembered
        Other two are the history of inputs and outputs
        """
        if size > 1:
            self.memory_size = size
        else:
            self.memory_size = LIMITLESS
        self.inputs = []
        self.outputs = []
        
    def reset(self):
        """
        Resets the inputs previous input so far
        """
        self.inputs = []
        self.outputs = []

    def add(self, value):
        """
        Adds a value to the filter
        """
        self.number_or_raise(value)
        self.inputs.append(value)
        if len(self.inputs) > self.memory_size and self.memory_size != LIMITLESS:
            self.inputs = self.inputs[1:]
        self.outputs.append(self.evaluate())

    def __eq__(self, other):
        return self.memory_size == other.memory_size and self.outputs == other.outputs

    def evaluate(self):
        raise NotImplementedError("This needs implemented")

    def number_or_raise(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError

class MaxFilter(Filter):
    def evaluate(self):
        if len(self.inputs) == 0:
            return 0
        return max(self.inputs)

class MinFilter(Filter):
    def evaluate(self):
        if len(self.inputs) == 0:
            return 0
        return min(self.inputs)

class AvgFilter(Filter):
    def evaluate(self):
        if len(self.inputs) == 0:
            return 0
        total = sum(self.inputs)/len(self.inputs)
        return total

class CascadeFilter(Filter):
    """
    Lets you feed one filter into another
    """
    def __init__(self, first_filter, second_filter):

        if not isinstance(first_filter, Filter) or not isinstance(second_filter, Filter):
            raise TypeError
        self.first = first_filter
        self.second = second_filter
        self.outputs = []

    def add(self, value):
        self.number_or_raise(value)
        self.first.add(value)
        self.second.add(self.first.evaluate())
        self.outputs.append(self.second.evaluate())

    def evaluate(self):
        return self.second.evaluate()

class ScalarLinearFilter(Filter):
    """
    Creates output equal to the equation:
        Yi = (Xi + Xi-1)*Bi - (Yi-1)*Ai
        Where Y is output value
        X is input value
        B and A are in and out weights
    """
    def __init__(self, ins, outs):
        '''ins are input weights b, and outs are output weights a'''
        self.in_weights = ins
        self.out_weights = outs
        self.inputs = []
        self.outputs = []
    
    def add(self, value):
        #output = (input + prev input) * weight b - previous output * weight a
        self.number_or_raise(value)
        if len(self.inputs) == 0:
            self.inputs.append(value)
            input_vals = self.inputs[0]*self.in_weights[0]
            self.outputs.append(input_vals)
        elif len(self.inputs) == len(self.in_weights) or len(self.inputs) == len(self.out_weights): #If you're out of weights to use, ignore input
            pass
        else:
            input_vals= (value+self.inputs[-1])*self.in_weights[len(self.inputs)-1]
            output_vals = self.outputs[-1]*self.out_weights[len(self.outputs)-1]
            self.inputs.append(value)
            self.outputs.append(input_vals-output_vals)
        return self.outputs[-1]

    def reset(self, value):
        self.number_or_raise(value)
        self.outputs = []
        self.inputs = []
        for index, value in enumerate(self.inputs):
            self.inputs[index] = value
            self.outputs.append(value)


class FIRFilter(Filter):
    """
    Multiplies each value by the constructor's argument
    """
    def __init__(self, multiplier):
        self.number_or_raise(multiplier)
        self.gain = multiplier
        self.inputs = []
        self.outputs = []

    def add(self, value):
        self.number_or_raise(value)
        self.inputs.append(value)
        self.outputs.append(self.evaluate())

    def evaluate(self):
        return self.inputs[-1] * self.gain

class BinomialFilter(ScalarLinearFilter):
    """
    It has in_weights coefficients based on length:
            1
           1 1
          1 2 1
         1 3 3 1
    """
    def __init__(self):
        self.gain = [] #weights
        self.inputs = [] #series of inputs
        self.outputs = [] #history of outputs

    def reset(self):
        self.gain = []
        self.inputs = []
        self.outputs = []

    def add(self, value):
        self.number_or_raise(value)
        self._grow_gain()
        if len(self.inputs) == 0:
            self.inputs.append(value)
            self.outputs.append(value)
        else:
            input_vals = (value+self.inputs[-1])*self.gain[len(self.inputs)-1]
            self.inputs.append(value)
            self.outputs.append(input_vals)
        return self.outputs[-1]

    def _grow_gain(self):
        '''
        Moves the gain list to the next row of Pascal's Triangle
        '''
        if(self.gain == []):
            self.gain = [1]
        else:
            temp_gain = [1]
            for index, value in enumerate(self.gain):
                if index == (len(self.gain)-1):
                    temp_gain.append(1)
                else:
                    temp_gain.append(value + self.gain[index + 1])
            self.gain = temp_gain