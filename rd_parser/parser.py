import re
from collections import namedtuple

token_patterns = {
    'NUM' : r'\d+',
    'PLUS' : r'\+',
    'MINUS' : r'-',
    'TIME' : r'\*',
    'DIVIDE': r'/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'WS' : r'\s+'
}

token_pattern_all = '|'.join([r'(?P<{}>{})'.format(t, p) for t, p in token_patterns.iteritems()])

token_regex = re.compile(token_pattern_all)
Token = namedtuple('Token', 'type, val')

def tokenizer(expr):
    for m in re.finditer(token_regex, expr):
        token = Token(m.lastgroup, m.group())
        if token.type != 'WS':
            yield token

class Parser(object):
    
    def __init__(self, expr):
        self.token_stream = tokenizer(expr)
        self.cur_token = None
        self.next_token = None

    def _advance(self):
        self.cur_token, self.next_token = self.next_token, next(self.token_stream, None)

    def parse(self):
        self._advance()
        return self._parse_expr()

    def _accept(self, token_type):
        if self.next_token and self.next_token.type == token_type:
            self._advance()
            return True
        else:
            return False

    def _parse_expr(self):
        term = self._parse_term() 

        while self._accept('PLUS') or self._accept('MINUS'):
            if self.cur_token.type == 'PLUS':
                return term + self._parse_expr()
            elif self.cur_token.type == 'MINUS':
                return term - self._parse_expr()
        
        return term
                
    def _parse_term(self):
        factor = self._parse_factor()
        while self._accept('TIME') or self._accept('DIVIDE'):
            if self.cur_token.type == 'TIME':
                return factor * self._parse_factor()
            elif self.cur_token.type == 'DIVIDE':
                return factor / self._parse_factor()

        return factor

    def _parse_factor(self):
        if self._accept('LPAREN'):
            expr = self._parse_expr()
            if not self._accept('RPAREN'):
                raise SyntaxError
            return expr
        elif self._accept('NUM'):
            return int(self.cur_token.val)
        elif self._accept('PLUS') or self._accept('MINUS'):
            sign = -1 if self.cur_token.type == 'MINUS' else 1
            while self._accept('PLUS') or self._accept('MINUS'):
                sign *= -1 if self.cur_token.type == 'MINUS' else 1 
            return sign * self._parse_expr()
        
        raise SyntaxError


parser = Parser('-(1 + 2) * -3')
print parser.parse()

