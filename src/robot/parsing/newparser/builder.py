import os

from robot.parsing.vendor import yacc

from robot.output import LOGGER
from robot.utils import Utf8Reader
from robot.parsing.lexer import RobotFrameworkLexer

from .parser import RobotFrameworkParser


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
    for name, values in section:
        key = name.lower()
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
                report_invalid_syntax(populator._datafile, "Non-existing setting '{}'.".format(name))


def populate_variables(populator, section):
    datafile = populator._datafile
    datafile.variable_table.set_header('Variables')
    for name, values in section:
        datafile.variable_table.add(name, populator._replace_curdirs_in(values))


def create_step(parent, step, datafile):
    from robot.parsing.model import ForLoop
    assign, name, args = step[:3]
    if name == 'FOR':
        s = ForLoop(parent, replace_curdirs_in(datafile, args))
        for forstep in step[3]:
            fs = Step(forstep[0] or [], forstep[1], replace_curdirs_in(datafile, forstep[2]))
            s.steps.append(fs)
    else:
        s = Step(assign or [], name, replace_curdirs_in(datafile, args))
    return s


def populate_tests(populator, section):
    datafile = populator._datafile
    datafile.testcase_table.set_header('Test cases')
    for name, settings, stepdata in section:
        t = datafile.testcase_table.add(name)
        for step in stepdata:
            t.steps.append(create_step(t, step, datafile))
        for name, value in settings:
            name = name[1:-1].lower()
            setting = {
                'timeout': t.timeout,
                'documentation': t.doc,
                'setup': t.setup,
                'teardown': t.teardown,
                'template': t.template,
                'tags': t.tags
            }.get(name.lower())
            if setting is not None:
                setting.populate(value)


def populate_kws(populator, section):
    datafile = populator._datafile
    datafile.keyword_table.set_header('Keywords')
    for name, settings, stepdata in section:
        k = datafile.keyword_table.add(name)
        for step in stepdata:
            k.steps.append(create_step(k, step, datafile))
        for name, value in settings:
            name = name[1:-1].lower()
            setting = {
                'arguments': k.args,
                'return': k.return_,
                'timeout': k.timeout,
                'documentation': k.doc,
                'teardown': k.teardown,
                'tags': k.tags
            }.get(name.lower())
            if setting is not None:
                setting.populate(value)


class Builder(object):

    def read(self, source, populator):
        data = Utf8Reader(source).read()
        parser = yacc.yacc(module=RobotFrameworkParser())
        sections = parser.parse(lexer=LexerWrapper(data))
        for s in sections:
            if s[0] == 'settings':
                populate_settings(populator, s[1])
            if s[0] == 'variables':
                populate_variables(populator, s[1])
            if s[0] == 'testcases':
                populate_tests(populator, s[1])
            if s[0] == 'keywords':
                populate_kws(populator, s[1])


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
