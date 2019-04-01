import os

from robot.parsing.vendor import yacc

from robot.output import LOGGER
from robot.utils import Utf8Reader
from robot.parsing.lexer import RobotFrameworkLexer

from .parser import RobotFrameworkParser
from .ast import KeywordCall, ForLoop


class Step(object):
    def __init__(self, assign, name, args):
        self.assign = assign
        self.name = name
        self.args = args

    def is_comment(self):
        return False

    def is_for_loop(self):
        return False


def report_invalid_syntax(datafile, message, level='ERROR'):
    initfile = getattr(datafile, 'initfile', None)
    path = os.path.join(datafile.source, initfile) if initfile else datafile.source
    LOGGER.write("Error in file '%s': %s" % (path, message), level)


def replace_curdirs_in(datafile, values):
    if datafile.directory:
        curdir = datafile.directory.replace('\\','\\\\')
        old, new = '${CURDIR}', curdir
        return [v if old not in v else v.replace(old, new) for v in values]


def populate_settings(populator, section):
    settings = populator._datafile.setting_table
    settings.set_header('Settings')
    for s in section.settings:
        key = s.name.lower()
        values = s.value
        values = replace_curdirs_in(populator._datafile, values)
        if key == 'resource':
            settings.add_resource(values[0])
        elif key == 'library':
            settings.add_library(values[0], values[1:])
        elif key == 'variables':
            settings.add_variables(values[0], values[1:])
        else:
            setting = {
                'documentation': settings.doc,
                'suite setup': settings.suite_setup,
                'suite teardown': settings.suite_teardown,
                'test setup': settings.test_setup,
                'test teardown': settings.test_teardown,
                'force tags': settings.force_tags,
                'default tags': settings.default_tags,
                'test timeout': settings.test_timeout,
                'test template': settings.test_template
            }.get(key)
            if setting is not None:
                setting.populate(values)
            else:
                report_invalid_syntax(populator._datafile, "Non-existing setting '{}'.".format(s.name))


def populate_variables(populator, section):
    datafile = populator._datafile
    datafile.variable_table.set_header('Variables')
    for var in section.variables:
        datafile.variable_table.add(var.name, populator._replace_curdirs_in(var.value))


def create_step(parent, step, datafile):
    from robot.parsing.model import ForLoop
    if type(step).__name__ == 'ForLoop':
        s = ForLoop(parent, replace_curdirs_in(datafile, step.args))
        for kw in step.keyword_calls:
            fs = Step(kw.assign or [], kw.keyword, replace_curdirs_in(datafile, kw.args))
            s.steps.append(fs)
    else:
        s = Step(step.assign or [], step.keyword, replace_curdirs_in(datafile, step.args))
    return s


def populate_tests(populator, section):
    datafile = populator._datafile
    datafile.testcase_table.set_header('Test cases')
    for test in section.tests:
        t = datafile.testcase_table.add(test.name)
        for item in test.body:
            if isinstance(item, KeywordCall):
                t.steps.append(create_step(t, item, datafile))
            elif isinstance(item, ForLoop):
                t.steps.append(create_step(t, item, datafile))
            else:
                name = item.name[1:-1].lower()
                setting = {
                    'timeout': t.timeout,
                    'documentation': t.doc,
                    'setup': t.setup,
                    'teardown': t.teardown,
                    'template': t.template,
                    'tags': t.tags
                }[name]
                setting.populate(item.value)


def populate_kws(populator, section):
    datafile = populator._datafile
    datafile.keyword_table.set_header('Keywords')
    for kw in section.keywords:
        k = datafile.keyword_table.add(kw.name)
        for item in kw.body:
            if isinstance(item, KeywordCall):
                k.steps.append(create_step(k, item, datafile))
            elif isinstance(item, ForLoop):
                k.steps.append(create_step(k, item, datafile))
            else:
                name = item.name[1:-1].lower()
                setting = {
                    'arguments': k.args,
                    'return': k.return_,
                    'timeout': k.timeout,
                    'documentation': k.doc,
                    'teardown': k.teardown,
                    'tags': k.tags
                }.get(name)
                setting.populate(item.value)


import ast
class V(ast.NodeVisitor):
    def __init__(self):
        self.depth = 0

    def generic_visit(self, node):
        print("\t" * self.depth + type(node).__name__)
        self.depth += 1
        ast.NodeVisitor.generic_visit(self, node)
        self.depth -= 1


class Builder(object):

    def read(self, source, populator):
        data = Utf8Reader(source).read()
        parser = yacc.yacc(module=RobotFrameworkParser())
        datafile = parser.parse(lexer=LexerWrapper(data))
        V().visit(datafile)
        print(ast.dump(datafile))
        for s in datafile.sections:
            if type(s).__name__ == 'SettingSection':
                populate_settings(populator, s)
            if type(s).__name__ == 'VariableSection':
                populate_variables(populator, s)
            if type(s).__name__ == 'TestCaseSection':
                populate_tests(populator, s)
            if type(s).__name__ == 'KeywordSection':
                populate_kws(populator, s)
        return datafile


class LexerWrapper(object):

    def __init__(self, data):
        lexer = RobotFrameworkLexer(data_only=True)
        lexer.input(data)
        self.tokens = lexer.get_tokens()

    def token(self):
        token = next(self.tokens, None)
        while token and token.type == 'EOS':
            token = next(self.tokens, None)
        return token
