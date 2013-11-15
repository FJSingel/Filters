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

    def __init__(self):
        """
        Constructor............................
        """
        pass
        
    def reset(self):
        """
        Resets the values previous input so far
        """
        pass

    def 

class MaxFilter(Filter, size):
    pass

class MinFilter(Filter, size):
    pass

class AvgFilter(Filter, size):
    pass

class CascadeFilter(Filter, first_filter, second_filter):
    pass
