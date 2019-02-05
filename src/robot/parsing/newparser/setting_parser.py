from robot.parsing.vendor import lex, yacc

from .util import append_to_list_value

tokens = ('DOCUMENTATION', 'SETTING', 'UNRECOGNIZED', 'VALUE', 'SEPARATOR', 'CONTINUATION', 'COMMENT')

def t_newline(t):
    r'\r?\n'
    pass

def t_separator(t):
    r'\ {2,}'
    pass

def t_COMMENT(t):
    r'\#.*'
    pass

def t_DOCUMENTATION(t):
    r'Documentation'
    return t

def t_SETTING(t):
    r'(?i)^(Library|Resource|Variables|Suite\ Setup|Suite\ Teardown|Test\ Setup|Test\ Teardown|Default\ Tags|Force\ Tags)'
    return t

def t_CONTINUATION(t):
    r'(?m)^\.\.\.'
    return t

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

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

parser = yacc.yacc()

def setting_parser(data):
    return parser.parse(data, lexer=lexer)
