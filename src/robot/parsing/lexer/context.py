from .settings import KeywordSettings, TestCaseFileSettings, TestCaseSettings


class LexingContext(object):

    def __init__(self, settings=None):
        self.settings = settings

    def validate_setting(self, name):
        self.settings.validate(name)

    def test_case_context(self):
        return TestCaseContext(TestCaseSettings(self.settings))

    def keyword_context(self):
        return KeywordContext(KeywordSettings())


class TestCaseFileContext(LexingContext):

    def __init__(self, settings=None):
        LexingContext.__init__(self, settings or TestCaseFileSettings())


class TestCaseContext(LexingContext):

    @property
    def template_set(self):
        return self.settings.template_set


class KeywordContext(LexingContext):
    settings_class = KeywordSettings

    @property
    def template_set(self):
        return False
