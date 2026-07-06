# FlowLang — DSL para Workflows de Automatización

Compilador de **FlowLang**, un lenguaje de dominio específico para definir workflows de automatización como autómatas finitos con guardas. Trabajo Final del curso **Teoría de Compiladores** (1ACC0218, sección 3230, UPC).

Frontend con **ANTLR4** (lexer, parser, patrón Visitor), analizador semántico con tabla de símbolos y análisis de grafos, y **cuatro backends** que consumen la misma IR validada:

| Backend | Artefacto | Uso |
| --- | --- | --- |
| `json` | `programa.json` | especificación para motores de automatización |
| `script` | `programa_run.py` | script Python **autónomo** con hook `accion(estado, ctx)` |
| `llvm` | `programa.ll` | LLVM IR: cada estado = bloque básico, guardas = saltos condicionales |
| `svg` | `programa.svg` | diagrama del flujo completo (layout por capas) |

![Arquitectura](docs/arquitectura.svg)

## Ejemplo del lenguaje

```flowlang
workflow compra {
    var stock_ok : bool
    start -> validar
    validar -> procesar_pago if stock_ok
    validar -> cancelar if not stock_ok
    procesar_pago -> enviar_email
    cancelar -> end
    enviar_email -> end
}
```

## Requisitos

```bash
pip install antlr4-python3-runtime==4.9.3   # runtime de ANTLR (obligatorio)
pip install llvmlite                         # verificación y JIT de LLVM IR (recomendado)
```

## Uso del compilador (`flowc`)

```bash
cd src

python3 flowc.py check  ../examples/compra.flow            # diagnósticos (léxico/sintaxis/semántica)
python3 flowc.py ast    ../examples/compra.flow            # árbol sintáctico
python3 flowc.py json   ../examples/compra.flow -o ../output/compra.json
python3 flowc.py script ../examples/compra.flow -o ../output/compra_run.py
python3 flowc.py llvm   ../examples/compra.flow -o ../output/compra.ll
python3 flowc.py svg    ../examples/compra.flow -o ../output/compra.svg
python3 flowc.py run    ../examples/compra.flow --set stock_ok=true
python3 flowc.py build  ../examples/compra.flow -d ../output   # todos los artefactos
```

Ejecución del script de automatización generado (no requiere ANTLR ni el compilador):

```bash
python3 output/compra_run.py --set stock_ok=true
# recorrido: start -> validar -> procesar_pago -> enviar_email -> end
```

## Validación

```bash
python3 tests/run_tests.py
```

Fase A (9 programas válidos): compilación, consistencia del JSON, verificación del módulo LLVM y **ejecución cruzada** — la traza del intérprete de referencia, la del script generado y la del código máquina JIT-compilado desde el IR (llvmlite/MCJIT) deben coincidir para toda combinación de valores de las variables. Fase B (14 programas inválidos): cada archivo declara el error esperado (`// EXPECT: Exxx`). **Resultado: 50/50 PASS.**

## Estructura del repositorio

```
grammar/FlowLang.g4        gramática ANTLR4
src/
  FlowLang{Lexer,Parser,Visitor}.py   generado por ANTLR 4.9.3
  FlowLangCustomVisitor.py  Visitor: árbol -> IR
  model.py / exprs.py       IR: Workflow, Transition, AST de expresiones
  errors.py                 diagnósticos + error listeners (E101/E201)
  semantic.py               analizador semántico (E301–E309, W301–W303)
  codegen/                  backends: json, python(script), llvm, svg
  interpreter.py            intérprete de referencia
  llvm_exec.py              ejecución JIT del IR (validación cruzada)
  flowc.py                  CLI del compilador
  driver.py                 driver simple (compatibilidad Hito 1)
examples/*.flow             programas de ejemplo
tests/                      suite de validación (valid/, invalid/, run_tests.py)
docs/                       informe final (markdown) + diagramas SVG
```

Para regenerar el parser tras modificar la gramática:

```bash
java -jar antlr-4.9.3-complete.jar -Dlanguage=Python3 -visitor -no-listener -o src grammar/FlowLang.g4
```

## Códigos de diagnóstico

`E101` léxico · `E201` sintáctico · `E301` sin salida de `start` · `E302` no se llega a `end` · `E303` variable duplicada · `E304` variable no declarada · `E305` tipos incompatibles · `E306` guardia no booleana · `E307` estado inalcanzable · `E308` estado sumidero · `E309` ciclo sin salida · `W301` transición muerta · `W302` variable sin uso · `W303` salidas desde `end`.
