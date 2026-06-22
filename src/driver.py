from antlr4 import *
from FlowLangLexer import FlowLangLexer
from FlowLangParser import FlowLangParser
from FlowLangCustomVisitor import FlowLangCustomVisitor
from exprs import collect_vars, infer_type
import re


def main():
    import sys
    source_text = None
    if len(sys.argv) > 1:
        path = sys.argv[1]
        input_stream = FileStream(path, encoding="utf-8")
        with open(path, encoding='utf-8') as f:
            source_text = f.read()
    else:
        input_stream = InputStream("""
workflow compra {
    var stock_ok : bool
    start -> validar
    validar -> procesar_pago if stock_ok
    validar -> cancelar if not stock_ok
    procesar_pago -> enviar_email
    cancelar -> end
    enviar_email -> end
}
""")
        source_text = input_stream.strdata

    lexer = FlowLangLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FlowLangParser(token_stream)

    tree = parser.root()

    print("Árbol Sintáctico")
    print(tree.toStringTree(recog=parser))

    # Recorrido con el patrón Visitor para construir la representación de los workflows
    visitor = FlowLangCustomVisitor()
    workflows = visitor.visit(tree)

    print()
    print("Resumen de Workflows")
    for workflow in workflows:
        print()
        print(f"workflow: {workflow.nombre}")
        print(f"  estados ({len(workflow.estados)}): {', '.join(sorted(workflow.estados))}")
        print(f"  transiciones ({len(workflow.transiciones)}):")
        # las variables ya se recogen desde el Visitor (`workflow.variables`)

        # construir tabla de símbolos
        symtab = {name:typ for (name,typ) in getattr(workflow, 'variables', [])}

        # validar variables duplicadas
        names = [n for (n,_) in getattr(workflow, 'variables',[])]
        dups = set([n for n in names if names.count(n) > 1])
        for d in dups:
            print(f"  ERROR: variable duplicada: {d}")

        # procesar transiciones y condiciones
        for transition in workflow.transiciones:
            expr = transition.condicion
            if expr is None:
                print(f"    {transition}")
                continue
           
            # comprobar variables usadas
            used = collect_vars(expr)
            for u in used:
                if u not in symtab:
                    print(f"  ERROR: variable usada sin declarar: {u} en workflow {workflow.nombre}")
            # inferir tipo de la expresion
            t = infer_type(expr, symtab)
            if t == 'type-error':
                print(f"  ERROR: incompatibilidad de tipos en condición: {expr}")
            elif t is None:
                print(f"  ERROR: tipo desconocido en condición: {expr}")

            # show transition with parsed expr
            print(f"    {transition.origen} -> {transition.destino} if {expr}")

        # comprobaciones semánticas globales
        estados = set(workflow.estados)
        if 'start' not in estados:
            print(f"  ERROR: falta estado 'start' en workflow {workflow.nombre}")
        if 'end' not in estados:
            print(f"  ERROR: falta estado 'end' en workflow {workflow.nombre}")

        # detectar inalcanzables y sumideros
        # construir grafo dirigido
        graph = {s:set() for s in estados}
        for t in workflow.transiciones:
            graph.setdefault(t.origen, set()).add(t.destino)
        # reachable from start
        reachable = set()
        if 'start' in estados:
            stack = ['start']
            while stack:
                n = stack.pop()
                if n in reachable: continue
                reachable.add(n)
                for m in graph.get(n,[]):
                    if m not in reachable:
                        stack.append(m)
        unreachable = estados - reachable
        for u in sorted(unreachable):
            print(f"  WARNING: estado inalcanzable: {u}")
        # sumideros: nodes with outdegree 0 that are not 'end'
        for s, outs in graph.items():
            if len(outs) == 0 and s != 'end':
                print(f"  WARNING: estado sumidero (sin salidas): {s}")


if __name__ == '__main__':
    main()
