# codegen/json_backend.py
# Backend JSON: serializa la IR (model.Workflow) a la especificacion JSON que
# consume un motor de automatizacion. Este es el artefacto que pidio el
# profesor: el Visitor construye la IR y este backend la convierte en el JSON
# necesario para la automatizacion.
#
# Esquema (version 1.0):
# {
#   "format": "flowlang-automation",
#   "version": "1.0",
#   "workflow": "<nombre>",
#   "variables": [ {"name": ..., "type": ...}, ... ],
#   "initial_state": "start",
#   "final_state": "end",
#   "states": {
#     "<estado>": {
#       "transitions": [
#         {"target": "<estado>", "condition": <arbol de expresion> | null}
#       ]
#     }, ...
#   }
# }
#
# Las condiciones se serializan como arboles de expresion estructurados
# (no como strings), de modo que cualquier motor puede evaluarlas sin volver
# a parsear:  {"op":"and","left":{"op":"var","name":"a"},"right":...}
import json

from model import START, END

FORMAT_NAME = "flowlang-automation"
FORMAT_VERSION = "1.0"


def workflow_to_dict(wf):
    states = {}
    for estado in wf.orden_estados():
        states[estado] = {
            "transitions": [
                {
                    "target": t.destino,
                    "condition": t.condicion.to_json() if t.condicion else None,
                }
                for t in wf.salidas(estado)
            ]
        }
    return {
        "format": FORMAT_NAME,
        "version": FORMAT_VERSION,
        "workflow": wf.nombre,
        "variables": [{"name": n, "type": t} for n, t, _l in wf.variables],
        "initial_state": START,
        "final_state": END,
        "states": states,
    }


def generate(workflows):
    """Genera el JSON de automatizacion. Un objeto si hay un solo workflow,
    una lista si hay varios."""
    dicts = [workflow_to_dict(wf) for wf in workflows]
    payload = dicts[0] if len(dicts) == 1 else dicts
    return json.dumps(payload, indent=2, ensure_ascii=False)
