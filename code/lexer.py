from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


TOKEN_SPECIFICATION = [
    ('NUMBER',      r'-?\d+(\.\d*)?'),
    ('FUNC',        r'math.sin|math.cos|math.tan|math.sqrt|abs'),
    ('LOG',         r'print'),
    ('OPERATOR',    r'[+\-*/]|==|!=|<=|>=|<|>|and|or|not'),
    ('BLOCK',       r'if|else|while'),
    ('BOOL',        r'True|False'),
    ('STRING',      r'\"[^"\']*\"|\'[^"\']*\''),
    ('VARIABLE',    r'[A-Za-z0-9_]+'),
    ('ASSIGN',      r'='),
    ('COLON',       r':'),
    ('NEWLINE',     r'\n'),
    ('TAB',         r'    '),
    ('SKIP',        r'[ \r]+'),
    ('LPAR',        r'\('),
    ('RPAR',        r'\)'),
    ('MISMATCH',    r'.'),
]


def tokenize(code: str):
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code + '\n'):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            value = '\n'
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'unexpected {value!r} on line {line_num}')
        yield Token(kind, value.replace('\'', '\"'), line_num, column)
