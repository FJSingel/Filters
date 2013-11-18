"""
Created on Nov 14, 2013

@author: Frank Singel
FJS52@case.edu

This module manages the creation and function of filters.

"""

from __future__ import division
import copy
import sys 

LIMITLESS = -1;

class Filter(object):
    """
    Parent class for other filters
    """
    def __init__(self, size):
        """
        Constructor............................
        """
        self.memory_size = size
        self.values = []
        self.outputs = []
        
    def reset(self):
        """
        Resets the values previous input so far
        """
        self.values = []
        self.outputs = []

    def add(self, value):
        """
        Adds a value to the filter
        """
        self.values.append(value)

        if len(self.values) > self.memory_size and self.memory_size != LIMITLESS:
            self.values = self.values[1:]

        self.outputs.append(self.evaluate())

    def evaluate(self):
        raise NotImplementedError("This needs implemented")

class MaxFilter(Filter):
    def evaluate(self):
        if len(self.values) == 0:
            return 0
        return max(self.values)

class MinFilter(Filter):
    def evaluate(self):
        if len(self.values) == 0:
            return 0
        return min(self.values)

class AvgFilter(Filter):
    def evaluate(self):
        if len(self.values) == 0:
            return 0
        total = sum(self.values)/len(self.values)
        return total

class CascadeFilter(Filter):
    """
    Lets you feed one filter into another
    """
    def __init__(self, first_filter, second_filter):
        self.first = first_filter
        self.second = second_filter
        self.outputs = []

    def add(self, value):
        self.first.add(value)
        self.second.add(self.first.evaluate())
        self.outputs.append(self.second.evaluate())

    def evaluate(self):
        return self.second.evaluate()

class ScalarLinearFilter(Filter):
    """
    Funny working filter...
    ...I don't understand it.
    """
    def __init__(self, ins, outs):
        '''ins are input weights b, and outs are output weights a'''
        self.in_weights = ins
        self.out_weights = outs
        self.inputs = []
        self.outputs = []
    
    def add(self, value):
        #output = (input + prev input) * weight b - previous output * weight a

        if len(self.inputs) == 0:
            self.inputs.append(value)
            input_vals = self.inputs[0]*self.in_weights[0]
            self.outputs.append(input_vals)
        else:
            input_vals= (value+self.inputs[-1])*self.in_weights[len(self.inputs)-1]
            output_vals = self.outputs[-1]*self.out_weights[len(self.outputs)-1]
            self.inputs.append(value)
            self.outputs.append(input_vals-output_vals)
        return self.outputs[-1]

    def reset(self, value):
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
        self.gain = multiplier

    def evaluate(self):
        return self.values[-1] * self.gain

class BinomialFilter(FIRFilter):
    """
    It has coefficients based on length:
            1
           1 1
          1 2 1
         1 3 3 1
    """
    def __init__(self):
        self.gain = []
        self.values = []
        self.outputs = []

    def add(self, value):
        self.values.append(value)
        self._grow_gain()

    def _grow_gain(self):
        if(self.gain == []):
            self.gain = [1]
        else:
            temp_gain = [1]      # 1 2 
            #self.gain.append(0)  # 1 1 0
            for index, value in enumerate(self.gain):
                if index == (len(self.gain)-1):
                    temp_gain.append(1)
                else:
                    temp_gain.append(value + self.gain[index + 1])
            self.gain = temp_gain

        

