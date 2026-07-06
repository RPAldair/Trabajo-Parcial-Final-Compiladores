# Paquete de backends de generacion de codigo de FlowLang.
# Todos consumen la misma IR (model.Workflow) validada por semantic.py:
#   json_backend    -> especificacion JSON para motores de automatizacion
#   python_backend  -> script Python autonomo ejecutable
#   llvm_backend    -> LLVM IR (bloques basicos + saltos condicionales)
#   svg_backend     -> diagrama del grafo del workflow
