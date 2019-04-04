from ast import AST

class Node(AST):
    _fields = ()


class DataFile(Node):
    _fields = ('sections',)

    def __init__(self, sections):
        self.sections = sections


class SettingSection(Node):
    _fields = ('settings',)

    def __init__(self, settings):
        self.settings = settings


class VariableSection(Node):
    _fields = ('variables',)

    def __init__(self, variables):
        self.variables = variables


class TestCaseSection(Node):
    _fields = ('tests',)

    def __init__(self, tests):
        self.tests = tests


class KeywordSection(Node):
    _fields = ('keywords',)

    def __init__(self, keywords):
        self.keywords = keywords


class Variable(Node):
    _fields = ('name', 'value')

    def __init__(self, name, value):
        self.name = name
        self.value = value


class KeywordCall(Node):
    _fields = ('assign', 'keyword', 'args')

    def __init__(self, assign, keyword, args):
        self.assign = assign
        self.keyword = keyword
        self.args = args


class ForLoop(Node):
    _fields = ('flavor', 'variables', 'values', 'keyword_calls')

    def __init__(self, flavor, variables, values, keyword_calls):
        self.flavor = flavor
        self.variables = variables
        self.values = values
        self.keyword_calls = keyword_calls


class TestCase(Node):
    _fields = ('name', 'body')

    def __init__(self, name, body):
        self.name = name
        self.body = body


class Keyword(Node):
    _fields = ('name', 'body')

    def __init__(self, name, body):
        self.name = name
        self.body = body


class TemplateArguments(Node):
    _fields = ('args',)

    def __init__(self, args):
        self.args = args


class Setting(Node):
    _fields = ('value',)

    def __init__(self, value):
        self.value = value


class ImportSetting(Node):
    _fields = ('name', 'args')

    def __init__(self, name, args):
        self.name = name
        self.args = args


class MetadataSetting(Node):
    _fields = ('name', 'value')

    def __init__(self, name, value):
        self.name = name
        self.value = value


class DocumentationSetting(Setting): pass
class SuiteSetupSetting(Setting): pass
class SuiteTeardownSetting(Setting): pass
class TestSetupSetting(Setting): pass
class TestTeardownSetting(Setting): pass
class TestTemplateSetting(Setting): pass
class TestTimeoutSetting(Setting): pass
class ForceTagsSetting(Setting): pass
class DefaultTagsSetting(Setting): pass
class LibrarySetting(ImportSetting): pass
class ResourceSetting(ImportSetting): pass
class VariablesSetting(ImportSetting): pass
class SetupSetting(Setting): pass
class TeardownSetting(Setting): pass
class TemplateSetting(Setting): pass
class TimeoutSetting(Setting): pass
class TagsSetting(Setting): pass
class ArgumentsSetting(Setting): pass
class ReturnSetting(Setting): pass
