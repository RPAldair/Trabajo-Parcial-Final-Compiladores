#!/usr/bin/env python3
# driver.py
# Driver simple conservado por compatibilidad con el Hito 1.
# El punto de entrada principal del compilador es ahora flowc.py:
#     python3 flowc.py check|json|script|llvm|svg|run|build <archivo.flow>
import sys

from antlr4 import FileStream, InputStream, CommonTokenStream

from FlowLangLexer import FlowLangLexer
from FlowLangParser import FlowLangParser
from FlowLangCustomVisitor import FlowLangCustomVisitor
from errors import DiagnosticBag, CollectingLexerErrorListener, CollectingParserErrorListener
from semantic import SemanticAnalyzer

EJEMPLO = """
workflow compra {
    var stock_ok : bool
    start -> validar
    validar -> procesar_pago if stock_ok
    validar -> cancelar if not stock_ok
    procesar_pago -> enviar_email
    cancelar -> end
    enviar_email -> end
}
"""


def main():
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1], encoding="utf-8")
    else:
        input_stream = InputStream(EJEMPLO)

    bag = DiagnosticBag()
    lexer = FlowLangLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(CollectingLexerErrorListener(bag))
    parser = FlowLangParser(CommonTokenStream(lexer))
    parser.removeErrorListeners()
    parser.addErrorListener(CollectingParserErrorListener(bag))

    tree = parser.root()
    print("Arbol Sintactico")
    print(tree.toStringTree(recog=parser))

    if bag.has_errors():
        for d in bag:
            print(d)
        sys.exit(2)

    workflows = FlowLangCustomVisitor().visit(tree)
    SemanticAnalyzer(bag).analyze_program(workflows)

    print()
    print("Resumen de Workflows")
    for wf in workflows:
        print()
        print(f"workflow: {wf.nombre}")
        print(f"  variables ({len(wf.variables)}): "
              + ", ".join(f"{n}:{t}" for n, t, _ in wf.variables))
        print(f"  estados ({len(wf.estados)}): {', '.join(sorted(wf.estados))}")
        print(f"  transiciones ({len(wf.transiciones)}):")
        for t in wf.transiciones:
            print(f"    {t}")

    print()
    print("Diagnosticos")
    if not bag.items:
        print("  (sin diagnosticos)")
    for d in bag:
        print(f"  {d}")
    sys.exit(2 if bag.has_errors() else 0)


if __name__ == "__main__":
    main()
