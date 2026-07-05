# interpreter.py
# Interprete de referencia de FlowLang.
#
# Ejecuta un workflow validado con un contexto de variables concreto y
# devuelve la traza de estados recorridos. Sirve como semantica operacional
# de referencia: el JSON de automatizacion, el script Python generado y el
# LLVM IR deben producir exactamente el mismo recorrido que este interprete
# (propiedad que explota el plan de validacion).
#
# Regla de ejecucion en cada estado (misma en todos los backends):
#   1. Se evaluan las transiciones de salida en orden de aparicion en el fuente.
#   2. Se toma la primera cuya guardia evalua a true (una transicion
#      incondicional equivale a guardia true).
#   3. Si ninguna aplica, la ejecucion queda "atascada" (stuck) y termina con
#      codigo de error.
from exprs import VariableExpr, LiteralExpr, EqualExpr, AndExpr, OrExpr, NotExpr
from model import START, END

MAX_STEPS = 10_000  # proteccion frente a ciclos sin salida


class FlowRuntimeError(Exception):
    pass


def eval_expr(expr, ctx):
    if isinstance(expr, LiteralExpr):
        return expr.value
    if isinstance(expr, VariableExpr):
        if expr.name not in ctx:
            raise FlowRuntimeError(f"variable sin valor en el contexto: '{expr.name}'")
        return ctx[expr.name]
    if isinstance(expr, EqualExpr):
        return eval_expr(expr.left, ctx) == eval_expr(expr.right, ctx)
    if isinstance(expr, AndExpr):
        return bool(eval_expr(expr.left, ctx)) and bool(eval_expr(expr.right, ctx))
    if isinstance(expr, OrExpr):
        return bool(eval_expr(expr.left, ctx)) or bool(eval_expr(expr.right, ctx))
    if isinstance(expr, NotExpr):
        return not bool(eval_expr(expr.expr, ctx))
    raise FlowRuntimeError(f"expresion no soportada: {expr!r}")


def run(wf, ctx, on_state=None):
    """Ejecuta `wf` con el contexto `ctx` (dict nombre -> valor).

    Devuelve (trace, exit_code): la lista de estados visitados en orden y
    0 si se alcanzo `end`, 1 si la ejecucion quedo atascada.
    `on_state(estado)` se invoca al entrar a cada estado (hook de accion).
    """
    estado = START
    trace = [estado]
    if on_state:
        on_state(estado)

    for _ in range(MAX_STEPS):
        if estado == END:
            return trace, 0
        siguiente = None
        for t in wf.salidas(estado):
            if t.condicion is None or eval_expr(t.condicion, ctx):
                siguiente = t.destino
                break
        if siguiente is None:
            return trace, 1  # atascado: ninguna guardia aplico
        estado = siguiente
        trace.append(estado)
        if on_state:
            on_state(estado)

    raise FlowRuntimeError(f"se supero el limite de {MAX_STEPS} pasos (ciclo sin fin)")


def parse_value(typ, raw):
    """Convierte un valor de linea de comandos al tipo declarado."""
    if typ == "bool":
        if raw.lower() in ("true", "1", "si", "yes"):
            return True
        if raw.lower() in ("false", "0", "no"):
            return False
        raise ValueError(f"valor bool invalido: {raw!r}")
    if typ == "int":
        return int(raw)
    return raw  # string
