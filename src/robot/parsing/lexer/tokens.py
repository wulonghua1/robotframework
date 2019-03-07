class Token(object):
    ERROR = 'ERROR'
    SETTING = 'SETTING'
    ARGUMENT = 'ARGUMENT'
    KEYWORD = 'KEYWORD'
    VARIABLE = 'VARIABLE'
    COMMENT = 'COMMENT'
    HEADER = 'HEADER'
    IGNORE = 'IGNORE'
    SEPARATOR = 'SEPARATOR'
    NAME = 'NAME'
    ASSIGN = 'ASSIGN'
    CONTINUATION = 'CONTINUATION'
    FOR = 'FOR'
    FOR_SEPARATOR = 'FOR_SEPARATOR'
    OLD_FOR_INDENT = 'OLD_FOR_INDENT'
    END = 'END'
    DATA = 'DATA'
    EOS = 'EOS'
    NON_DATA_TOKENS = {SEPARATOR, COMMENT, CONTINUATION, IGNORE}

    __slots__ = ['type', 'value', 'lineno', 'columnno']

    def __init__(self, type, value='', lineno=-1, columnno=-1):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.columnno = columnno

    def __str__(self):
        # TODO: __unicode__
        return self.value

    def __repr__(self):
        return 'Token(%s, %r, %s, %s)' % (self.type, self.value,
                                          self.lineno, self.columnno)
