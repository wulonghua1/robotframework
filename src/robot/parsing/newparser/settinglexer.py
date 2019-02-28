tokens = (
    'DOCUMENTATION',
    'SETTING',
    'UNRECOGNIZED',
    'VALUE',
    'SEPARATOR',
    'CONTINUATION',
    'COMMENT'
)
setting_names = ['Library', 'Resource', ]


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


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
    r'(?i)^(Variables|Suite\ Setup|Suite\ Teardown|Test\ Setup|Test\ Teardown|Default\ Tags|Force\ Tags)'
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
