# Expr AST and small recursive-descent parser for conditions
import re

class Expr:
    pass

class VariableExpr(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class LiteralExpr(Expr):
    def __init__(self, value, type_):
        self.value = value
        self.type = type_

    def __str__(self):
        return repr(self.value)

class EqualExpr(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} == {self.right})"

class AndExpr(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} and {self.right})"

class OrExpr(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} or {self.right})"

class NotExpr(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"(not {self.expr})"

# Tokenizer
_TOKEN_RE = re.compile(r"\s*(=>|==|and\b|or\b|not\b|\(|\)|\d+|true\b|false\b|\"(\\\"|[^\"])*\"|[a-zA-Z_][a-zA-Z0-9_]*)", re.IGNORECASE)

class ParseError(Exception):
    pass

class _Tokenizer:
    def __init__(self, text):
        self.tokens = [m.group(1) for m in _TOKEN_RE.finditer(text)]
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def next(self):
        t = self.peek()
        self.pos += 1
        return t

# Grammar:
# expr  : or_expr
# or_expr : and_expr ( 'or' and_expr )*
# and_expr: not_expr ( 'and' not_expr )*
# not_expr: 'not' not_expr | comparison
# comparison: primary ( '==' primary )?
# primary: ID | NUMBER | STRING | TRUE | FALSE | '(' expr ')'


def parse_condition(text):
    tok = _Tokenizer(text)
    expr = _parse_or(tok)
    if tok.peek() is not None:
        raise ParseError(f"Unexpected token {tok.peek()}")
    return expr


def _parse_or(tok):
    left = _parse_and(tok)
    while True:
        if tok.peek() and tok.peek().lower() == 'or':
            tok.next()
            right = _parse_and(tok)
            left = OrExpr(left, right)
        else:
            break
    return left


def _parse_and(tok):
    left = _parse_not(tok)
    while True:
        if tok.peek() and tok.peek().lower() == 'and':
            tok.next()
            right = _parse_not(tok)
            left = AndExpr(left, right)
        else:
            break
    return left


def _parse_not(tok):
    if tok.peek() and tok.peek().lower() == 'not':
        tok.next()
        expr = _parse_not(tok)
        return NotExpr(expr)
    return _parse_comparison(tok)


def _parse_comparison(tok):
    left = _parse_primary(tok)
    if tok.peek() == '==':
        tok.next()
        right = _parse_primary(tok)
        return EqualExpr(left, right)
    return left


def _parse_primary(tok):
    t = tok.peek()
    if t is None:
        raise ParseError('Unexpected end of input')
    if t == '(':
        tok.next()
        e = _parse_or(tok)
        if tok.next() != ')':
            raise ParseError('Expected )')
        return e
    # string literal
    if t.startswith('"'):
        tok.next()
        # remove surrounding quotes and unescape
        val = t[1:-1].replace('\"', '"')
        return LiteralExpr(val, 'string')
    # booleans
    if t.lower() == 'true' or t.lower() == 'false':
        tok.next()
        return LiteralExpr(t.lower() == 'true', 'bool')
    # number
    if t.isdigit():
        tok.next()
        return LiteralExpr(int(t), 'int')
    # identifier
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', t):
        tok.next()
        return VariableExpr(t)
    raise ParseError(f'Unexpected token: {t}')

# Helpers for semantic analysis

def collect_vars(expr, out=None):
    if out is None:
        out = set()
    if isinstance(expr, VariableExpr):
        out.add(expr.name)
    elif isinstance(expr, LiteralExpr):
        pass
    elif isinstance(expr, EqualExpr):
        collect_vars(expr.left, out)
        collect_vars(expr.right, out)
    elif isinstance(expr, (AndExpr, OrExpr)):
        collect_vars(expr.left, out)
        collect_vars(expr.right, out)
    elif isinstance(expr, NotExpr):
        collect_vars(expr.expr, out)
    return out

def infer_type(expr, symbol_table):
    # returns 'bool' or type string for literals/vars
    if isinstance(expr, LiteralExpr):
        return expr.type
    if isinstance(expr, VariableExpr):
        return symbol_table.get(expr.name)
    if isinstance(expr, EqualExpr):
        lt = infer_type(expr.left, symbol_table)
        rt = infer_type(expr.right, symbol_table)
        if lt is None or rt is None:
            return None
        if lt != rt:
            return 'type-error'
        return 'bool'
    if isinstance(expr, (AndExpr, OrExpr, NotExpr)):
        # boolean operators always produce bool
        return 'bool'
    return None
