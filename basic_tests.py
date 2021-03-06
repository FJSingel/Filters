"""
Created on Nov 14, 2013
Last updated Dec 1, 2013

Unit tests for filters.py
Frank Singel
"""

from testify import *

import filters

class FilterTests(TestCase):
    """Tests each general filter"""
    def test_filter(self):
        """Ensure basic filter doesn't work"""
        filt = filters.Filter(3)
        with assert_raises(NotImplementedError):
            filt.add(5)

    def test_max_limited(self):
        """Add and confirm input of: 1,2,3,1,1,1,4,reset"""
        max_filter = filters.MaxFilter(3)
        max_filter.add(1)
        max_filter.add(2)
        max_filter.add(3)
        max_filter.add(1)
        max_filter.add(1)
        max_filter.add(1)
        max_filter.add(4)
        assert_equals([1,2,3,3,3,1,4], max_filter.outputs)
        max_filter.reset()
        assert_equals([], max_filter.outputs)



    def test_min_limited(self):
        """Add and confirm input of: 1,2,3,3,3,1,0,reset"""
        min_filter = filters.MinFilter(3)
        min_filter.add(1)
        min_filter.add(2)
        min_filter.add(3)
        min_filter.add(3)
        min_filter.add(3)
        min_filter.add(1)
        min_filter.add(0)
        assert_equals([1,1,1,2,3,1,0], min_filter.outputs)
        min_filter.reset()
        assert_equals([], min_filter.outputs)

    def test_avg_limited(self):
        """Add and confirm input of: 3,6,9,9,reset"""
        avg_filter = filters.AvgFilter(3)
        avg_filter.add(3)
        avg_filter.add(6)
        avg_filter.add(9)
        avg_filter.add(9)
        assert_equals([3.0, 4.5, 6.0, 8.0], avg_filter.outputs)
        avg_filter.reset()
        assert_equals([], avg_filter.outputs)

    def test_max_unlimited(self):
        """Add and confirm input of: 1,2,3,1,1,1,4,reset"""
        max_filter = filters.MaxFilter(filters.LIMITLESS)
        max_filter.add(1)
        max_filter.add(2)
        max_filter.add(3)
        max_filter.add(3)
        max_filter.add(3)
        max_filter.add(4)
        assert_equals([1,2,3,3,3,4], max_filter.outputs)
        max_filter.reset()
        assert_equals([], max_filter.outputs)

    def test_min_unlimited(self):
        """Add and confirm input of: 1,2,3,3,3,1,0,reset,1"""
        min_filter = filters.MinFilter(filters.LIMITLESS)
        min_filter.add(1)
        min_filter.add(2)
        min_filter.add(3)
        min_filter.add(3)
        min_filter.add(3)
        min_filter.add(1)
        min_filter.add(0)
        assert_equals([1,1,1,1,1,1,0], min_filter.outputs)
        min_filter.reset()
        min_filter.add(1)
        assert_equals([1], min_filter.outputs)

    def test_avg_unlimited(self):
        """Add and confirm input of: 1,2,3,3,-9,reset"""
        avg_filter = filters.AvgFilter(filters.LIMITLESS)
        avg_filter.add(1)
        avg_filter.add(2)
        avg_filter.add(3)
        avg_filter.add(3)
        avg_filter.add(-9)
        assert_equals([1.0, 1.5, 2.0, 2.25, 0.0], avg_filter.outputs)
        avg_filter.reset()
        assert_equals([], avg_filter.outputs)

    def test_cascade(self):
        """Feed a Max2 filter into a Min3 one using values from pdf"""
        min_filter = filters.MinFilter(3)
        max_filter = filters.MaxFilter(2)
        cascade = filters.CascadeFilter(max_filter, min_filter)

        cascade.add(-1)
        cascade.add(3)
        cascade.add(1)
        cascade.add(2)
        cascade.add(1)
        assert_equals([-1,-1,-1,2,2], cascade.outputs)

    def test_scalar_linear(self):
        """Test input from project description"""
        outs = [.1, .1, .1, .1, .1]
        ins = [.5, .5, .5, .5, .5]
        scalar = filters.ScalarLinearFilter(ins, outs)
        scalar.add(-1)
        scalar.add(1)
        scalar.add(2)
        assert_equals([-0.5, 0.05, 1.495], scalar.outputs)
        scalar.reset(0)
        scalar.add(-1)
        scalar.add(3)
        scalar.add(1)
        scalar.add(2)
        scalar.add(1)
        assert_equals([-0.5, 1.05, 1.895, 1.3105, 1.36895], scalar.outputs)
        scalar.add(2) #test what happens if you have more inputs than weights. Should ignore.
        assert_equals([-0.5, 1.05, 1.895, 1.3105, 1.36895], scalar.outputs)

        #ensure that it doesn't accept unequal weight counts
        with assert_raises(ValueError):
            scalar2 = filters.ScalarLinearFilter(ins, outs[1:])

    def test_FIR(self):
        """Test input of 1,2,3,reset,5 for a filter of gain = 3"""
        fir = filters.FIRFilter(3)
        fir.add(1)
        fir.add(2)
        fir.add(3)
        assert_equals([3,6,9], fir.outputs)
        fir.reset()
        fir.add(5)
        assert_equals([15], fir.outputs)

    def test_binomial(self):
        """Test the growth of pascal's triangle"""
        binom = filters.BinomialFilter()
        binom.add(1)
        binom.add(1)
        binom.add(1)
        binom.add(1)
        binom.add(1)
        assert_equals([1,4,6,4,1], binom.gain)
        binom.add(1)
        assert_equals([1,5,10,10,5,1], binom.gain)
        
    def test_eqs(self):
        """Tests filter equality"""
        min_filter1 = filters.MinFilter(3)
        min_filter2 = filters.MinFilter(3)
        min_filter3 = filters.MinFilter(2)
        max_filter = filters.MaxFilter(3)

        assert_equals(min_filter1, min_filter2)
        assert_not_equal(min_filter1, min_filter3)
        min_filter1.add(5)
        assert_not_equal(min_filter1, min_filter2)
        assert_not_equal(max_filter, min_filter2)
        min_filter2.add(5)
        assert_equals(min_filter1, min_filter2)

if __name__ == '__main__':
    run()