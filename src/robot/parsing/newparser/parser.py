from robot.parsing.lexer.tokens import Token

from .nodes import (
    DataFile, SettingSection, VariableSection, TestCaseSection,
    KeywordSection, Variable, DocumentationSetting, SuiteSetupSetting,
    SuiteTeardownSetting, MetadataSetting, TestSetupSetting,
    TestTeardownSetting, TestTemplateSetting, TestTimeoutSetting,
    ForceTagsSetting, DefaultTagsSetting, LibrarySetting,
    ResourceSetting, VariablesSetting, SetupSetting, TeardownSetting,
    TimeoutSetting, TagsSetting, TemplateSetting, ArgumentsSetting,
    ReturnSetting, TemplateArguments, TestCase, Keyword, KeywordCall, ForLoop)


class RobotFrameworkParser(object):
    tokens = Token.DATA_TOKENS

    def p_datafile(self, p):
        '''datafile : sections'''
        p[0] = DataFile(p[1])

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
        '''setting_section : SETTING_HEADER EOS settings'''
        p[0] = SettingSection(p[3])

    def p_settings(self, p):
        '''settings : setting
                    | settings setting'''
        append_to_list_value(p)

    def p_setting(self, p):
        '''setting : documentation_setting EOS
                   | suite_setup_setting EOS
                   | suite_teardown_setting EOS
                   | metadata_setting EOS
                   | test_setup_setting EOS
                   | test_teardown_setting EOS
                   | test_template_setting EOS
                   | test_timeout_setting EOS
                   | force_tags_setting EOS
                   | default_tags_setting EOS
                   | library_setting EOS
                   | resource_setting EOS
                   | variables_setting EOS
                   | setup_setting EOS
                   | teardown_setting EOS
                   | template_setting EOS
                   | timeout_setting EOS
                   | tags_setting EOS
                   | arguments_setting EOS
                   | return_setting EOS'''
        p[0] = p[1]

    def p_documentation(self, p):
        '''documentation_setting : DOCUMENTATION arguments'''
        p[0] = DocumentationSetting(p[2])

    def p_suite_setup(self, p):
        '''suite_setup_setting : SUITE_SETUP arguments'''
        p[0] = SuiteSetupSetting(p[2])

    def p_suite_teardown(self, p):
        '''suite_teardown_setting : SUITE_TEARDOWN arguments'''
        p[0] = SuiteTeardownSetting(p[2])

    def p_metadata(self, p):
        '''metadata_setting : METADATA arguments'''
        p[0] = MetadataSetting(p[2][0], p[2][1:])

    def p_test_setup(self, p):
        '''test_setup_setting : TEST_SETUP arguments'''
        p[0] = TestSetupSetting(p[2])

    def p_test_teardown(self, p):
        '''test_teardown_setting : TEST_TEARDOWN arguments'''
        p[0] = TestTeardownSetting(p[2])

    def p_test_template(self, p):
        '''test_template_setting : TEST_TEMPLATE arguments'''
        p[0] = TestTemplateSetting(p[2])

    def p_test_timeout(self, p):
        '''test_timeout_setting : TEST_TIMEOUT arguments'''
        p[0] = TestTimeoutSetting(p[2])

    def p_force_tags(self, p):
        '''force_tags_setting : FORCE_TAGS arguments'''
        p[0] = ForceTagsSetting(p[2])

    def p_default_tags(self, p):
        '''default_tags_setting : DEFAULT_TAGS arguments'''
        p[0] = DefaultTagsSetting(p[2])

    def p_library(self, p):
        '''library_setting : LIBRARY arguments'''
        name, args = parse_name_and_args(p)
        p[0] = LibrarySetting(name, args)

    def p_resource(self, p):
        '''resource_setting : RESOURCE arguments'''
        name, args = parse_name_and_args(p)
        p[0] = ResourceSetting(name, args)

    def p_variables_import(self, p):
        '''variables_setting : VARIABLES arguments'''
        name, args = parse_name_and_args(p)
        p[0] = VariablesSetting(name, args)

    def p_setup(self, p):
        '''setup_setting : SETUP arguments'''
        p[0] = SetupSetting(p[2])

    def p_teardown(self, p):
        '''teardown_setting : TEARDOWN arguments'''
        p[0] = TeardownSetting(p[2])

    def p_template(self, p):
        '''template_setting : TEMPLATE arguments'''
        p[0] = TemplateSetting(p[2])

    def p_timeout(self, p):
        '''timeout_setting : TIMEOUT arguments'''
        p[0] = TimeoutSetting(p[2])

    def p_tags(self, p):
        '''tags_setting : TAGS arguments'''
        p[0] = TagsSetting(p[2])

    def p_arguments_setting(self, p):
        '''arguments_setting : ARGUMENTS arguments'''
        p[0] = ArgumentsSetting(p[2])

    def p_return(self, p):
        '''return_setting : RETURN arguments'''
        p[0] = ReturnSetting(p[2])

    def p_variable_section(self, p):
        '''variable_section : VARIABLE_HEADER EOS variables'''
        p[0] = VariableSection(p[3])

    def p_variables(self, p):
        '''variables : variable
                    | variables variable'''
        append_to_list_value(p)

    def p_variable(self, p):
        'variable : VARIABLE arguments EOS'
        p[0] = Variable(p[1], p[2])

    def p_testcase_section(self, p):
        '''testcase_section : TESTCASE_HEADER EOS tests'''
        p[0] = TestCaseSection(p[3])

    def p_keyword_section(self, p):
        '''keyword_section : KEYWORD_HEADER EOS keywords'''
        p[0] = KeywordSection(p[3])

    def p_tests(self, p):
        '''tests : test
                | tests test'''
        append_to_list_value(p)

    def p_keywords(self, p):
        '''keywords : keyword
                    | keywords keyword'''
        append_to_list_value(p)

    def p_test(self, p):
        '''test : NAME EOS
               | NAME EOS body_items'''
        if len(p) == 3:
            p[0] = TestCase(p[1], [])
        else:
            p[0] = TestCase(p[1], p[3])

    def p_keyword(self, p):
        '''keyword : NAME EOS
                    | NAME EOS body_items'''
        if len(p) == 3:
            p[0] = Keyword(p[1], [])
        else:
            p[0] = Keyword(p[1], p[3])


    def p_body_items(self, p):
        '''body_items : body_item
                      | body_items body_item
        '''
        append_to_list_value(p)

    def p_body_item(self, p):
        '''body_item : forloop
                     | setting
                     | step
                     | templatearguments
        '''
        p[0] = p[1]

    def p_step(self, p):
        '''step : KEYWORD EOS
                | KEYWORD arguments EOS'''
        if len(p) == 3:
            p[0] = KeywordCall(None, p[1], [])
        else:
            p[0] = KeywordCall(None, p[1], p[2])

    def p_step_with_assignment(self, p):
        '''step : assignments KEYWORD EOS
                | assignments KEYWORD arguments EOS'''
        if len(p) == 4:
            p[0] = KeywordCall(p[1], p[2], [])
        else:
            p[0] = KeywordCall(p[1], p[2], p[3])

    def p_forloop(self, p):
        '''forloop : FOR arguments FOR_SEPARATOR arguments EOS foritems END EOS'''
        p[0] = ForLoop(p[3], p[2], p[4], p[6])

    def p_foritems(self, p):
        '''foritems : step
                    | foritems step
        '''
        append_to_list_value(p)

    def p_templatearguments(self, p):
        '''templatearguments : arguments EOS'''
        p[0] = TemplateArguments(p[1])

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


def parse_name_and_args(p):
    if p[2]:
        return p[2][0], p[2][1:]
    else:
        return '', []
