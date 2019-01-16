import re

from .util import append_to_list_value


class TCUKParser(object):
    tokens = ('COMMENT', 'NAME', 'SEPARATOR', 'KEYWORD', 'ARGUMENT', 'FOR', 'CONTINUATION', 'ASSIGNMENT', 'SETTING', 'SETTING_VALUE', 'INDENT')

    def t_error(self, t):
        print(t)
        print("TCUKparser illegal character '%s'" % t.value)
        t.lexer.skip(1)

    t_ignore = '\r?\n'

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_CONTINUATION(self, t):
        r'(?m)^\ {2,}\.\.\.'
        pass

    def t_SETTING(self, t):
        r'(?i)\[.*\]'
        self._setting_seen = True
        t.value = t.value[1:-1].lower()
        return t

    def t_INDENT(self, t):
        r'\\'
        return t

    def t_NAME(self, t):
        r'^(\S+\ )*\S+'
        self._kw_seen = False
        self._setting_seen = False
        return t

    def t_first_value(self, t):
        r'(^\ {2,})(?!\.\.\.)'
        self._kw_seen = False
        self._setting_seen = False
        self._in_for_loop = False

    def t_value(self, t):
        r'(\S+\ )*\S+'
        if self._setting_seen:
            t.type = 'SETTING_VALUE'
        elif self._kw_seen or self._in_for_loop:
            t.type = 'ARGUMENT'
        elif re.match(r'[$@&]\{.+\}( ?=)?', t.value):
            t.type = 'ASSIGNMENT'
        elif t.value == ': FOR':
            t.type = 'FOR'
            self._in_for_loop = True
        else:
            t.type = 'KEYWORD'
            self._kw_seen = True
        return t

    t_ignore_SEPARATOR = r'\ {2,}'

    def p_testcases(self, p):
        '''testcases : testcase
                    | testcases testcase'''
        append_to_list_value(p)

    def p_testcase(self, p):
        '''testcase : NAME
                    | NAME body_items'''
        if len(p) == 2:
            p[0] = (p[1], [], [])
        else:
            p[0] = (p[1], p[2][0], p[2][1])

    def p_body_items(self, p):
        '''body_items : body_item
                      | body_items body_item
        '''
        if len(p) == 2:
            p[0] = ([], [])
            value = p[1]
        else:
            p[0] = p[1]
            value = p[2]
        
        if value[0] == 'setting':
            p[0][0].append(value[1:])
        else:
            p[0][1].append(value[1:])

    def p_body_item(self, p):
        '''body_item : forloop
                     | setting 
                     | step
        '''
        p[0] = p[1]

    def p_setting(self, p):
        '''setting : SETTING setting_values'''
        p[0] = ('setting', p[1], p[2])

    def p_setting_values(self, p):
        '''setting_values : SETTING_VALUE
                          | setting_values SETTING_VALUE'''
        append_to_list_value(p)

    def p_step(self, p):
        '''step : KEYWORD
                | KEYWORD arguments'''
        if len(p) == 2:
            p[0] = ('step', None, p[1], [])
        elif len(p) == 3:
            p[0] = ('step', None, p[1], p[2])

    def p_step_with_assignment(self, p):
        '''step : assignments KEYWORD
                | assignments KEYWORD arguments'''
        if len(p) == 3:
            p[0] = ('step', p[1], p[2], [])
        else:
            p[0] = ('step', p[1], p[2], p[3])

    def p_forloop(self, p):
        '''forloop : FOR arguments foritems'''
        p[0] = ('step', None, p[1], p[2], p[3])

    def p_foritems(self, p):
        '''foritems : INDENT step
                    | foritems INDENT step
        '''
        if len(p) == 3:
            p[0] = [p[2][1:]]
        else:
            p[1].append(p[3][1:])
            p[0] = p[1]

    def p_assignments(self, p):
        '''assignments : ASSIGNMENT
                     | assignments ASSIGNMENT'''
        append_to_list_value(p)

    def p_arguments(self, p):
        '''arguments : ARGUMENT
                     | arguments ARGUMENT'''
        append_to_list_value(p)

    def p_error(self, e):
        print("Parse error:" + str(e))
