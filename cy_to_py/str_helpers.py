'''
this file shall contain helpers to manipulate strings
'''

def remove_delim(input_str : str, delim : str) -> str:
    open = 0
    close = len(input_str) - 1
    while input_str[open] == delim:
        open += 1
    while input_str[close] == delim:
        close -= 1
    return input_str[open : close + 1]

def remove_delim_spaces(input_str : str) -> str:
    '''
    remove_delim_spaces removes spaces at the beginning of a given string
    '''
    return remove_delim(input_str = input_str, delim = ' ')