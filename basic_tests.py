"""
Unit tests for filters
Frank Singel

TODO:
LINE NUMBERS ARE SUBJECT TO CHANGE!!!
Locations for structured basis testing
"""

from mock import patch
from StringIO import StringIO

from testify import *

import filters

#Constants for checking error handling
NO_MATCH = "Data is empty or does not match. Exiting.\n"
TOKEN_ERROR = "Error in token: "
NONSEVEN_LIST_ERROR = "List not of appropriate length\n"
EXIT_SUCCESS = True
EXIT_FAILURE = False

class BasisTests(TestCase):
    """
    Tests all conditionals
    """
    pass

class BoundaryTests(TestCase):
    """
    Test for off-by-one errors: just above/below/on min
    Contains most of BadData tests
    """
    def test_min_input(self, output):
        pass

    def test_no_number(self, output):
        pass

class DataFlow(TestCase):
    """
    Test as many if's as possible
    """
    @class_setup
    def setUp(self):
        pass

    def test_multiple_lines(self, output):
        pass

class BadData(TestCase):
    """
    Test some bad data
    """
    def test_bad_number(self, output):
        pass

class StressTest(TestCase):
    """
    Some stress testing
    """

    @suite('stress', reason="Time Intensive Stress Test not needed on every test run")
    def test_more_input(self, output):
        pass

if __name__ == '__main__':
    run()