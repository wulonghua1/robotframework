import re

from .tcukspacelexer import TOKENS


class PipeLexer(object):
    tokens = TOKENS

    def __init__(self, ctx):
        self.ctx = ctx

    def t_error(self, t):
        print(t)
        print("PipeLexer Illegal character '%s'" % t.value)
        t.lexer.skip(1)

    t_ignore = '\r?\n'

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_CONTINUATION(self, t):
        r'(?m)^\|\s+\|\s+\.\.\.'
        pass

    def t_SETTING(self, t):
        r'(?i)\[.*\]'
        self.ctx.setting_seen = True
        t.value = t.value[1:-1].lower()
        return t

    def t_INDENT(self, t):
        r'(?m)^(\|\s+)+'
        self.ctx.name_allowed = t.value.count('|') == 1
        self.ctx.in_for_loop_declaration = False
        self.ctx.kw_seen = False
        return t

    def t_SEPARATOR(self, t):
        r'(\s+\|(\s+|\s*$)|\s+$)'
        return t

    def t_first_value(self, t):
        r'(^\|\s+\|\s+)(?!\.\.\.)'
        self.ctx.kw_seen = False
        self.ctx.setting_seen = False
        self.ctx.in_for_loop_declaration = False

    def t_value(self, t):
        r'(?m).+?(?=(\s+\|\s+|\s+\|?\s*$))'
        if self.ctx.setting_seen:
            t.type = 'SETTING_VALUE'
        elif self.ctx.name_allowed:
            t.type = 'NAME'
        elif self.ctx.kw_seen or self.ctx.in_for_loop_declaration:
            t.type = 'ARGUMENT'
        elif re.match(r'[$@&]\{.+\}( ?=)?', t.value):
            t.type = 'ASSIGNMENT'
        elif t.value.upper() == ': FOR' or t.value == 'FOR':
            t.type = 'FOR'
            self.ctx.in_for_loop_declaration = True
        else:
            t.type = 'KEYWORD'
            self.ctx.kw_seen = True
        return t
