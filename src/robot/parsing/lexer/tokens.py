#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


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
