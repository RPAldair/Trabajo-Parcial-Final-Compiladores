from antlr4 import *
from FlowLangLexer import FlowLangLexer
from FlowLangParser import FlowLangParser

def main():
    import sys
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream("""
workflow compra {python src/driver.py examples/compra.flow
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

if __name__ == '__main__':
    main()