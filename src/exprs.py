# exprs.py
# AST de expresiones de FlowLang.
#
# Las condiciones de guardia de las transiciones se representan como un arbol
# de expresiones tipado (no como texto). Cada nodo sabe:
#   - imprimirse           (__str__)          -> para diagnosticos legibles
#   - serializarse a JSON  (to_json)          -> backend de automatizacion
#   - recolectar variables (collect_vars)     -> analisis semantico
#   - inferir su tipo      (infer_type)       -> verificacion de tipos


class Expr:
    """Nodo base del AST de expresiones."""

    def to_json(self):
        raise NotImplementedError

    def __repr__(self):
        return f"<{type(self).__name__} {self}>"


class VariableExpr(Expr):
    """Referencia a una variable declarada con `var`."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def to_json(self):
        return {"op": "var", "name": self.name}


class LiteralExpr(Expr):
    """Literal: true/false, entero o cadena."""

    def __init__(self, value, type_):
        self.value = value
        self.type = type_  # 'bool' | 'int' | 'string'

    def __str__(self):
        if self.type == "bool":
            return "true" if self.value else "false"
        if self.type == "string":
            return f'"{self.value}"'
        return str(self.value)

    def to_json(self):
        return {"op": "lit", "type": self.type, "value": self.value}


class EqualExpr(Expr):
    """Comparacion de igualdad: `a == b`."""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} == {self.right})"

    def to_json(self):
        return {"op": "eq", "left": self.left.to_json(), "right": self.right.to_json()}


class AndExpr(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} and {self.right})"

    def to_json(self):
        return {"op": "and", "left": self.left.to_json(), "right": self.right.to_json()}


class OrExpr(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} or {self.right})"

    def to_json(self):
        return {"op": "or", "left": self.left.to_json(), "right": self.right.to_json()}


class NotExpr(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"(not {self.expr})"

    def to_json(self):
        return {"op": "not", "expr": self.expr.to_json()}


# ---------------------------------------------------------------------------
# Utilidades para el analisis semantico
# ---------------------------------------------------------------------------

def collect_vars(expr, out=None):
    """Devuelve el conjunto de nombres de variables referenciadas en `expr`."""
    if out is None:
        out = set()
    if isinstance(expr, VariableExpr):
        out.add(expr.name)
    elif isinstance(expr, EqualExpr):
        collect_vars(expr.left, out)
        collect_vars(expr.right, out)
    elif isinstance(expr, (AndExpr, OrExpr)):
        collect_vars(expr.left, out)
        collect_vars(expr.right, out)
    elif isinstance(expr, NotExpr):
        collect_vars(expr.expr, out)
    return out


def infer_type(expr, symbol_table, errors=None):
    """Infiere el tipo de `expr` con la tabla de simbolos dada.

    Devuelve 'bool' | 'int' | 'string' | None (tipo desconocido, p.ej. variable
    no declarada) | 'type-error'.

    Si se pasa una lista `errors`, se agregan mensajes detallados de cada
    incompatibilidad encontrada (util para reportar mas de un error por
    condicion).
    """

    def err(msg):
        if errors is not None:
            errors.append(msg)

    if isinstance(expr, LiteralExpr):
        return expr.type

    if isinstance(expr, VariableExpr):
        return symbol_table.get(expr.name)  # None si no esta declarada

    if isinstance(expr, EqualExpr):
        lt = infer_type(expr.left, symbol_table, errors)
        rt = infer_type(expr.right, symbol_table, errors)
        if lt is None or rt is None:
            return None
        if "type-error" in (lt, rt):
            return "type-error"
        if lt != rt:
            err(f"no se puede comparar '{expr.left}' ({lt}) con '{expr.right}' ({rt})")
            return "type-error"
        return "bool"

    if isinstance(expr, (AndExpr, OrExpr)):
        op = "and" if isinstance(expr, AndExpr) else "or"
        lt = infer_type(expr.left, symbol_table, errors)
        rt = infer_type(expr.right, symbol_table, errors)
        ok = True
        for side, t in ((expr.left, lt), (expr.right, rt)):
            if t not in ("bool", None, "type-error"):
                err(f"operando de '{op}' debe ser bool, pero '{side}' es {t}")
                ok = False
        if lt is None or rt is None:
            return None
        if not ok or "type-error" in (lt, rt):
            return "type-error"
        return "bool"

    if isinstance(expr, NotExpr):
        t = infer_type(expr.expr, symbol_table, errors)
        if t is None:
            return None
        if t == "type-error":
            return "type-error"
        if t != "bool":
            err(f"operando de 'not' debe ser bool, pero '{expr.expr}' es {t}")
            return "type-error"
        return "bool"

    return None
