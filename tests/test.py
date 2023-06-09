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
        self.func_name = func_to_test.__name__
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

class TestIsCimport(TestBoolFunc):

    def test_is_cimport(self):
        test_data = BoolFuncTestData(
            func_to_test = cy_to_py.is_cimport,
            true_cases = [
                'cimport numpy as np',
                'cimport random module'
            ],
            false_cases = [
                'import numpy as np',
                'a = 0',
                'import pandas as pd'
            ]
        )
        self.attach_data(test_data=test_data)
        self.run_bool_test()

class TestIsFuncDecl(TestBoolFunc):

    def test_is_func_declaration(self):
        test_data = BoolFuncTestData(
            func_to_test = cy_to_py.is_func_declaration,
            true_cases = [
                'def isAFunc():',
                'cpdef isACpdefFunc():',
                'def funcWithArgs(a : int):'
            ],
            false_cases = [
                'cdef int a = 0'
                'import numpy as np',
                'a = 0',
                'import pandas as pd'
            ]
        )
        self.attach_data(test_data=test_data)
        self.run_bool_test()

class TestHasFuncCallArgs(TestBoolFunc):

    def test_has_func_call_args(self):
        test_data = BoolFuncTestData(
            func_to_test = cy_to_py.has_func_call_args,
            true_cases = [
                'def isAFunc():',
                'cpdef isACpdefFunc():',
                'def funcWithArgs(a : int):'
            ],
            false_cases = [
                'def func_a_caso(())',
                'def func_a_caso(()',
                'def func_a_caso())',
                'def func_a_caso)',
                'def func_a_caso(',
                'def func_a_caso((aaa))',
                'def func_a_caso((a)',
                'def func_a_caso()a)',
                'def func_a_caso)a',
                'def func_a_caso(a',
                'def func_a_caso(a()',
                'def func_a_caso(a))'
            ]
        )
        self.attach_data(test_data=test_data)
        self.run_bool_test()

class TestIsVarDefs(TestBoolFunc):

    def test_is_var_def(self):
        test_data = BoolFuncTestData(
            func_to_test = cy_to_py.is_var_def,
            true_cases = [
                'cdef int a',
                'cdef long a',
                'cdef short a = 7'
            ],
            false_cases = [
                'def funzioneACaso():',
                'a = 0',
                'cdef void funcInvocableInCEnv():',
                'cdef int funcInvocableInCEnvWithVar():'
            ]
        )
        self.attach_data(test_data=test_data)
        self.run_bool_test()

class TestFieldArg(unittest.TestCase):

    def test_parse_field_arg(self):
        arg = cy_to_py.FuncArg('a')
        self.assertEqual(arg.cy_type, None)
        self.assertEqual(arg.py_type, None)
        self.assertEqual(arg.default_val, None)
        self.assertEqual(arg.field_name, 'a')

        arg = cy_to_py.FuncArg('int a')
        self.assertEqual(arg.cy_type, 'int')
        self.assertEqual(arg.py_type, None)
        self.assertEqual(arg.default_val, None)
        self.assertEqual(arg.field_name, 'a')

        arg = cy_to_py.FuncArg('int a = 3')
        self.assertEqual(arg.cy_type, 'int')
        self.assertEqual(arg.py_type, None)
        self.assertEqual(arg.default_val, '3')
        self.assertEqual(arg.field_name, 'a')

        arg = cy_to_py.FuncArg('unsigned int a = 3')
        self.assertEqual(arg.cy_type, 'unsigned int')
        self.assertEqual(arg.py_type, None)
        self.assertEqual(arg.default_val, '3')
        self.assertEqual(arg.field_name, 'a')

        arg = cy_to_py.FuncArg('a : int = 3')
        self.assertEqual(arg.cy_type, None)
        self.assertEqual(arg.py_type, 'int')
        self.assertEqual(arg.default_val, '3')
        self.assertEqual(arg.field_name, 'a')

    def test_pythonize(self):
        arg = cy_to_py.FuncArg('a')
        arg.cy_type = None
        arg.py_type = None
        arg.default_val = None
        arg.field_name = 'a'
        self.assertEqual( 'a', arg.pythonize() )

        arg.py_type = 'str'
        self.assertEqual( 'a : str', arg.pythonize() )

        arg.py_type = None
        arg.default_val = '\'boh\''
        self.assertEqual( 'a = \'boh\'', arg.pythonize() )

        arg.py_type = 'str'
        self.assertEqual( 'a : str = \'boh\'', arg.pythonize() )

class TestMultilineReadingContext(unittest.TestCase):

    def testContextEnd(self):
        rc = cy_to_py.ReadingContextStr('\'')
        self.assertTrue( rc.contextEnd( '\'\'\'abc\'\'\'', 6 ) )
        self.assertFalse( rc.contextEnd( '\'\'\'ab\\\'\'\'', 6 ) )

        rc = cy_to_py.ReadingContextStr('\'\'\'')
        self.assertTrue( rc.contextEnd( '\'\'\'abc\'\'\'', 8 ) )
        self.assertFalse( rc.contextEnd( '\'\'\'abc\'\'\'', 7 ) )
        self.assertFalse( rc.contextEnd( '\'\'\'ab\\\'\'\'', 8 ) )



if __name__ == '__main__':
    unittest.main()