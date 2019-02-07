from robot.parsing.vendor import lex, yacc

from .tcukspacelexer import SpaceLexer
from .tcukpipelexer import PipeLexer
from .tcukparser import TCUKParser


class TestCaseParser(object):

    def __init__(self, lexer):
        self.parser = yacc.yacc(module=TCUKParser())
        self.lexer = lexer

    def parse(self, data):
        self.lexer.lex(data)
        return self.parser.parse(lexer=self.lexer)


class TestCaseLexer(object):

    def __init__(self, ctx):
        self.space_lexer = lex.lex(module=SpaceLexer(ctx))
        self.pipe_lexer = lex.lex(module=PipeLexer(ctx))
        self.tokens = []
        self._in_for_loop = False
        self._end_needed = False
        self._next_must_be_end = False

    def lex(self, data):
        for line in data.splitlines():
            lexer = self.space_lexer if line[:2] != '| ' else self.pipe_lexer
            lexer.input(line)
            self.tokens.extend(list(lexer))

    def token(self):
        if not self.tokens:
            return None
        t = self.tokens.pop(0)
        if t.type == 'FOR':
            self._in_for_loop = True
        elif self._in_for_loop and t.type == 'FORINDENT':
            self._end_needed = True
        elif self._end_needed and t.type == 'INDENT':
            self._next_must_be_end = True
        elif self._next_must_be_end or (self._end_needed and t.type == 'NAME'):
            self._in_for_loop = self._end_needed = self._next_must_be_end = False
            if t.type != 'END':
                self.tokens.insert(0, t)
                t = T('END')
        if t.type in ['INDENT', 'SEPARATOR', 'FORINDENT']:
            return self.token()
        return t

class T(object):
    def __init__(self, type_):
        self.type = type_

def tcuktable_parser(data, ctx):
    return TestCaseParser(TestCaseLexer(ctx)).parse(data)
