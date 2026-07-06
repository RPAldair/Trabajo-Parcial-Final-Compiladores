# errors.py
# Diagnosticos del compilador y captura de errores lexicos/sintacticos.
#
# ANTLR4 imprime errores por consola por defecto; para un compilador real
# necesitamos recolectarlos, clasificarlos por fase y decidir si continuar.
from antlr4.error.ErrorListener import ErrorListener


class Diagnostic:
    """Un diagnostico del compilador con fase, severidad, codigo y ubicacion."""

    ERROR = "error"
    WARNING = "warning"

    def __init__(self, phase, severity, code, message, line=None, column=None):
        self.phase = phase          # 'lexico' | 'sintactico' | 'semantico'
        self.severity = severity    # 'error' | 'warning'
        self.code = code            # p.ej. 'E004'
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        loc = ""
        if self.line is not None:
            loc = f"linea {self.line}"
            if self.column is not None:
                loc += f":{self.column}"
            loc = f" [{loc}]"
        return f"{self.severity.upper()} {self.code} ({self.phase}){loc}: {self.message}"


class DiagnosticBag:
    """Acumulador de diagnosticos compartido por todas las fases."""

    def __init__(self):
        self.items = []

    def error(self, phase, code, message, line=None, column=None):
        self.items.append(Diagnostic(phase, Diagnostic.ERROR, code, message, line, column))

    def warning(self, phase, code, message, line=None, column=None):
        self.items.append(Diagnostic(phase, Diagnostic.WARNING, code, message, line, column))

    @property
    def errors(self):
        return [d for d in self.items if d.severity == Diagnostic.ERROR]

    @property
    def warnings(self):
        return [d for d in self.items if d.severity == Diagnostic.WARNING]

    def has_errors(self):
        return bool(self.errors)

    def __iter__(self):
        return iter(self.items)


class CollectingLexerErrorListener(ErrorListener):
    """Captura errores lexicos (token no reconocido) como diagnosticos E101."""

    def __init__(self, bag):
        self.bag = bag

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.bag.error("lexico", "E101", msg, line, column)


class CollectingParserErrorListener(ErrorListener):
    """Captura errores sintacticos del parser como diagnosticos E201."""

    def __init__(self, bag):
        self.bag = bag

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.bag.error("sintactico", "E201", msg, line, column)
