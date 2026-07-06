# codegen/llvm_backend.py
# Backend LLVM: traduce la IR (model.Workflow) a LLVM IR textual (.ll).
#
# Esquema de traduccion (el prometido en el informe: "el workflow como un
# conjunto de bloques basicos con saltos condicionales"):
#
#   * Cada workflow se compila a una funcion:
#         define i32 @workflow_<nombre>(<params>)
#     donde los parametros son las variables declaradas:
#         bool -> i1, int -> i32, string -> ptr (cadena C terminada en \0)
#
#   * Cada estado es un bloque basico `state_<nombre>`. Al entrar se invoca
#     el hook externo `@flow_action(ptr)` con el nombre del estado, que el
#     runtime de automatizacion implementa (equivalente al hook `accion` del
#     script Python generado).
#
#   * Las transiciones de un estado se compilan, en orden de fuente, a una
#     cadena de bloques `guard`: cada guardia se evalua a un i1 y se emite
#     `br i1 %g, label %state_destino, label %siguiente_guardia`. Una
#     transicion incondicional se emite como `br label %state_destino`.
#     Si ninguna guardia aplica, se salta a `%flow_stuck` (ret i32 1).
#
#   * `state_end` retorna 0. La semantica coincide exactamente con la del
#     interprete de referencia (interpreter.py), lo que permite validar por
#     ejecucion cruzada.
#
#   * Igualdad: i1/i32 -> `icmp eq`; string -> llamada externa
#     `@flow_streq(ptr, ptr) -> i1`. and/or/not -> `and/or/xor` sobre i1
#     (las guardias son expresiones puras, sin efectos: no se requiere
#     short-circuit).
#
# El IR usa punteros opacos (`ptr`), la sintaxis de LLVM >= 15.
from exprs import VariableExpr, LiteralExpr, EqualExpr, AndExpr, OrExpr, NotExpr, infer_type
from model import START, END

_TYPE_MAP = {"bool": "i1", "int": "i32", "string": "ptr"}


def _sanitize(name):
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name)


class _Emitter:
    """Acumula lineas de IR y reparte nombres unicos de temporales/globales."""

    def __init__(self):
        self.globals = []
        self.lines = []
        self._tmp = 0
        self._str_cache = {}

    def tmp(self):
        self._tmp += 1
        return f"%t{self._tmp}"

    def emit(self, line, indent=True):
        self.lines.append(("  " if indent else "") + line)

    def cstring(self, text, hint):
        """Interna una cadena C global y devuelve su nombre @global."""
        if text in self._str_cache:
            return self._str_cache[text]
        raw = text.encode("utf-8")
        n = len(raw) + 1
        payload = "".join(
            chr(b) if 32 <= b < 127 and chr(b) not in ('"', "\\") else f"\\{b:02X}"
            for b in raw) + "\\00"
        gname = f"@.str.{_sanitize(hint)}.{len(self._str_cache)}"
        self.globals.append(
            f'{gname} = private unnamed_addr constant [{n} x i8] c"{payload}"')
        self._str_cache[text] = gname
        return gname


def _compile_expr(expr, em, symtab):
    """Compila una expresion a IR; devuelve (valor_ssa, tipo_llvm)."""
    if isinstance(expr, LiteralExpr):
        if expr.type == "bool":
            return ("1" if expr.value else "0"), "i1"
        if expr.type == "int":
            return str(expr.value), "i32"
        g = em.cstring(expr.value, "lit")
        return g, "ptr"

    if isinstance(expr, VariableExpr):
        typ = _TYPE_MAP[symtab[expr.name]]
        return f"%{_sanitize(expr.name)}", typ

    if isinstance(expr, EqualExpr):
        lv, lt = _compile_expr(expr.left, em, symtab)
        rv, _rt = _compile_expr(expr.right, em, symtab)
        out = em.tmp()
        if lt == "ptr":  # comparacion de strings via runtime
            em.emit(f"{out} = call i1 @flow_streq(ptr {lv}, ptr {rv})")
        else:
            em.emit(f"{out} = icmp eq {lt} {lv}, {rv}")
        return out, "i1"

    if isinstance(expr, AndExpr):
        lv, _ = _compile_expr(expr.left, em, symtab)
        rv, _ = _compile_expr(expr.right, em, symtab)
        out = em.tmp()
        em.emit(f"{out} = and i1 {lv}, {rv}")
        return out, "i1"

    if isinstance(expr, OrExpr):
        lv, _ = _compile_expr(expr.left, em, symtab)
        rv, _ = _compile_expr(expr.right, em, symtab)
        out = em.tmp()
        em.emit(f"{out} = or i1 {lv}, {rv}")
        return out, "i1"

    if isinstance(expr, NotExpr):
        v, _ = _compile_expr(expr.expr, em, symtab)
        out = em.tmp()
        em.emit(f"{out} = xor i1 {v}, true")
        return out, "i1"

    raise ValueError(f"expresion no soportada: {expr!r}")


