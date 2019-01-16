from robot.parsing.vendor import lex, yacc

from .util import append_to_list_value

tokens = ('SETTING', 'UNRECOGNIZED', 'VALUE', 'SEPARATOR', 'CONTINUATION', 'COMMENT')

t_ignore = '\r?\n'

def t_separator(t):
    r'\ {2,}'
    pass

def t_COMMENT(t):
    r'\#.*'
    pass

def t_SETTING(t):
    r'(?i)^(Library|Resource|Documentation|Variables|Suite\ Setup|Suite\ Teardown|Test\ Setup|Test\ Teardown|Default\ Tags|Force\ Tags)'
    return t

def t_ignore_CONTINUATION(t):
     r'(?m)^\.\.\.'
     pass

def t_UNRECOGNIZED(t):
    r'^(\S+\ )*\S+'
    return t


def t_VALUE(t):
    r'(\S+\ )*\S+'
    return t


lexer = lex.lex()

def p_settings(p):
    '''settings : setting
                | settings setting'''
    append_to_list_value(p)

def p_setting(p):
    '''setting : SETTING values
               | UNRECOGNIZED values
    '''
    p[0] = (p[1], p[2])

def p_value(p):
    '''values : VALUE
              | values VALUE'''
    append_to_list_value(p)

def p_error(e):
    print("Parse error:" + e)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

parser = yacc.yacc()

def setting_parser(data):
    return parser.parse(data, lexer=lexer)
