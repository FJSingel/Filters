"""
Created on Nov 14, 2013

@author: Frank Singel
FJS52@case.edu

This module manages the creation and function of filters.

"""

import copy
import sys 

class Filter(object):
    """
    Parent class for other filters
    """

    def __init__(self, size):
        """
        Constructor............................
        """
        self.memory_size = size
        self.short = []
        self.long = []
        print "Initted with size of: " + str(self.memory_size)
        
    def reset(self):
        """
        Resets the values previous input so far
        """
        #return values first
        self.short = []
        self.long = []
        print "Reset"

    def add(self, value):
        """
        Adds a value to the filter
        """
        if len(self.short) >= self.memory_size:
            print "Forgot" + str(short[0])
            self.short = self.short[1:]

        self.short.append(value)
        self.long.append(value)
        print ("Added" + str(value))

class MaxFilter(Filter):
    pass

class MinFilter(Filter):
    pass

class AvgFilter(Filter):
    pass

class CascadeFilter(Filter):

    def __init__(self, first_filter, second_filter):
        pass