def _compile_workflow(wf, em):
    symtab = wf.symbol_table
    params = ", ".join(
        f"{_TYPE_MAP[typ]} %{_sanitize(name)}" for name, typ, _l in wf.variables)

    em.emit("", indent=False)
    em.emit(f"; workflow '{wf.nombre}': cada estado es un bloque basico;", indent=False)
    em.emit("; las guardias se evaluan en orden de fuente con saltos condicionales.",
            indent=False)
    em.emit(f"define i32 @workflow_{_sanitize(wf.nombre)}({params}) {{", indent=False)

    estados = wf.orden_estados()
    em.emit("entry:", indent=False)
    em.emit(f"br label %state_{_sanitize(START)}")

    for estado in estados:
        s = _sanitize(estado)
        em.emit(f"state_{s}:", indent=False)
        gname = em.cstring(estado, estado)
        em.emit(f"call void @flow_action(ptr {gname})")

        if estado == END:
            em.emit("ret i32 0")
            continue

        salidas = wf.salidas(estado)
        if not salidas:
            # estado sumidero: el analizador semantico ya lo reporta (E308);
            # se emite terminador defensivo para mantener el IR bien formado.
            em.emit("br label %flow_stuck")
            continue
        # cadena de guardias: guard_<estado>_<i>
        for i, t in enumerate(salidas):
            if i > 0:
                em.emit(f"guard_{s}_{i}:", indent=False)
            destino = f"state_{_sanitize(t.destino)}"
            if t.condicion is None:
                em.emit(f"br label %{destino}")
                break  # transiciones posteriores son codigo muerto (W301)
            sino = (f"guard_{s}_{i + 1}" if i + 1 < len(salidas) else "flow_stuck")
            val, _typ = _compile_expr(t.condicion, em, symtab)
            em.emit(f"br i1 {val}, label %{destino}, label %{sino}")

    em.emit("flow_stuck:", indent=False)
    em.emit("ret i32 1  ; ninguna guardia aplico: ejecucion atascada")
    em.emit("}", indent=False)


def generate(workflows, module_name="flowlang"):
    """Genera el modulo LLVM IR textual para la lista de workflows."""
    em = _Emitter()
    header = [
        f"; ModuleID = '{module_name}'",
        f'source_filename = "{module_name}.flow"',
        "",
        "; Runtime minimo de automatizacion (lo implementa el sistema anfitrion):",
        "declare void @flow_action(ptr)      ; hook: ejecutar la accion del estado",
        "declare i1 @flow_streq(ptr, ptr)    ; igualdad de strings",
    ]
    for wf in workflows:
        _compile_workflow(wf, em)
    return "\n".join(header + [""] + em.globals + em.lines) + "\n"


def verify(ir_text):
    """Verifica el IR con llvmlite (bindings oficiales de LLVM), si esta
    disponible. Devuelve (ok, mensaje)."""
    try:
        import llvmlite.binding as llvm
    except ImportError:
        return None, "llvmlite no instalado: verificacion omitida"
    try:
        mod = llvm.parse_assembly(ir_text)
        mod.verify()
        return True, "modulo LLVM valido"
    except Exception as e:  # pragma: no cover
        return False, str(e)
