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

token_precedence_specification = [
    # interger, variable and equal sign should be 0
    ('+', 10),
    ('-', 10),
    ('*', 20),
    ('/', 20),
    ('(', 30),
    (')', 0)
]

token_precedence = {t: p for t, p in token_precedence_specification}

class Token(object):
    __slots__ = 'val', 'lbp', 'first', 'second'

    calc_maps = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
    }
    
    def __init__(self, val, precedence=0):
        self.val = val
        self.lbp = precedence # left binding power
        self.first = None
        self.second = None

    def led(self, left): 
        self.first = left
        self.second = expression(self.lbp)
        return Token.calc_maps[self.val](self.first, self.second)

    def nud(self):
        if self.val == '(':
            expr = expression()
            advance(')')
            return expr
        return self.val

    def __repr__(self):
        return (('(' + repr(self.first) if self.first else '')
            + ' ' + str(self.val) + ' '
            + (repr(self.second) + ')' if self.second else ''))


def advance(ending_token):
    global token, token_stream
    if ending_token != token.val:
        raise SyntaxError('Expecting %r' % token)
    token = next(token_stream)

def tokenize(program):
    for m in re.finditer(token_regex, program):
        kind = m.lastgroup
        val = m.group(kind)
        if kind == 'INTEGER':
            yield Token(int(val))
        elif kind in ['VARIABLE', 'EQUAL']:
            yield Token(val)
        else:
            yield Token(val, token_precedence[val])
    yield Token('', 0) # designate the ending token

def expression(rbp=0):
    global token, token_stream
    t = token
    token = next(token_stream)
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next(token_stream)
        left = t.led(left)
    return left

def parse(program):
    global token, token_stream
    token_stream = tokenize(program)
    token = next(token_stream)
    import pdb; pdb.set_trace()
    return expression() 

print parse('12 - 3*(2 + 1) -4 + 2*5')
