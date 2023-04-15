import unittest

#import python code from the upperfolder
import sys
sys.path.append('../')
import cy_to_py

class TestIsCimport(unittest.TestCase):
    '''
    TestIsCimport shall test the function is_cimport
    '''

    def test_is_cimport(self):
        cimport_codelines = [
            'cimport numpy as np',
            'cimport random module'
        ]
        other_codelines = [
            'import numpy as np',
            'a = 0',
            'import pandas as pd'
        ]
        for cimport_codeline in cimport_codelines:
            self.assertTrue( cy_to_py.is_cimport(cimport_codeline) )
        for other_codeline in other_codelines:
            self.assertFalse( cy_to_py.is_cimport(other_codeline) )

class TestIsFuncDecl(unittest.TestCase):
    def test_is_func_declaration(self):
        func_decl_codelines = [
            'def isAFunc():',
            'cpdef isACpdefFunc():',
            'def funcWithArgs(a : int):'
        ]
        other_codelines = [
            'cdef int a = 0'
            'import numpy as np',
            'a = 0',
            'import pandas as pd'
        ]
        for func_decl_codeline in func_decl_codelines:
            self.assertTrue( cy_to_py.is_func_declaration(func_decl_codeline) )
        for other_codeline in other_codelines:
            self.assertFalse( cy_to_py.is_func_declaration(other_codeline) )

if __name__ == '__main__':
    unittest.main()