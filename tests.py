from dijkstra import TestDijkstra
from max_flow import TestMaxFlow
from primes import TestPrimesLibrary
from sort import TestSortLibrary
import unittest


test_suite = unittest.TestSuite()
test_suite.addTest(TestDijkstra("test_dijkstra"))
test_suite.addTest(TestMaxFlow("test_max_flow"))
test_suite.addTest(TestPrimesLibrary("test_by_comparison"))
test_suite.addTest(TestSortLibrary("test_mergesort_random"))
test_suite.addTest(TestSortLibrary("test_mergesort"))

unittest.main()
