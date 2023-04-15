import unittest

import sys
sys.path.append('../cy_to_py/')
import str_helpers

class TestRemoveDelim(unittest.TestCase):

    def test_remove_delim(self):
        self.assertEqual( 'abc' , str_helpers.remove_delim(' abc ', ' ') )
        self.assertEqual( 'abc' , str_helpers.remove_delim('  abc  ', ' ') )
        self.assertEqual( 'abc' , str_helpers.remove_delim(' abc', ' ') )
        self.assertEqual( 'abc' , str_helpers.remove_delim('abc ', ' ') )
        self.assertEqual( 'abc' , str_helpers.remove_delim('abc', ' ') )

if __name__ == '__main__':
    unittest.main()