import ast

from robot.errors import DataError
from robot.parsing.newparser.builder import Builder
from robot.running.model import TestSuite, Keyword, ForLoop
from robot.utils import abspath
from robot.variables import VariableIterator


def create_fixture(data, type):
    return Keyword(name=data[0], args=tuple(data[1:]), type=type)


class SettingsBuilder(ast.NodeVisitor):
    def __init__(self, suite, test_defaults):
        self.suite = suite
        self.test_defaults = test_defaults

    def visit_DocumentationSetting(self, node):
        self.suite.doc = "\n".join(node.value)

    def visit_SuiteSetupSetting(self, node):
        self.suite.keywords.append(create_fixture(node.value, 'setup'))

    def visit_SuiteTeardownSetting(self, node):
        self.suite.keywords.append(create_fixture(node.value, 'teardown'))

    def visit_TestSetupSetting(self, node):
        self.test_defaults.setup = node.value

    def visit_TestTeardownSetting(self, node):
        self.test_defaults.teardown = node.value

    def visit_TestTimeoutSetting(self, node):
        self.test_defaults.timeout = node.value

    def visit_DefaultTagsSetting(self, node):
        self.test_defaults.default_tags = node.value

    def visit_ForecTagsSetting(self, node):
        self.test_defaults.force_tags = node.value

    def visit_TestTemplateSetting(self, node):
        self.test_defaults.test_template = node.value

    def visit_VariableSection(self, node):
        pass

    def visit_TestCaseSection(self, node):
        pass

    def visit_KeywordSection(self, node):
        pass


class SuiteBuilder(ast.NodeVisitor):
    def __init__(self, suite, test_defaults):
        self.suite = suite
        self.test_defaults = test_defaults

    def visit_TestCase(self, node):
        TestCaseBuilder(self.suite, self.test_defaults).visit(node)

    def visit_Keyword(self, node):
        KeywordBuilder(self.suite.resource).visit(node)

    def visit_Variable(self, node):
        self.suite.resource.variables.create(name=node.name, value=node.value)


class TestCaseBuilder(ast.NodeVisitor):

    def __init__(self, suite, defaults):
        self.suite = suite
        self.settings = TestSettings(defaults)
        self.test = None

    def visit_TestCase(self, node):
        self.test = self.suite.tests.create(name=node.name)
        self.generic_visit(node)
        self.settings.set_test_values(self.test)
        template = self.settings.get_template()
        if template:
            TemplateBuilder(self.test, template[0]).visit(node)

    def visit_ForLoop(self, node):
        for_loop = ForLoop(node.variables, node.values, node.flavor)
        ForLoopBuilder(for_loop).visit(node)
        self.test.keywords.append(for_loop)

    def visit_DocumentationSetting(self, node):
        self.test.doc = "\n".join(node.value)

    def visit_SetupSetting(self, node):
        self.settings.setup = node.value

    def visit_TeardownSetting(self, node):
        self.settings.teardown = node.value

    def visit_TimeoutSetting(self, node):
        self.settings.timeout = node.value

    def visit_TagsSetting(self, node):
        self.settings.tags = node.value

    def visit_TemplateSetting(self, node):
        self.settings.template = node.value

    def visit_KeywordCall(self, node):
        self.test.keywords.create(name=node.keyword, args=node.args, assign=node.assign or [])


class KeywordBuilder(ast.NodeVisitor):
    def __init__(self, resource):
        self.resource = resource
        self.kw = None

    def visit_Keyword(self, node):
        self.kw = self.resource.keywords.create(name=node.name)
        self.generic_visit(node)

    def visit_ArgumentsSetting(self, node):
        self.kw.args = node.value

    def visit_TagsSetting(self, node):
        self.kw.tags = node.value

    def visit_KeywordCall(self, node):
        self.kw.keywords.create(name=node.keyword, args=node.args, assign=node.assign or [])


class ForLoopBuilder(ast.NodeVisitor):
    def __init__(self, for_loop):
        self.for_loop = for_loop

    def visit_KeywordCall(self, node):
        self.for_loop.keywords.create(name=node.keyword, args=node.args, assign=node.assign or [])


class TemplateBuilder(ast.NodeVisitor):

    def __init__(self, test, template):
        self.test = test
        self.template = template

    def visit_TemplateArguments(self, node):
        template, args = self._format_template(self.template, node.args)
        self.test.keywords.append(Keyword(name=template, args=args))

    def _format_template(self, template, args):
        iterator = VariableIterator(template, identifiers='$')
        variables = len(iterator)
        if not variables or variables != len(args):
            return template, tuple(args)
        temp = []
        for before, variable, after in iterator:
            temp.extend([before, args.pop(0)])
        temp.append(after)
        return ''.join(temp), ()


class TestDefaults(object):
    def __init__(self):
        self.setup = None
        self.teardown = None
        self.timeout = None
        self.force_tags = None
        self.default_tags = None
        self.test_template = None


class TestSettings(object):
    def __init__(self, defaults):
        self.defaults = defaults
        self.setup = None
        self.teardown = None
        self.timeout = None
        self.template = None
        self.tags = None

    def get_template(self):
        return self.template or self.defaults.test_template

    def set_test_values(self, test):
        self.set_setup(test)
        self.set_teardown(test)
        self.set_timout(test)
        self.set_tags(test)

    def set_setup(self, test):
        setup = self.setup or self.defaults.setup
        if setup:
             test.keywords.setup = create_fixture(setup, type='setup')

    def set_teardown(self, test):
        teardown = self.teardown or self.defaults.teardown
        if teardown:
            test.keywords.teardown = create_fixture(teardown, type='teardown')

    def set_timout(self, test):
        timeout = self.timeout or self.defaults.timeout
        if timeout:
            test.timout = timeout

    def set_tags(self, test):
        default_tags = (self.tags or self.defaults.default_tags) or []
        test.tags = default_tags + (self.defaults.force_tags or [])


class TestSuiteBuilder(object):

    def __init__(self, include_suites=None, warn_on_skipped='DEPRECATED',
                 extension=None, rpa=None):
        self.rpa = rpa

    def build(self, *paths):
        """
        :param paths: Paths to test data files or directories.
        :return: :class:`~robot.running.model.TestSuite` instance.
        """
        if not paths:
            raise DataError('One or more source paths required.')
        if len(paths) == 1:
            return self._parse_and_build(paths[0])
        root = TestSuite()
        for path in paths:
            root.suites.append(self._parse_and_build(path))
        root.rpa = self.rpa
        return root

    def _parse_and_build(self, path):
        suite = self._build_suite(self._parse(path))
        suite.remove_empty_suites()
        return suite

    def _build_suite(self, data, parent_defaults=None):
        suite = TestSuite()
        defaults = TestDefaults()
        SettingsBuilder(suite, defaults).visit(data)
        SuiteBuilder(suite, defaults).visit(data)
        return suite

    def _parse(self, path):
        try:
            return Builder().read(abspath(path), None)
        except DataError as err:
            raise DataError("Parsing '%s' failed: %s" % (path, err.message))
