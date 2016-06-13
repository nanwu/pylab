import re
import copy
from collections import namedtuple

token_patterns = {
    'NUM' : r'\d+',
    'PLUS' : r'\+',
    'MINUS' : r'-',
    'TIME' : r'\*',
    'DIVIDE': r'/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'WS' : r'\s+',
    'VAR': r'\d*[XY]'
}

token_pattern_all = '|'.join([r'(?P<{}>{})'.format(t, p) for t, p in token_patterns.iteritems()])

token_regex = re.compile(token_pattern_all)
Token = namedtuple('Token', 'type, val')

class Var(object):

    def __init__(self, var_to_factor={}, constant=0):
        self.var_to_factor = var_to_factor
        self.constant = constant

    def _add_delegate(self, to_add, new_var):
        if isinstance(to_add, int):
            new_var.constant += to_add
        elif isinstance(to_add, Var):
            for var_to_add, factor_to_add in to_add.var_to_factor.iteritems():
                new_var.var_to_factor[var_to_add] = factor_to_add + \
                                                    new_var.var_to_factor.get(var_to_add, 0)

            new_var.constant += to_add.constant
        else:
            raise TypeError('can not add to the Var object.')

        return new_var

    def __add__(self, to_add):
        return self._add_delegate(to_add, copy.deepcopy(self))

    def __iadd__(self, to_add):
        return self._add_delegate(to_add, self)

    def __radd__(self, to_add):
        return self._add_delegate(to_add, copy.deepcopy(self))

    def __neg__(self):
        new_var= copy.deepcopy(self)
        for var in new_var.var_to_factor.keys():
            new_var.var_to_factor[var] = -new_var.var_to_factor[var]
        new_var.constant = -new_var.constant
        return new_var
           
    def _sub_delegate(self, to_sub, new_var):
        if isinstance(to_sub, int):
            new_var.constant -= to_sub
        elif isinstance(to_sub, Var):
            for var_to_sub, factor_to_sub in to_sub.var_to_factor.iteritems():
                new_var.var_to_factor[var_to_sub] = new_var.var_to_factor.get(var_to_sub, 0) - factor_to_sub
            new_var.constant -= to_sub.constant
        else:
            raise TypeError('can not substract from Var object.')

        return new_var

    def __rsub__(self, to_sub):
        return self._add_delegate(to_sub, -self) 

    def __isub__(self, to_sub):
        return self._add_delegate(-to_sub, self)

    def __sub__(self, to_sub):
        return self._add_delegate(-to_sub, copy.deepcopy(self))

    def __eq__(self, another_var):
        return self.constant == another_var.constant and self.var_to_factor == another_var.var_to_factor
    
    def __repr__(self):
        return repr(self.var_to_factor) + ', constant: ' + str(self.constant)

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


#parser = Parser('-(1 + 2) * -3')
#print parser.parse()

