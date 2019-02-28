from robot.parsing.vendor import lex, yacc

tokens = (
    'SETTING_HEADER',
    'VARIABLE_HEADER',
    'TEST_CASE_HEADER',
    'KEYWORD_HEADER',
    'DATA'
)

SPACE_SEPARATED = r'^\*+\ ?{}?\ ?\**(\s*|\s\s.*)$'
PIPE_SEPARATED = r'^\|\s+\*+\s?{}\s?\**.*$'
t_SETTING_HEADER = r'(?im)({}|{})'.format(SPACE_SEPARATED.format('settings?'), PIPE_SEPARATED.format('settings'))
t_VARIABLE_HEADER = r'(?im)({}|{})'.format(SPACE_SEPARATED.format('variables?'), PIPE_SEPARATED.format('variables'))
t_TEST_CASE_HEADER = r'(?im)({}|{})'.format(SPACE_SEPARATED.format('test\ cases?'), PIPE_SEPARATED.format('test\ cases?'))
t_KEYWORD_HEADER = r'(?im)({}|{})'.format(SPACE_SEPARATED.format('keywords?'), PIPE_SEPARATED.format('keywords?'))
t_DATA = r'.+'
t_ignore = '\n'


def t_error(t):
    print("Section parser, illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def p_sections_section(p):
    '''sections : section
                | sections section'''
    if len(p) == 2:
        name, data = p[1]
        p[0] = {name: data}
    else:
        sections = p[1]
        name, data = p[2]
        if name in sections:
            data = sections[name] + '\n' + data
        sections[name] = data
        p[0] = sections


def p_section(p):
    '''section : setting_section
               | variable_section
               | testcase_section
               | keyword_section'''
    p[0] = p[1]


def p_setting_section(p):
    'setting_section : SETTING_HEADER section_data'
    p[0] = ('SETTING', p[2])


def p_variable_section(p):
    'variable_section : VARIABLE_HEADER section_data'
    p[0] = ('VARIABLE', p[2])


def p_testcase_section(p):
    'testcase_section : TEST_CASE_HEADER section_data'
    p[0] = ('TESTCASE', p[2])


def p_keyword_section(p):
    'keyword_section : KEYWORD_HEADER section_data'
    p[0] = ('KEYWORD', p[2])


def p_section_data(p):
    '''section_data : DATA
                    | section_data DATA'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + '\n' + p[2]


def p_error(e):
    print("Parse error:",  e)


parser = yacc.yacc()


def section_parser(data):
    return parser.parse(data, lexer=lexer)
