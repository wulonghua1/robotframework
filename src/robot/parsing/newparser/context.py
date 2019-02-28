class ParsingContext(object):

    def __init__(self):
        self.setting_seen = False
        self.kw_seen = False
        self.in_for_loop_declaration = False


class TestCaseParsingContext(ParsingContext):
    pass


class KeywordParsingContext(ParsingContext):
    pass
