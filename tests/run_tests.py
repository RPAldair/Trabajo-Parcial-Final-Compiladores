#!/usr/bin/env python3
# tests/run_tests.py
# Suite de validacion del compilador FlowLang (plan de validacion del informe).
#
#   FASE A - programas validos (tests/valid/*.flow):
#     A1. el frontend + analisis semantico no reporta errores
#     A2. el backend JSON produce JSON bien formado y consistente con la IR
#     A3. el backend LLVM produce un modulo que LLVM verifica como valido
#     A4. EJECUCION CRUZADA: para cada combinacion de valores de las
#         variables, la traza del interprete de referencia, la del script
#         Python generado y la del codigo maquina JIT-compilado desde el
#         LLVM IR son identicas (equivalencia semantica de los 3 backends)
#
#   FASE B - programas invalidos (tests/invalid/*.flow):
#     Cada archivo declara en su primera linea el diagnostico esperado
#     (// EXPECT: Exxx). Se comprueba que el compilador lo reporta.
#
# Uso:  python3 tests/run_tests.py
import itertools
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")
sys.path.insert(0, SRC)

from flowc import compile_file                      # noqa: E402
from codegen import json_backend, llvm_backend, python_backend  # noqa: E402
from exprs import LiteralExpr, EqualExpr, AndExpr, OrExpr, NotExpr  # noqa: E402
import interpreter                                  # noqa: E402

try:
    import llvm_exec
    HAS_JIT = True
except Exception:
    HAS_JIT = False

PASS, FAIL = "PASS", "FAIL"
results = []


def record(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  [{PASS if ok else FAIL}] {name}" + (f"  -- {detail}" if detail and not ok else ""))


# ---------------------------------------------------------------------------
def _literals(expr, out):
    if isinstance(expr, LiteralExpr):
        out.setdefault(expr.type, set()).add(expr.value)
    elif isinstance(expr, EqualExpr):
        _literals(expr.left, out)
        _literals(expr.right, out)
    elif isinstance(expr, (AndExpr, OrExpr)):
        _literals(expr.left, out)
        _literals(expr.right, out)
    elif isinstance(expr, NotExpr):
        _literals(expr.expr, out)


def contexts_for(wf, max_ctx=32):
    """Genera contextos de prueba: bools con ambos valores; ints y strings
    con los literales que aparecen en las guardias mas un valor distinto."""
    lits = {}
    for t in wf.transiciones:
        if t.condicion is not None:
            _literals(t.condicion, lits)
    domains = []
    names = []
    for name, typ, _l in wf.variables:
        names.append(name)
        if typ == "bool":
            domains.append([True, False])
        elif typ == "int":
            vals = sorted(lits.get("int", set())) or [0]
            domains.append(vals + [max(vals) + 999])
        else:
            vals = sorted(lits.get("string", set())) or ["x"]
            domains.append(vals + ["__otro__"])
    combos = list(itertools.product(*domains))[:max_ctx]
    return [dict(zip(names, c)) for c in combos] or [{}]


def run_generated_script(script_path, wf, ctx):
    """Ejecuta el script Python generado en un subproceso y extrae la traza."""
    args = [sys.executable, script_path]
    for name, _typ, _l in wf.variables:
        v = ctx[name]
        raw = ("true" if v else "false") if isinstance(v, bool) else str(v)
        args += ["--set", f"{name}={raw}"]
    proc = subprocess.run(args, capture_output=True, text=True)
    m = re.search(r"recorrido: (.+)", proc.stdout)
    trace = m.group(1).strip().split(" -> ") if m else []
    return trace, proc.returncode


# ---------------------------------------------------------------------------
def phase_a():
    print("\n=== FASE A: programas validos (equivalencia de backends) ===")
    valid_dir = os.path.join(HERE, "valid")
    tmp_dir = os.path.join(HERE, "_tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    for fname in sorted(os.listdir(valid_dir)):
        if not fname.endswith(".flow"):
            continue
        path = os.path.join(valid_dir, fname)
        print(f"\n- {fname}")
        result = compile_file(path)

        # A1: sin errores
        record("A1 compila sin errores", result.ok,
               "; ".join(str(d) for d in result.bag.errors))
        if not result.ok:
            continue

        # A2: JSON bien formado y consistente
        try:
            spec = json.loads(json_backend.generate(result.workflows))
            specs = spec if isinstance(spec, list) else [spec]
            ok = all(
                set(s["states"]) == wf.estados
                and sum(len(v["transitions"]) for v in s["states"].values())
                == len(wf.transiciones)
                for s, wf in zip(specs, result.workflows))
            record("A2 JSON bien formado y consistente con la IR", ok)
        except Exception as e:
            record("A2 JSON bien formado y consistente con la IR", False, str(e))

        # A3: LLVM IR valido
        ir = llvm_backend.generate(result.workflows,
                                   module_name=os.path.splitext(fname)[0])
        ok, msg = llvm_backend.verify(ir)
        record("A3 modulo LLVM verificado", bool(ok), msg)

        # A4: ejecucion cruzada interprete / script / LLVM JIT
        for wf in result.workflows:
            script_path = os.path.join(tmp_dir, f"{wf.nombre}_run.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(python_backend.generate(wf))

            ctxs = contexts_for(wf)
            mismatches = []
            comparados = 0
            for ctx in ctxs:
                try:
                    t_ref, c_ref = interpreter.run(wf, ctx)
                except interpreter.FlowRuntimeError:
                    continue  # ciclo sin fin bajo este contexto: se omite
                comparados += 1
                t_py, c_py = run_generated_script(script_path, wf, ctx)
                if (t_py, c_py) != (t_ref, c_ref):
                    mismatches.append(("script", ctx, t_ref, t_py))
                if HAS_JIT:
                    t_ll, c_ll = llvm_exec.run_workflow_ir(
                        ir, wf.nombre, [(n, t) for n, t, _ in wf.variables], ctx)
                    if (t_ll, c_ll) != (t_ref, c_ref):
                        mismatches.append(("llvm", ctx, t_ref, t_ll))
            record(f"A4 ejecucion cruzada '{wf.nombre}' "
                   f"({comparados} contextos x {'3' if HAS_JIT else '2'} backends)",
                   not mismatches, str(mismatches[:2]))


def phase_b():
    print("\n=== FASE B: programas invalidos (deteccion de errores) ===")
    invalid_dir = os.path.join(HERE, "invalid")
    for fname in sorted(os.listdir(invalid_dir)):
        if not fname.endswith(".flow"):
            continue
        path = os.path.join(invalid_dir, fname)
        with open(path, encoding="utf-8") as f:
            first = f.readline()
        m = re.search(r"EXPECT:\s*(\w+)", first)
        expected = m.group(1) if m else None

        result = compile_file(path)
        codes = {d.code for d in result.bag.errors}
        ok = (not result.ok) and (expected in codes if expected else True)
        record(f"B  {fname} -> espera {expected}",
               ok, f"codigos reportados: {sorted(codes)}")


def main():
    phase_a()
    phase_b()
    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    print("\n" + "=" * 60)
    print(f"RESULTADO: {passed}/{total} pruebas superadas")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
