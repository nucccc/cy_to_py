'''
in here somehow keywords shall be called and instantiated
'''

MULTI_LINE_DELIM = '\'\'\''

CONTROL_KEYWS = {
    'for',
    'while',
    'if',
    'elif',
    'else'
}

C_TYPES = {
    'int',
    'float',
    'double',
    'short',
    'long'
}

CY_VAR_DEF = 'cdef'

CY_TO_PY_TYPE = {
    'int' : 'int',
    'float' : 'float',
    'double' : 'float',
    'short' : 'int',
    'long' : 'int'
}

FUNC_DEF_STARTS = {
    'def',
    'cdef',
    'cpdef'
}