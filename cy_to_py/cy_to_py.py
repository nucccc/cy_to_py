'''
in here there shall be the cython to python execution code
'''

def is_cimport(codeline : str):
    '''
    is_cimport returns me if a codeline is a cimport
    '''
    if len(codeline) < 7:
        return False
    if codeline[:7] == 'cimport':
        return True
    return False

def is_func_declaration(codeline : str):
    '''
    is_func_declaration returns me if a line
    '''
    if (codeline[:5] == 'cpdef' or codeline[:3] == 'def') and codeline[-1] == ':':
        return True
    return False

def to_rem(codeline : str):
    '''
    to_rem returns if the codeline needs to be removed
    '''
    if is_cimport(codeline=codeline):
        return True
    return False

def ctp_line(codeline : str):
    '''
    ctp_line takes in input a code line and converts it back to python from cython
    '''
    pass