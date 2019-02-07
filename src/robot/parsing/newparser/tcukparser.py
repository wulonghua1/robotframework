from .util import append_to_list_value

from .tcukspacelexer import TOKENS


class TCUKParser(object):
    tokens = TOKENS

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
        '''forloop : FOR arguments foritems END'''
        p[0] = ('step', None, 'FOR', p[2], p[3])

    def p_foritems(self, p):
        '''foritems : step
                    | foritems step
        '''
        if len(p) == 2:
            p[0] = [p[1][1:]]
        else:
            p[1].append(p[2][1:])
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
