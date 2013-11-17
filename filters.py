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
        self.short_term = []
        self.long_term = []
        print "Initted with size of: " + str(self.memory_size)
        
    def reset(self):
        """
        Resets the values previous input so far
        """
        #store return values first
        self.short_term = []
        self.long_term = []
        print "Reset"

    def add(self, value):
        """
        Adds a value to the filter
        """
        self.short_term.append(value)
        self.long_term.append(value)
        print ("Added" + str(value))

        if len(self.short_term) > self.memory_size:
            print "Forgot" + str(self.short_term[0])
            self.short_term = self.short_term[1:]

    def evaluate(self):
        raise NotImplementedError("This needs implemented")

class MaxFilter(Filter):
    def evaluate(self):
        if len(self.short_term) == 0:
            return [0,0]
        return [max(self.short_term), max(self.long_term)]

class MinFilter(Filter):
    def evaluate(self):
        if len(self.short_term) == 0:
            return [0,0]
        return [min(self.short_term), min(self.long_term)]

class AvgFilter(Filter):
    def evaluate(self):
        if len(self.short_term) == 0:
            return [0,0]
        print self.short_term
        print sum(self.short_term)
        print len(self.short_term)
        print sum(self.short_term)/len(self.short_term)
        print self.long_term
        return [sum(self.short_term)/len(self.short_term),
                sum(self.long_term)/len(self.short_term)]

class CascadeFilter(Filter):
    def __init__(self, first_filter, second_filter):
        pass
