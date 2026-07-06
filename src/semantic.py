# semantic.py
# Analizador semantico de FlowLang.
#
# Recibe la IR (model.Workflow) construida por el Visitor y verifica, con la
# tabla de simbolos y algoritmos de grafos, las propiedades prometidas por el
# diseño del lenguaje (el workflow como DFA con guardas):
#
#   E301  no existe transicion que parta de `start`
#   E302  ninguna transicion llega a `end`
#   E303  variable duplicada
#   E304  variable usada sin declarar
#   E305  incompatibilidad de tipos en una condicion (p.ej. string == int)
#   E306  condicion de guardia no booleana (p.ej. `if edad` con edad:int)
#   E307  estado inalcanzable desde `start`
#   E308  estado sumidero: sin transiciones de salida y distinto de `end`
#   E309  ciclo sin salida: estado alcanzable desde el que no se llega a `end`
#   W301  transicion muerta: aparece despues de una incondicional del mismo origen
#   W302  variable declarada pero nunca usada
#   W303  `end` tiene transiciones de salida (se ignoran en ejecucion)
#
# Los codigos E1xx/E2xx (lexico/sintactico) se emiten en errors.py.
from exprs import collect_vars, infer_type
from model import START, END


class SemanticAnalyzer:
    def __init__(self, bag):
        self.bag = bag  # errors.DiagnosticBag

    def analyze_program(self, workflows):
        for wf in workflows:
            self.analyze(wf)

    def analyze(self, wf):
        self._check_variables(wf)
        self._check_conditions(wf)
        self._check_graph(wf)

    # ------------------------------------------------------------------
    def _check_variables(self, wf):
        vistos = set()
        for name, _typ, line in wf.variables:
            if name in vistos:
                self.bag.error(
                    "semantico", "E303",
                    f"variable duplicada '{name}' en workflow '{wf.nombre}'", line)
            vistos.add(name)

        # W302: variables nunca usadas en ninguna condicion
        usadas = set()
        for t in wf.transiciones:
            if t.condicion is not None:
                usadas |= collect_vars(t.condicion)
        for name, _typ, line in wf.variables:
            if name not in usadas:
                self.bag.warning(
                    "semantico", "W302",
                    f"variable '{name}' declarada pero nunca usada", line)

    # ------------------------------------------------------------------
    def _check_conditions(self, wf):
        symtab = wf.symbol_table
        for t in wf.transiciones:
            expr = t.condicion
            if expr is None:
                continue

            # E304: variables no declaradas
            faltantes = sorted(collect_vars(expr) - set(symtab))
            for name in faltantes:
                self.bag.error(
                    "semantico", "E304",
                    f"variable usada sin declarar: '{name}' en condicion de "
                    f"'{t.origen} -> {t.destino}'", t.line)

            # E305 / E306: verificacion de tipos sobre el arbol de expresion
            detalles = []
            tipo = infer_type(expr, symtab, detalles)
            for msg in detalles:
                self.bag.error("semantico", "E305", msg, t.line)
            if tipo in ("int", "string"):
                self.bag.error(
                    "semantico", "E306",
                    f"la condicion de guardia debe ser bool, pero '{expr}' es {tipo}",
                    t.line)

    # ------------------------------------------------------------------
    def _check_graph(self, wf):
        estados = wf.estados

        # E301 / E302
        sale_de_start = any(t.origen == START for t in wf.transiciones)
        llega_a_end = any(t.destino == END for t in wf.transiciones)
        if not sale_de_start:
            self.bag.error(
                "semantico", "E301",
                f"workflow '{wf.nombre}': ninguna transicion parte de '{START}'",
                wf.line)
        if not llega_a_end:
            self.bag.error(
                "semantico", "E302",
                f"workflow '{wf.nombre}': ninguna transicion llega a '{END}'",
                wf.line)

        # Grafo dirigido para alcanzabilidad
        graph = {s: [] for s in estados}
        for t in wf.transiciones:
            graph[t.origen].append(t.destino)

        # E307: inalcanzables desde start (DFS)
        reachable = set()
        if START in estados:
            stack = [START]
            while stack:
                n = stack.pop()
                if n in reachable:
                    continue
                reachable.add(n)
                stack.extend(m for m in graph[n] if m not in reachable)
        for s in sorted(estados - reachable):
            self.bag.error(
                "semantico", "E307",
                f"estado inalcanzable desde '{START}': '{s}'",
                self._first_line_of(wf, s))

        # E308: sumideros (sin salidas) distintos de end
        for s in sorted(estados):
            if s != END and not graph[s]:
                self.bag.error(
                    "semantico", "E308",
                    f"estado sumidero (sin transiciones de salida): '{s}'",
                    self._first_line_of(wf, s))

        # E309: trampas / ciclos sin salida — estados alcanzables desde los
        # que es imposible llegar a `end` (alcanzabilidad inversa desde end)
        rgraph = {s: [] for s in estados}
        for t in wf.transiciones:
            rgraph[t.destino].append(t.origen)
        alcanza_end = set()
        if END in estados:
            stack = [END]
            while stack:
                n = stack.pop()
                if n in alcanza_end:
                    continue
                alcanza_end.add(n)
                stack.extend(m for m in rgraph[n] if m not in alcanza_end)
        for s in sorted((reachable & estados) - alcanza_end):
            # se excluyen sumideros: ya reportados como E308
            if graph[s]:
                self.bag.error(
                    "semantico", "E309",
                    f"ciclo sin salida: desde '{s}' es imposible alcanzar '{END}'",
                    self._first_line_of(wf, s))

        # W301: transiciones muertas despues de una incondicional
        for s in sorted(estados):
            salidas = wf.salidas(s)
            incondicional_vista = False
            for t in salidas:
                if incondicional_vista:
                    self.bag.warning(
                        "semantico", "W301",
                        f"transicion muerta: '{t}' nunca se evalua porque una "
                        f"transicion incondicional anterior desde '{s}' siempre se toma",
                        t.line)
                if t.condicion is None:
                    incondicional_vista = True

        # W303: salidas desde end
        for t in wf.salidas(END):
            self.bag.warning(
                "semantico", "W303",
                f"transicion desde '{END}' se ignora en ejecucion: '{t}'", t.line)

    @staticmethod
    def _first_line_of(wf, estado):
        for t in wf.transiciones:
            if estado in (t.origen, t.destino):
                return t.line
        return wf.line
