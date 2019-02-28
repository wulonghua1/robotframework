
tokens = ('VARIABLE_NAME', 'VALUE', 'SEPARATOR', 'CONTINUATION')

t_ignore_SEPARATOR = r'\ {2,}'
t_VARIABLE_NAME = r'(?m)^[$@&]\{.+?\}(\ ?=)?'
t_ignore_CONTINUATION = r'(?m)^\.\.\.'
t_VALUE = r'(\S+\ )*\S+'

t_ignore = '\r?\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
