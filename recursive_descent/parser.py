import re
from collections import namedtuple

token_specification = [
    ('INTEGER',  r'\d+'),
    ('ASSIGN',   r'='),
    ('VARIABLE', r'[xy]'),
    ('LPAREN',   r'\('),   # parathesis need escape
    ('RPAREN',   r'\)'),
    ('DIVIDE',   r'/'),
    ('TIME',     r'\*'),
    ('MINUS',    r'-'),
    ('PLUS',     r'\+')]

token_regex = '|'.join(['(?P<%s>%s)' % ts for ts in token_specification])

for m in re.finditer(token_regex, "12 + 3*(x + 3y) = 4"):
    kind = m.lastgroup
    print repr(m.group(kind))
