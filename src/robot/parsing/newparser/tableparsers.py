from robot.parsing.vendor import lex, yacc

from . import settinglexer
from . import settingparser
from . import variablelexer
from . import variableparser
from .tcukspacelexer import SpaceLexer
from .tcukparser import TCUKParser


class SimpleTableParser(object):

    def __init__(self, lexer, parser_module):
        self.parser = yacc.yacc(module=parser_module)
        self.lexer = lexer

    def parse(self, data):
        self.lexer.lex(data)
        return self.parser.parse(lexer=self.lexer)


class SimpleTableLexer(object):

    def __init__(self, lexer_module):
        self.lexer = lex.lex(module=lexer_module)
        self.tokens = []

    def lex(self, data):
        for line in data.splitlines():
            self.lexer.input(line)
            self.tokens.extend(list(self.lexer))

    def token(self):
        return self.tokens.pop(0) if self.tokens else None


def parse_settingtable(data):
    return SimpleTableParser(
        SimpleTableLexer(settinglexer), settingparser).parse(data)


def parse_variabletable(data):
    return SimpleTableParser(
        SimpleTableLexer(variablelexer), variableparser).parse(data)


class TestCaseParser(object):

    def __init__(self, lexer):
        self.parser = yacc.yacc(module=TCUKParser())
        self.lexer = lexer

    def parse(self, data):
        self.lexer.lex(data)
        return self.parser.parse(lexer=self.lexer)


class TestCaseLexer(object):

    def __init__(self, ctx):
        self.lexer = lex.lex(module=SpaceLexer(ctx))
        self.tokens = []
        self._in_for_loop = False
        self._end_needed = False
        self._next_must_be_end = False

    def lex(self, data):
        for line in data.splitlines():
            self.lexer.input(line)
            self.tokens.extend(list(self.lexer))

    def _reset_for_loop_state(self):
        self._in_for_loop = self._end_needed = self._next_must_be_end = False

    def token(self):
        if not self.tokens:
            if self._end_needed:
                self._reset_for_loop_state()
                return T('END')
            return None
        t = self.tokens.pop(0)
        if t.type == 'FOR':
            self._in_for_loop = True
        elif self._in_for_loop and t.type == 'FORINDENT':
            self._end_needed = True
        elif self._end_needed and t.type == 'INDENT':
            self._next_must_be_end = True
        elif self._next_must_be_end or (self._end_needed and t.type == 'NAME'):
            self._reset_for_loop_state()
            if t.type != 'END':
                self.tokens.insert(0, t)
                t = T('END')
        if t.type in ['INDENT', 'SEPARATOR', 'FORINDENT']:
            return self.token()
        return t


class T(object):
    def __init__(self, t):
        self.type = t


def parse_tcuktable(data, ctx):
    return TestCaseParser(TestCaseLexer(ctx)).parse(data)
