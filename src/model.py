# model.py
# Representacion intermedia (IR de alto nivel) de un programa FlowLang.
# Es el resultado del recorrido del arbol sintactico con el Visitor y la
# entrada comun de: analizador semantico, interprete y todos los backends
# (JSON, script Python, LLVM IR, SVG).

START = "start"
END = "end"


class Transition:
    """Una transicion: origen -> destino [if condicion].

    `condicion` es un arbol de expresiones (exprs.Expr) o None si la
    transicion es incondicional. `line` conserva la linea del fuente para
    diagnosticos.
    """

    def __init__(self, origen, destino, condicion=None, line=None):
        self.origen = origen
        self.destino = destino
        self.condicion = condicion
        self.line = line

    def __str__(self):
        if self.condicion is None:
            return f"{self.origen} -> {self.destino}"
        return f"{self.origen} -> {self.destino} if {self.condicion}"


class Workflow:
    """Un workflow: nombre, variables tipadas y lista ordenada de transiciones."""

    def __init__(self, nombre, line=None):
        self.nombre = nombre
        self.line = line
        self.variables = []      # lista de (nombre, tipo, linea)
        self.transiciones = []   # lista de Transition (en orden de fuente)

    @property
    def estados(self):
        """Conjunto de estados que aparecen como origen o destino."""
        nombres = set()
        for t in self.transiciones:
            nombres.add(t.origen)
            nombres.add(t.destino)
        return nombres

    @property
    def symbol_table(self):
        """Tabla de simbolos: nombre de variable -> tipo (primera declaracion)."""
        tabla = {}
        for name, typ, _line in self.variables:
            tabla.setdefault(name, typ)
        return tabla

    def salidas(self, estado):
        """Transiciones que salen de `estado`, en orden de fuente."""
        return [t for t in self.transiciones if t.origen == estado]

    def orden_estados(self):
        """Estados en orden estable: start, luego por primera aparicion, end al final."""
        vistos = []
        for t in self.transiciones:
            for s in (t.origen, t.destino):
                if s not in vistos:
                    vistos.append(s)
        orden = [s for s in vistos if s not in (START, END)]
        resultado = []
        if START in self.estados:
            resultado.append(START)
        resultado.extend(orden)
        if END in self.estados:
            resultado.append(END)
        return resultado
