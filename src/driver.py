from antlr4 import *
from FlowLangLexer import FlowLangLexer
from FlowLangParser import FlowLangParser
from FlowLangCustomVisitor import FlowLangCustomVisitor

def main():
    import sys
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1], encoding="utf-8")
    else:
        input_stream = InputStream("""
workflow compra {
    start -> validar
    validar -> procesar_pago if stock_ok
    validar -> cancelar if not stock_ok
    procesar_pago -> enviar_email
    cancelar -> end
    enviar_email -> end
}
""")

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
        for transition in workflow.transiciones:
            print(f"    {transition}")

if __name__ == '__main__':
    main()
