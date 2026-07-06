# llvm_exec.py
# Ejecucion JIT del LLVM IR generado, usando llvmlite (bindings de LLVM).
#
# Este modulo cierra el circulo del plan de validacion: no solo verificamos
# que el IR es sintacticamente valido (`llvm_backend.verify`), sino que lo
# COMPILAMOS a codigo maquina con MCJIT y lo EJECUTAMOS, registrando el hook
# @flow_action como un callback de ctypes que captura la traza de estados.
# Asi podemos comparar, para el mismo contexto de variables:
#
#     traza del interprete de referencia  ==  traza del codigo maquina LLVM
#
# Si ambas coinciden en todos los casos de prueba, el backend LLVM preserva
# la semantica del lenguaje.
import ctypes

import llvmlite.binding as llvm

llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


def run_workflow_ir(ir_text, wf_name, variables, ctx):
    """Compila `ir_text` con MCJIT y ejecuta @workflow_<wf_name>.

    variables: lista de (nombre, tipo) en orden de declaracion.
    ctx: dict nombre -> valor Python.
    Devuelve (trace, exit_code) igual que interpreter.run.
    """
    trace = []

    # callback para @flow_action(ptr): registra el estado visitado
    ACTION_T = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
    action_cb = ACTION_T(lambda name: trace.append(name.decode("utf-8")))

    # callback para @flow_streq(ptr, ptr) -> i1
    STREQ_T = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p)
    streq_cb = STREQ_T(lambda a, b: a == b)

    llvm.add_symbol("flow_action", ctypes.cast(action_cb, ctypes.c_void_p).value)
    llvm.add_symbol("flow_streq", ctypes.cast(streq_cb, ctypes.c_void_p).value)

    mod = llvm.parse_assembly(ir_text)
    mod.verify()
    target = llvm.Target.from_default_triple().create_target_machine()
    engine = llvm.create_mcjit_compiler(mod, target)
    engine.finalize_object()

    addr = engine.get_function_address(f"workflow_{wf_name}")

    # firma de la funcion segun los tipos declarados
    argtypes = []
    argvals = []
    keepalive = []
    for name, typ in variables:
        val = ctx[name]
        if typ == "bool":
            argtypes.append(ctypes.c_bool)
            argvals.append(bool(val))
        elif typ == "int":
            argtypes.append(ctypes.c_int32)
            argvals.append(int(val))
        else:  # string
            argtypes.append(ctypes.c_char_p)
            buf = ctypes.create_string_buffer(str(val).encode("utf-8"))
            keepalive.append(buf)
            argvals.append(ctypes.cast(buf, ctypes.c_char_p))

    fn = ctypes.CFUNCTYPE(ctypes.c_int32, *argtypes)(addr)
    code = fn(*argvals)
    # mantener vivos los callbacks y el engine hasta despues de la llamada
    del engine, action_cb, streq_cb, keepalive
    return trace, code
