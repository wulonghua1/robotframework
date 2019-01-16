from robot.parsing.vendor import lex, yacc

from .util import append_to_list_value

tokens = ('VARIABLE_NAME', 'VALUE', 'SEPARATOR', 'CONTINUATION')

t_ignore_SEPARATOR = r'\ {2,}'
t_VARIABLE_NAME = r'(?m)^[$@&]\{.+?\}(\ ?=)?'
t_ignore_CONTINUATION = r'(?m)^\.\.\.'
t_VALUE = r'(\S+\ )*\S+'

t_ignore = '\r?\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

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

parser = yacc.yacc()

def variable_parser(data):
    return parser.parse(data, lexer=lexer)
