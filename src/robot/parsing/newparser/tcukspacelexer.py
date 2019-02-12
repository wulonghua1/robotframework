import re

TOKENS = (
    'COMMENT',
    'NAME',
    'SEPARATOR',
    'KEYWORD',
    'ARGUMENT',
    'FOR',
    'CONTINUATION',
    'ASSIGNMENT',
    'SETTING',
    'SETTING_VALUE',
    'INDENT',
    'END',
    'FORINDENT',
)


class SpaceLexer(object):
    tokens = TOKENS

    def __init__(self, ctx):
        self.ctx = ctx

    def t_error(self, t):
        print(t)
        print("SpaceLexer illegal character '%s'" % t.value)
        t.lexer.skip(1)

    t_ignore = '\r?\n'

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_END(self, t):
        r'^\s\s+END\s*$'
        return t

    def t_CONTINUATION(self, t):
        r'(?m)^\ {2,}\.\.\.'
        pass

    def t_SETTING(self, t):
        r'(?i)\[.*\]'
        self.ctx.setting_seen = True
        t.value = t.value[1:-1].lower()
        return t

    def t_FORINDENT(self, t):
        r'(?m)^\s+\\'
        self.ctx.in_for_loop_declaration = False
        self.ctx.kw_seen = False
        return t

    def t_INDENT(self, t):
        r'^\s\s+'
        self.ctx.kw_seen = False
        self.ctx.in_for_loop_declaration = False
        self.ctx.setting_seen = False
        return t

    def t_SEPARATOR(self, t):
        r'\s\s+'
        return t

    def t_NAME(self, t):
        r'^(\S+\ )*\S+'
        self.ctx.kw_seen = False
        self.ctx.setting_seen = False
        return t

    def t_first_value(self, t):
        r'(^\ {2,})(?!\.\.\.)'
        self.ctx.kw_seen = False
        self.ctx.setting_seen = False
        self.ctx.in_for_loop_declaration = False

    def t_value(self, t):
        r'(\S+\ )*\S+'
        if self.ctx.setting_seen:
            t.type = 'SETTING_VALUE'
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
