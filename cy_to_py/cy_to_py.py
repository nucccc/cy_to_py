'''
in here there shall be the cython to python execution code
'''

from .str_helpers import remove_delim_spaces

from .keyws import *

from abc import ABC, abstractmethod

from typing import List

C_TYPE_KEYWORDS = [
    'int',
    'long',
    'float',
    'double',
    'char'
]

SEPS = {
    ' ',
    ''
}

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

#before everything i would just need something that checks me if an instruction
#is a variable defintion
def is_var_def(cmd : str) -> bool:
    '''
    is_var_def shall verify if a command is variable declaration
    '''
    cmd_defs = cmd.split(',')
    def_start = cmd_defs[0]
    def_elems = def_start.split(' ')
    if def_elems[0] != CY_VAR_DEF:
        return False
    for elem in def_elems[1:]:
        if elem in C_TYPES:
            return True
    return False

class FuncArg:
    '''
    FuncArg shall represent a function argument, which should then be
    pythonized some way
    '''
    def __init__(self, raw_arg : str):
        self.cy_type = None
        self.field_name = None
        self.py_type = None
        self.default_val = None
        self.parse_raw_arg(raw_arg = raw_arg)

    def parse_raw_arg(self, raw_arg : str):
        '''
        parse_raw_arg shall take in input the raw string representing the
        function argument, and then parse it to extrapolate the field name,
        together with eventual types and default values
        '''
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
    
    def pythonize(self) -> str:
        '''
        pythonize returns the corresponding function argument as python code
        '''
        result = self.field_name
        if self.py_type is not None:
            result += ' : {}'.format(self.py_type)
        if self.default_val is not None:
            result += ' = {}'.format(self.default_val)
        return result
    
def comment_present(cmd : str) -> int:
    '''
    comment_present is going to tell if a comment is present at a certain line
    '''
        
#now there are certain calls that require some more lines eventually
def continues_in_next_line(cmd : str) -> bool:
    '''
    continues_in_next_line
    '''

def makes_sense_as_syntactical_word(word : str) -> bool:
    '''
    makes_sense_as_syntactical_word shall return if stuff extrapolated from
    sep_syntactical_words
    '''
    print('invoked')
    #well if the length of a string is 0 then i shall return false
    if len(word) == 0:
        return False
    #then i check if there only spaces
    all_spaces = True
    for char in word:
        if char != ' ':
            all_spaces = False
            break
    if all_spaces:
        return False
    #if i passed all checks i return false
    return True

def sep_syntactical_words(cmd : str) -> List[str]:
    '''
    sep_syntactical_words shall in some still unknown way take a command and
    return its parts

    also it separates a comment nobody knows why
    '''
    elems = list()
    first_char = 0
    special_context = False
    for i, char in enumerate(cmd):
        if not special_context:
            if char in SEPS:
                if makes_sense_as_syntactical_word( cmd[first_char:i] ):
                    print( cmd[first_char:i] )
                    elems.append( cmd[first_char:i] )
                first_char = i + 1
        if char == '#':
            if makes_sense_as_syntactical_word( cmd[first_char:i] ):
                print( cmd[first_char:i] )
                elems.append( cmd[first_char:i] )
            elems.append(cmd[i:])
            return elems
    if makes_sense_as_syntactical_word( cmd[first_char:] ):
        elems.append( cmd[first_char:] )
    return elems

def sep_commands(code : str) -> List[str]:
    '''
    okay i don't know where this is going but i guess i'll write some stuff

    here i would like something that separates various portions of code into
    commands, don't know how don't know why
    '''
    cmds = list()
    expected_break = '\n'
    first_keyw = None
    start = 0
    evaluating_cdef_doubt = False

    #i shall loop through all my characters
    for i, char in enumerate(code):
        if char == expected_break:
            start = i + 1
            cmds.append( code[start:i] )
            expected_break = '\n'
            first_keyw = None
            evaluating_cdef_doubt = False
        elif first_keyw is None and char in SEPS:
            first_keyw = code[start:i]
            #eventually depending on the first keyword i shall modify the expected break
            if first_keyw in CONTROL_KEYWS + FUNC_DEF_STARTS and first_keyw != CY_VAR_DEF:
                expected_break = ':'
            elif first_keyw == CY_VAR_DEF:
                #well in this case i shall see from other keywords which one shall be the ending point
                evaluating_cdef_doubt = True
                #i will then check whether or not there is a character defined as
                #something that just allows to say that this will be a function
                #or a variable declaration
        elif evaluating_cdef_doubt:
            if char in {',', '='}:
                evaluating_cdef_doubt = False
            elif char == '(':
                evaluating_cdef_doubt = False
                expected_break = ':'        
    
    return cmds

class ReadingContext(ABC):
    '''
    okay maybe i need a reading context, maybe i will stack them in order to know
    in which condition i am
    '''
    
    @abstractmethod
    def contextEnd(self, s : str, i : int) -> bool:
        '''
        contextEnd shall tell me if the context ends with character at pos i of string s
        '''
        pass

    @abstractmethod
    def isNaturalLanguage(self) -> bool:
        pass

class ReadingContextStr(ReadingContext):
    '''
    this shall be a multi line stuff
    '''
    _quote_mark : str = '\''

    def __init__(self, quote_mark : None | str):
        if quote_mark is not None:
            self._quote_mark = quote_mark

    def getQuoteMark(self) -> str:
        return self._quote_mark

    def contextEnd(self, s: str, i: int) -> bool:
        quote_mark = self.getQuoteMark()
        qm_len = len(quote_mark)
        if i < 2:
            return False
        if s[i-qm_len+1:i+1] == self.getQuoteMark():
            if i > qm_len - 1 and s[i-qm_len] == '\\':
                    return False
            else:
                return True
        return False

    def isNaturalLanguage(self) -> bool:
        return True

class ReadingContextComment(ReadingContext):
    '''
    this shall be a multi line stuff
    '''

    def contextEnd(self, s: str, i: int) -> bool:
        return s[i] == '\n'

    def isNaturalLanguage(self) -> bool:
        return True
    
class ReadingContextTabExp(ReadingContext):
    '''
    this should be expressions which terminate in a ':' character, usually
    imposing a subsequent tab
    '''

    def contextEnd(self, s: str, i: int) -> bool:
        return s[i] == ':'

    def isNaturalLanguage(self) -> bool:
        return False

class ReadingContextExp(ReadingContext):
    '''
    this should be normal expressions
    '''

    def contextEnd(self, s: str, i: int) -> bool:
        return s[i] == '\n'

    def isNaturalLanguage(self) -> bool:
        return False

STR_SEPS = [
    '\'',
    '"'
]

def multilineReadingContext(s : str, i : int) -> bool:
    '''
    this shall tell me if the following reading context is a multiline one,
    which is the case when 3 consecutive such chars happen to be in there
    '''
    quote_char = s[i]
    if i + 2 >= len(s):
        return False
    if s[i+1] == s[i+2] == quote_char:
        return True
    return False