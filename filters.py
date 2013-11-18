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
        print "Initted with size of: " + str(self.memory_size)
        
    def reset(self):
        """
        Resets the values previous input so far
        """
        self.values = []
        print "Reset"

    def add(self, value):
        """
        Adds a value to the filter
        """
        self.values.append(value)
        print ("Added" + str(value))

        if len(self.values) > self.memory_size and self.memory_size != LIMITLESS:
            print "Forgot" + str(self.values[0])
            self.values = self.values[1:]

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
        print self.values
        print sum(self.values)
        print len(self.values)
        print sum(self.values)/len(self.values)
        total = sum(self.values)/len(self.values)
        print self.values
        return total

class CascadeFilter(Filter):
    def __init__(self, first_filter, second_filter):
        pass
