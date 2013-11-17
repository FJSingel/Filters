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
EXIT_SUCCESS = True
EXIT_FAILURE = False

class BasisTests(TestCase):
    """
    Tests all conditionals
    """
    def test_max(self):
        max_filter = filters.MaxFilter(3)
        max_filter.add(1)
        assert_equals([1,1], max_filter.evaluate())
        max_filter.add(2)
        assert_equals([2,2], max_filter.evaluate())
        max_filter.add(3)
        assert_equals([3,3], max_filter.evaluate())
        max_filter.add(1)
        assert_equals([3,3], max_filter.evaluate())
        max_filter.add(1)
        assert_equals([3,3], max_filter.evaluate())
        max_filter.add(1)
        assert_equals([1,3], max_filter.evaluate())
        max_filter.add(4)
        assert_equals([4,4], max_filter.evaluate())
        max_filter.reset()
        assert_equals([0,0], max_filter.evaluate())

    def test_min(self):
        min_filter = filters.MinFilter(3)
        min_filter.add(1)
        assert_equals([1,1], min_filter.evaluate())
        min_filter.add(2)
        assert_equals([1,1], min_filter.evaluate())
        min_filter.add(3)
        assert_equals([1,1], min_filter.evaluate())
        min_filter.add(3)
        assert_equals([2,1], min_filter.evaluate())
        min_filter.add(3)
        assert_equals([3,1], min_filter.evaluate())
        min_filter.add(1)
        assert_equals([1,1], min_filter.evaluate())
        min_filter.add(0)
        assert_equals([0,0], min_filter.evaluate())
        min_filter.reset()
        min_filter.add(1)
        assert_equals([1,1], min_filter.evaluate())

    def test_avg(self):
        avg_filter = filters.AvgFilter(3)
        avg_filter.add(1)
        assert_equals([1,1], avg_filter.evaluate())
        avg_filter.add(2)
        assert_equals([1.5,1.5], avg_filter.evaluate())
        avg_filter.add(3)
        assert_equals([2,2], avg_filter.evaluate())
        avg_filter.add(3)
        assert_equals([8/3,3], avg_filter.evaluate())
        avg_filter.reset()
        assert_equals([0,0], avg_filter.evaluate())

class BoundaryTests(TestCase):
    """
    Test for off-by-one errors: just above/below/on min
    Contains most of BadData tests
    """
    def test_min_input(self):
        pass

    def test_no_number(self):
        pass

class DataFlow(TestCase):
    """
    Test as many if's as possible
    """
    @class_setup
    def setUp(self):
        pass

    def test_multiple_lines(self):
        pass

class BadData(TestCase):
    """
    Test some bad data
    """
    def test_bad_number(self):
        pass

class StressTest(TestCase):
    """
    Some stress testing
    """

    @suite('stress', reason="Time Intensive Stress Test not needed on every test run")
    def test_more_input(self):
        pass

if __name__ == '__main__':
    run()