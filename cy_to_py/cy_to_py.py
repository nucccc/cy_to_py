'''
in here there shall be the cython to python execution code
'''

def is_cimport(codeline : str) -> bool:
    '''
    is_cimport returns me if a codeline is a cimport
    '''
    if len(codeline) < 7:
        return False
    if codeline[:7] == 'cimport':
        return True
    return False

def has_func_call_args(codeline : str) -> bool:
    '''
    has_func_call_args returns me if there is a set of arguments,
    which is a valid condition for a function
    '''
    open_par_pos = -1
    close_par_pos = -1
    for pos, c in enumerate(codeline):
        if c == '(':
            if open_par_pos == -1:
                open_par_pos = pos
            else:
                #in such case this would be the second open parenthesis, and i 
                #thus return false
                return False
        if c == ')':
            if open_par_pos == -1:
                #in case i still didn't find an opening parenthesis then i
                #should return false, since such close parenthesis doesn't
                #make sense
                return False
            elif close_par_pos == -1:
                close_par_pos = pos
            else:
                return False
    if open_par_pos == -1 or close_par_pos == -1:
        return False
    return True

def is_func_declaration(codeline : str) -> bool:
    '''
    is_func_declaration returns me if a line
    '''
    if codeline[-1] != ':':
        return False
    if codeline[:5] != 'cpdef' and codeline[:3] != 'def' and codeline[:4] != 'cdef':
        return False
    return True

def to_rem(codeline : str) -> bool:
    '''
    to_rem returns if the codeline needs to be removed
    '''
    if is_cimport(codeline=codeline):
        return True
    return False

def ctp_line(codeline : str) -> str:
    '''
    ctp_line takes in input a code line and converts it back to python from cython
    '''
    pass