from robot.parsing.lexer.tokens import Token


class RobotFrameworkParser(object):
    tokens = Token.DATA_TOKENS

    def p_sections(self, p):
        '''sections : section
                    | sections section'''
        append_to_list_value(p)

    def p_section(self, p):
        '''section : setting_section
                   | variable_section
                   | testcase_section
                   | keyword_section
        '''
        p[0] = p[1]

    def p_setting_section(self, p):
        '''setting_section : SETTING_HEADER settings'''
        p[0] = ('settings', p[2])

    def p_settings(self, p):
        '''settings : setting
                    | settings setting'''
        append_to_list_value(p)

    def p_setting(self, p):
        '''setting : setting_name arguments '''
        p[0] = (p[1], p[2])

    def p_setting_name(self, p):
        '''setting_name : DOCUMENTATION
                        | SUITE_SETUP
                        | SUITE_TEARDOWN
                        | METADATA
                        | TEST_SETUP
                        | TEST_TEARDOWN
                        | TEST_TEMPLATE
                        | TEST_TIMEOUT
                        | FORCE_TAGS
                        | DEFAULT_TAGS
                        | LIBRARY
                        | RESOURCE
                        | VARIABLES
                        | SETUP
                        | TEARDOWN
                        | TEMPLATE
                        | TIMEOUT
                        | TAGS
                        | ARGUMENTS
                        | RETURN
        '''
        p[0] = p[1]

    def p_variable_section(self, p):
        '''variable_section : VARIABLE_HEADER variables'''
        p[0] = ('variables', p[2])

    def p_variables(self, p):
        '''variables : variable
                    | variables variable'''
        append_to_list_value(p)

    def p_variable(self, p):
        'variable : VARIABLE arguments'
        p[0] = (p[1], p[2])

    def p_testcase_section(self, p):
        '''testcase_section : TESTCASE_HEADER tests_or_keywords'''
        p[0] = ('testcases', p[2])

    def p_keyword_section(self, p):
        '''keyword_section : KEYWORD_HEADER tests_or_keywords'''
        p[0] = ('keywords', p[2])

    def p_tests_or_keywords(self, p):
        '''tests_or_keywords : test_or_keyword
                    | tests_or_keywords test_or_keyword'''
        append_to_list_value(p)

    def p_test_or_keyword(self, p):
        '''test_or_keyword : NAME
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
                     | tc_uk_setting
                     | step
        '''
        p[0] = p[1]

    def p_tc_uk_setting(self, p):
        '''tc_uk_setting : setting_name arguments '''
        p[0] = ('setting', p[1], p[2])

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
        '''forloop : FOR arguments FOR_SEPARATOR arguments foritems END'''
        p[2].append(p[3])
        p[0] = ('step', None, 'FOR', p[2] + p[4], p[5])

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
        '''assignments : ASSIGN
                     | assignments ASSIGN'''
        append_to_list_value(p)

    def p_arguments(self, p):
        '''arguments : ARGUMENT
                     | arguments ARGUMENT'''
        append_to_list_value(p)

    def p_error(self, e):
        print(e)
        print("Parse error:" + str(e))


def append_to_list_value(p):
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        value = p[1]
        if (p[2]) is not None:
            value.append(p[2])
        p[0] = value
