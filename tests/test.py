import unittest

from typing import List

#import python code from the upperfolder
import sys
sys.path.append('../')
import cy_to_py

class BoolFuncTestData:
    '''
    BoolFuncTestData represents the atomic portion of test from which i shall
    test function ingesting a codeline and returning a string
    '''

    def __init__(
            self,
            func_to_test,
            true_cases : List[str],
            false_cases : List[str]
        ):
        self.func_to_test = func_to_test
        self.true_cases = true_cases
        self.false_cases = false_cases

class TestBoolFunc(unittest.TestCase):

    def attach_data(self, test_data : BoolFuncTestData):
        self.test_data = test_data

    def run_bool_test(self):
        for true_codeline in self.test_data.true_cases:
            self.assertTrue( self.test_data.func_to_test(true_codeline) )
        for false_codeline in self.test_data.false_cases:
            self.assertFalse( self.test_data.func_to_test(false_codeline) )

class TestIsCimport2(TestBoolFunc):

    def test_is_cimport(self):
        func_to_test = cy_to_py.is_cimport
        true_cases = [
            'cimport numpy as np',
            'cimport random module'
        ]
        false_cases = [
            'import numpy as np',
            'a = 0',
            'import pandas as pd'
        ]
        test_data = BoolFuncTestData(
            func_to_test=func_to_test,
            true_cases=true_cases,
            false_cases=false_cases
        )
        self.attach_data(test_data=test_data)
        self.run_bool_test()


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