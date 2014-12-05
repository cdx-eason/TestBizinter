from BizinterClass import BizinterClass

import unittest


class SampleTest(unittest.TestCase):
    def setUp(self):
        print '\ntest start'

    def tearDown(self):
        print '\ntest stop'

    def test_bizinter(self):
        bc = BizinterClass()
        print '\ntest bizinter'
        bc.hitbizinter()

if __name__ == '__main__':
    unittest.main()
