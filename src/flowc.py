#!/usr/bin/env python3
# flowc.py
# CLI del compilador FlowLang. Orquesta el pipeline completo:
#
#   .flow --lexer--> tokens --parser--> arbol --visitor--> IR (model.Workflow)
#        --semantico--> IR validada --backends--> JSON | script .py | .ll | .svg
#
# Subcomandos:
#   check   file.flow                  analiza y reporta diagnosticos
#   ast     file.flow                  imprime el arbol sintactico
#   json    file.flow [-o out.json]    genera el JSON de automatizacion
#   script  file.flow [-o out.py]      genera el script Python autonomo
#   llvm    file.flow [-o out.ll]      genera LLVM IR (y lo verifica)
#   svg     file.flow [-o out.svg]     genera el diagrama del workflow
#   run     file.flow --set v=x ...    ejecuta con el interprete de referencia
#   build   file.flow [-d outdir]      genera todos los artefactos
import argparse
import os
import sys

from antlr4 import FileStream, CommonTokenStream

from FlowLangLexer import FlowLangLexer
from FlowLangParser import FlowLangParser
from FlowLangCustomVisitor import FlowLangCustomVisitor
from errors import DiagnosticBag, CollectingLexerErrorListener, CollectingParserErrorListener
from semantic import SemanticAnalyzer
from codegen import json_backend, python_backend, llvm_backend, svg_backend
import interpreter


class CompilationResult:
    def __init__(self, tree, parser, workflows, bag):
        self.tree = tree
        self.parser = parser
        self.workflows = workflows or []
        self.bag = bag

    @property
    def ok(self):
        return not self.bag.has_errors()


def compile_file(path):
    """Frontend completo: lexico + sintactico + visitor + semantico."""
    bag = DiagnosticBag()
    input_stream = FileStream(path, encoding="utf-8")

    lexer = FlowLangLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(CollectingLexerErrorListener(bag))
    tokens = CommonTokenStream(lexer)

    parser = FlowLangParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(CollectingParserErrorListener(bag))
    tree = parser.root()

    workflows = []
    if not bag.has_errors():
        # solo se construye la IR y se analiza si el frontend no fallo
        workflows = FlowLangCustomVisitor().visit(tree) or []
        SemanticAnalyzer(bag).analyze_program(workflows)
    return CompilationResult(tree, parser, workflows, bag)


def report(bag, file=sys.stderr):
    for d in bag:
        print(str(d), file=file)
    if bag.has_errors():
        print(f"-- {len(bag.errors)} error(es), {len(bag.warnings)} warning(s)",
              file=file)
    elif bag.warnings:
        print(f"-- 0 errores, {len(bag.warnings)} warning(s)", file=file)


def _require_ok(result):
    report(result.bag)
    if not result.ok:
        sys.exit(2)


def _write(path, content):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"generado: {path}")


def _default_out(source, ext, outdir=None):
    base = os.path.splitext(os.path.basename(source))[0]
    return os.path.join(outdir or "output", base + ext)


# ---------------------------------------------------------------- comandos
def cmd_check(args):
    result = compile_file(args.file)
    report(result.bag, file=sys.stdout)
    if result.ok:
        for wf in result.workflows:
            print(f"OK workflow '{wf.nombre}': {len(wf.estados)} estados, "
                  f"{len(wf.transiciones)} transiciones, "
                  f"{len(wf.variables)} variables")
    sys.exit(0 if result.ok else 2)


def cmd_ast(args):
    result = compile_file(args.file)
    print(result.tree.toStringTree(recog=result.parser))
    report(result.bag)
    sys.exit(0 if result.ok else 2)


def cmd_json(args):
    result = compile_file(args.file)
    _require_ok(result)
    out = args.output or _default_out(args.file, ".json")
    _write(out, json_backend.generate(result.workflows))


def cmd_script(args):
    result = compile_file(args.file)
    _require_ok(result)
    for wf in result.workflows:
        suffix = f"_{wf.nombre}" if len(result.workflows) > 1 else ""
        out = args.output if (args.output and len(result.workflows) == 1) else \
            _default_out(args.file, f"{suffix}_run.py")
        _write(out, python_backend.generate(wf))
        os.chmod(out, 0o755)


