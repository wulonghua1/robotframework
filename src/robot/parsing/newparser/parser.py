import os

from robot.output import LOGGER
from robot.utils import Utf8Reader

from .section_parser import section_parser
from .tableparsers import parse_variabletable, parse_settingtable, parse_tcuktable
from .context import TestCaseParsingContext, KeywordParsingContext


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
    for name, values in parse_settingtable(section):
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
    for name, values in parse_variabletable(section):
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
    for name, settings, stepdata in parse_tcuktable(section, TestCaseParsingContext()):
        t = datafile.testcase_table.add(name)
        for step in stepdata:
            t.steps.append(create_step(t, step, datafile))
        for name, value in settings:
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
    for name, settings, stepdata in parse_tcuktable(section, KeywordParsingContext()):
        k = datafile.keyword_table.add(name)
        for step in stepdata:
            k.steps.append(create_step(k, step, datafile))
        for name, value in settings:
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


class NewParser(object):

    def read(self, source, populator):
        data = Utf8Reader(source).read()
        sections = section_parser(data)
        if 'SETTING' in sections:
            populate_settings(populator, sections['SETTING'])
        if 'VARIABLE' in sections:
            populate_variables(populator, sections['VARIABLE'])
        if 'TESTCASE' in sections:
            populate_tests(populator, sections['TESTCASE'])
        if 'KEYWORD' in sections:
            populate_kws(populator, sections['KEYWORD'])
