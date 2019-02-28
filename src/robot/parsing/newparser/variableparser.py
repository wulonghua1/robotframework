from .util import append_to_list_value
from . import variable_lexer


tokens = variable_lexer.tokens


def p_variables(p):
    '''variables : variable
                | variables variable'''
    append_to_list_value(p)


def p_setting(p):
    'variable : VARIABLE_NAME values'
    p[0] = (p[1], p[2])


def p_value(p):
    '''values : VALUE
              | values VALUE'''
    append_to_list_value(p)


def p_error(e):
    print(e)
