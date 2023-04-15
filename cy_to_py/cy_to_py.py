'''
in here there shall be the cython to python execution code
'''

from .str_helpers import remove_delim_spaces

C_TYPE_KEYWORDS = [
    'int',
    'long',
    'float',
    'double',
    'char'
]

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

class FuncArg:
    '''
    FuncArg shall represent a function argument, which should then be
    pythonized some way
    '''
    def __init__(self, raw_arg):
        self.cy_type = None
        self.field_name = None
        self.py_type = None
        self.default_val = None
        self.parse_raw_arg(raw_arg = raw_arg)

    def parse_raw_arg(self, raw_arg):
        '''first_char_pos = 0
        while first_char_pos < len(raw_arg) and raw_arg[first_char_pos] == ' ':
            first_char_pos += 1
        next_space_pos = first_char_pos + 1
        while next_char_pos < len(raw_arg) and raw_arg[first_char_pos] != ' ':
            next_char_pos += 1
        first_word = raw_arg[first_char_pos : next_space_pos+1]'''

        #let's do something different instead, start from the back
        last_pos_eval = len(raw_arg)
        pos = last_pos_eval - 1
        while pos >= 0 and (self.default_val is None or self.py_type is None):
            while pos >= 0 and raw_arg[pos] not in {':', '='}:
                pos -= 1
            if pos >= 0:
                caught_substring = raw_arg[pos + 1 : last_pos_eval]
                if raw_arg[pos] == ':':
                    self.py_type = remove_delim_spaces(caught_substring)
                if raw_arg[pos] == '=':
                    self.default_val = remove_delim_spaces(caught_substring)
                last_pos_eval = pos
                pos -= 1
        #at this point i sould take stuff from last_pos_eval and evaluate
        #that as a string with field name and eventual cython types
        remaing_substring = raw_arg[:last_pos_eval]
        values_list = [elem for elem in remaing_substring.split(' ') if elem]
        self.field_name = values_list[-1]
        if len(values_list) > 1:
            self.cy_type = ' '.join(values_list[:-1])
    
    def pythonize(self):
        result = self.field_name
        if self.py_type is not None:
            result += ' : {}'.format(self.py_type)
        if self.default_val is not None:
            result += ' = {}'.format(self.default_val)
        return result
        

