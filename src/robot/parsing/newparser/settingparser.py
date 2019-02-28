from . import setting_lexer
from .util import append_to_list_value

tokens = setting_lexer.tokens


def p_settings(p):
    '''settings : setting
                | settings setting'''
    append_to_list_value(p)


def p_setting(p):
    '''setting : SETTING values
               | DOCUMENTATION docvalues
               | UNRECOGNIZED values
    '''
    p[0] = (p[1], p[2])


def p_values(p):
    '''values : value
              | values value'''
    append_to_list_value(p)


def p_value(p):
    '''value : VALUE'''
    p[0] = p[1]


def p_continuation(p):
    '''value : CONTINUATION'''
    pass


def p_docvalues(p):
    '''docvalues : docvalue
                 | docvalues docvalue'''
    if (len(p) == 2):
        p[0] = [p[1]]
    else:
        if p[2] == '\n' or p[1][-1] == '\n':
            p[1].append(p[2])
        else:
            p[1].append(' ' + p[2])
        p[0] = p[1]


def p_docvalue(p):
    '''docvalue : VALUE'''
    p[0] = p[1]


def p_doccontinuation(p):
    '''docvalue : CONTINUATION'''
    p[0] = '\n'


def p_error(e):
    print("Parse error: ", e)
