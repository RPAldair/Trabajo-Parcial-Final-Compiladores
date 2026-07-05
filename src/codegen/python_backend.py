# codegen/python_backend.py
# Backend de script: genera un script Python *autonomo* de automatizacion
# (segunda mitad de lo pedido por el profesor: "script o JSON").
#
# El script generado:
#   - embebe la especificacion JSON producida por json_backend (una sola
#     fuente de verdad: el mismo arbol de expresiones serializado),
#   - incluye un evaluador minimo de esas expresiones,
#   - ejecuta el workflow estado por estado invocando un hook `accion(estado)`
#     que el equipo de automatizacion reemplaza por acciones reales
#     (llamadas HTTP, envio de correos, etc.),
#   - recibe el contexto por CLI (--set var=valor) o de forma interactiva.
#
# No requiere ANTLR ni el compilador para ejecutarse: es el artefacto final
# desplegable.
import json

from codegen.json_backend import workflow_to_dict

_TEMPLATE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de automatizacion generado por el compilador FlowLang.

Workflow: {name}
Este archivo es autonomo: no necesita ANTLR ni el compilador.
Reemplace la funcion `accion(estado, ctx)` por las acciones reales de su
sistema (llamadas HTTP, correos, registros en base de datos, etc.).
"""
import argparse
import json
import sys

SPEC = json.loads(r"""
{spec}
""")

MAX_STEPS = 10000


def eval_cond(node, ctx):
    """Evalua el arbol de expresion serializado en el JSON."""
    if node is None:
        return True
    op = node["op"]
    if op == "lit":
        return node["value"]
    if op == "var":
        if node["name"] not in ctx:
            raise KeyError("variable sin valor en el contexto: " + node["name"])
        return ctx[node["name"]]
    if op == "eq":
        return eval_cond(node["left"], ctx) == eval_cond(node["right"], ctx)
    if op == "and":
        return bool(eval_cond(node["left"], ctx)) and bool(eval_cond(node["right"], ctx))
    if op == "or":
        return bool(eval_cond(node["left"], ctx)) or bool(eval_cond(node["right"], ctx))
    if op == "not":
        return not bool(eval_cond(node["expr"], ctx))
    raise ValueError("operador desconocido: " + op)


def accion(estado, ctx):
    """Hook de accion: se invoca al entrar a cada estado del workflow.

    PUNTO DE EXTENSION: sustituya este cuerpo por la logica real de cada
    paso de la automatizacion.
    """
    print("  [accion] ejecutando estado:", estado)


def ejecutar(ctx):
    estado = SPEC["initial_state"]
    trace = [estado]
    accion(estado, ctx)
    for _ in range(MAX_STEPS):
        if estado == SPEC["final_state"]:
            return trace, 0
        transiciones = SPEC["states"].get(estado, {{}}).get("transitions", [])
        siguiente = None
        for t in transiciones:
            if eval_cond(t["condition"], ctx):
                siguiente = t["target"]
                break
        if siguiente is None:
            return trace, 1  # atascado: ninguna guardia aplico
        estado = siguiente
        trace.append(estado)
        accion(estado, ctx)
    raise RuntimeError("limite de pasos superado (posible ciclo sin fin)")


def parse_valor(tipo, crudo):
    if tipo == "bool":
        if crudo.lower() in ("true", "1", "si", "yes"):
            return True
        if crudo.lower() in ("false", "0", "no"):
            return False
        raise ValueError("valor bool invalido: " + crudo)
    if tipo == "int":
        return int(crudo)
    return crudo


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta el workflow '%s'" % SPEC["workflow"])
    parser.add_argument("--set", dest="sets", action="append", default=[],
                        metavar="VAR=VALOR",
                        help="asigna una variable del contexto (repetible)")
    args = parser.parse_args()

    tipos = {{v["name"]: v["type"] for v in SPEC["variables"]}}
    ctx = {{}}
    for asignacion in args.sets:
        nombre, _, crudo = asignacion.partition("=")
        if nombre not in tipos:
            parser.error("variable desconocida: " + nombre)
        ctx[nombre] = parse_valor(tipos[nombre], crudo)

    # pedir interactivamente las variables que falten
    for nombre, tipo in tipos.items():
        if nombre not in ctx:
            crudo = input("valor de %s (%s): " % (nombre, tipo))
            ctx[nombre] = parse_valor(tipo, crudo)

    print("workflow:", SPEC["workflow"])
    print("contexto:", ctx)
    trace, code = ejecutar(ctx)
    print("recorrido:", " -> ".join(trace))
    if code == 0:
        print("resultado: OK (se alcanzo '%s')" % SPEC["final_state"])
    else:
        print("resultado: ATASCADO en '%s' (ninguna guardia aplico)" % trace[-1])
    sys.exit(code)


if __name__ == "__main__":
    main()
'''


def generate(wf):
    """Genera el codigo fuente del script de automatizacion para `wf`."""
    spec = json.dumps(workflow_to_dict(wf), indent=2, ensure_ascii=False)
    return _TEMPLATE.format(name=wf.nombre, spec=spec)
