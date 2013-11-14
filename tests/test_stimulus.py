import unittest
from nose.tools import *
import stimulus

class BasicTest(unittest.TestCase):

    def setUp(self):
        print "SETUP!"
        
    def tearDown(self):
        print "TEAR DOWN!"
        
    def test_basic(self):
        assert_equal(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()