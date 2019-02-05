from robot.utils import Utf8Reader
from .section_parser import section_parser
from .setting_parser import setting_parser
from .variable_parser import variable_parser
from .testcase_parser import testcase_parser
from .keyword_parser import keyword_parser

class Step(object):
    def __init__(self, assign, name, args):
        self.assign = assign
        self.name = name
        self.args = args

    def is_comment(self):
        return False

    def is_for_loop(self):
        return False


def populate_settings(populator, section):
    settings = populator._datafile.setting_table
    settings.set_header('Settings')
    for name, values in setting_parser(section):
        name = name.lower()
        if name == 'resource':
            settings.add_resource(values[0])
        elif name == 'library':
            settings.add_library(values[0], values[1:])
        elif name == 'variables':
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
            }.get(name)
            if setting is not None:
                setting.populate(values)


def populate_variables(populator, section):
    datafile = populator._datafile
    datafile.variable_table.set_header('Variables')
    for name, values in variable_parser(section):
        datafile.variable_table.add(name, populator._replace_curdirs_in(values))


def populate_tests(populator, section):
    from robot.parsing.model import ForLoop
    datafile = populator._datafile
    datafile.testcase_table.set_header('Test cases')
    for name, settings, stepdata in testcase_parser(section):
        t = datafile.testcase_table.add(name)
        for step in stepdata:
            assign, name, args = step[:3]
            if name == ': FOR':
                s = ForLoop(t, args)
                for forstep in step[3]:
                    fs = Step(forstep[0] or [], forstep[1], forstep[2])
                    s.steps.append(fs)
            else:
                s = Step(assign or [], name, args)
            t.steps.append(s)
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
    from robot.parsing.model import ForLoop
    datafile = populator._datafile
    datafile.keyword_table.set_header('Keywords')
    for name, settings, stepdata in keyword_parser(section):
        k = datafile.keyword_table.add(name)
        for step in stepdata:
            assign, name, args = step[:3]
            if name == ': FOR':
                s = ForLoop(k, args)
                for forstep in step[3]:
                    fs = Step(forstep[0] or [], forstep[1], forstep[2])
                    s.steps.append(fs)
            else:
                s = Step(assign or [], name, args)
            k.steps.append(s)
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