def cmd_llvm(args):
    result = compile_file(args.file)
    _require_ok(result)
    module = os.path.splitext(os.path.basename(args.file))[0]
    ir = llvm_backend.generate(result.workflows, module_name=module)
    out = args.output or _default_out(args.file, ".ll")
    _write(out, ir)
    ok, msg = llvm_backend.verify(ir)
    print(f"verificacion LLVM: {msg}")
    if ok is False:
        sys.exit(3)


def cmd_svg(args):
    result = compile_file(args.file)
    _require_ok(result)
    for wf in result.workflows:
        suffix = f"_{wf.nombre}" if len(result.workflows) > 1 else ""
        out = args.output if (args.output and len(result.workflows) == 1) else \
            _default_out(args.file, f"{suffix}.svg")
        _write(out, svg_backend.generate(wf, title=f"workflow {wf.nombre}"))


def cmd_run(args):
    result = compile_file(args.file)
    _require_ok(result)
    wf = result.workflows[0]
    if args.workflow:
        matches = [w for w in result.workflows if w.nombre == args.workflow]
        if not matches:
            print(f"workflow no encontrado: {args.workflow}", file=sys.stderr)
            sys.exit(2)
        wf = matches[0]

    tipos = wf.symbol_table
    ctx = {}
    for asignacion in args.sets or []:
        nombre, _, crudo = asignacion.partition("=")
        if nombre not in tipos:
            print(f"variable desconocida: {nombre}", file=sys.stderr)
            sys.exit(2)
        ctx[nombre] = interpreter.parse_value(tipos[nombre], crudo)
    for nombre, tipo in tipos.items():
        if nombre not in ctx:
            ctx[nombre] = interpreter.parse_value(
                tipo, input(f"valor de {nombre} ({tipo}): "))

    print(f"workflow: {wf.nombre}")
    print(f"contexto: {ctx}")
    trace, code = interpreter.run(wf, ctx)
    print("recorrido:", " -> ".join(trace))
    print("resultado:", "OK (se alcanzo 'end')" if code == 0
          else f"ATASCADO en '{trace[-1]}'")
    sys.exit(code)


def cmd_build(args):
    result = compile_file(args.file)
    _require_ok(result)
    outdir = args.dir or "output"
    base = os.path.splitext(os.path.basename(args.file))[0]

    _write(os.path.join(outdir, base + ".json"),
           json_backend.generate(result.workflows))

    ir = llvm_backend.generate(result.workflows, module_name=base)
    _write(os.path.join(outdir, base + ".ll"), ir)
    ok, msg = llvm_backend.verify(ir)
    print(f"verificacion LLVM: {msg}")

    for wf in result.workflows:
        suffix = f"_{wf.nombre}" if len(result.workflows) > 1 else ""
        _write(os.path.join(outdir, f"{base}{suffix}_run.py"),
               python_backend.generate(wf))
        _write(os.path.join(outdir, f"{base}{suffix}.svg"),
               svg_backend.generate(wf, title=f"workflow {wf.nombre}"))
    if ok is False:
        sys.exit(3)


def main():
    p = argparse.ArgumentParser(prog="flowc", description="Compilador FlowLang")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_):
        sp = sub.add_parser(name, help=help_)
        sp.add_argument("file", help="archivo fuente .flow")
        sp.set_defaults(fn=fn)
        return sp

    add("check", cmd_check, "analisis lexico, sintactico y semantico")
    add("ast", cmd_ast, "imprime el arbol sintactico")
    for name, fn, help_ in [
        ("json", cmd_json, "genera JSON de automatizacion"),
        ("script", cmd_script, "genera script Python autonomo"),
        ("llvm", cmd_llvm, "genera LLVM IR"),
        ("svg", cmd_svg, "genera diagrama SVG"),
    ]:
        sp = add(name, fn, help_)
        sp.add_argument("-o", "--output", help="ruta de salida")

    sp = add("run", cmd_run, "ejecuta con el interprete de referencia")
    sp.add_argument("--set", dest="sets", action="append", metavar="VAR=VALOR",
                    help="asigna una variable del contexto (repetible)")
    sp.add_argument("--workflow", help="nombre del workflow si hay varios")

    sp = add("build", cmd_build, "genera todos los artefactos")
    sp.add_argument("-d", "--dir", help="directorio de salida (default: output/)")

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
