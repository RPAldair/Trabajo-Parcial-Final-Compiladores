# Recorre el árbol sintáctico producido por FlowLangParser usando el patrón
# Visitor de ANTLR4 y construye una representación estructurada de cada
# workflow: su nombre, sus transiciones y sus condiciones de guardia.
from antlr4 import *
from exprs import (
    VariableExpr,
    LiteralExpr,
    EqualExpr,
    AndExpr,
    OrExpr,
    NotExpr
)
if __name__ is not None and "." in __name__:
    from .FlowLangParser import FlowLangParser
    from .FlowLangVisitor import FlowLangVisitor
else:
    from FlowLangParser import FlowLangParser
    from FlowLangVisitor import FlowLangVisitor


class Transition:
    # Representa una transición: origen -> destino [if [not] condicion]
    def __init__(self, origen, destino, condicion=None):
        self.origen = origen
        self.destino = destino
        self.condicion = condicion

    def __str__(self):
        if self.condicion is None:
            return f"{self.origen} -> {self.destino}"
        return f"{self.origen} -> {self.destino} if {self.condicion}"


class Workflow:
    # Representa un workflow con su nombre y su lista de transiciones
    def __init__(self, nombre):
        self.nombre = nombre
        self.transiciones = []
        self.variables = []

    @property
    def estados(self):
        # Conjunto de estados que aparecen como origen o destino
        nombres = set()
        for t in self.transiciones:
            nombres.add(t.origen)
            nombres.add(t.destino)
        return nombres


class FlowLangCustomVisitor(FlowLangVisitor):
    # Construye la lista de workflows recorriendo el árbol con el patrón Visitor
    def __init__(self):
        self.workflows = []

    # root : workflow+ EOF ;
    def visitRoot(self, ctx:FlowLangParser.RootContext):
        for workflow_ctx in ctx.workflow():
            self.workflows.append(self.visit(workflow_ctx))
        return self.workflows

    # workflow : WORKFLOW ID LBRACE varDecl* transition+ RBRACE ;
    def visitWorkflow(self, ctx:FlowLangParser.WorkflowContext):
        workflow = Workflow(ctx.ID().getText())
        # variables (varDecl)
        for var_ctx in ctx.varDecl():
            name = var_ctx.ID().getText()
            # type : BOOLTYPE | INTTYPE | STRINGTYPE
            typ = var_ctx.dataType().getText()
            workflow.variables.append((name, typ))
        # transiciones
        for transition_ctx in ctx.transition():
            workflow.transiciones.append(self.visit(transition_ctx))
        return workflow

    # varDecl : VAR ID COLON type ;
    def visitVarDecl(self, ctx:FlowLangParser.VarDeclContext):
        name = ctx.ID().getText()
        typ = ctx.dataType().getText()
        return (name, typ)

    # transition : step ARROW step (IF NOT? condition)? ;
    def visitTransition(self, ctx:FlowLangParser.TransitionContext):
        origen = self.visit(ctx.step(0))
        destino = self.visit(ctx.step(1))
        condicion = None
        
        if ctx.IF() is not None:
            condicion = self.visit(ctx.condition())
            
        return Transition(origen, destino, condicion)

    # step : ID | START | END ;
    def visitStep(self, ctx:FlowLangParser.StepContext):
        return ctx.getText()

    # condition : ID ;
    def visitCondition(self, ctx:FlowLangParser.ConditionContext):
        return self.visit(ctx.expr())

    def visitExpr(self, ctx):
        return self.visit(ctx.orExpr())
    

    def visitOrExpr(self, ctx):
        exprs = [self.visit(x) for x in ctx.andExpr()]

        result = exprs[0]

        for e in exprs[1:]:
            result = OrExpr(result, e)

        return result
    

    def visitAndExpr(self, ctx):
        exprs = [self.visit(x) for x in ctx.notExpr()]

        result = exprs[0]

        for e in exprs[1:]:
            result = AndExpr(result, e)

        return result


    def visitNotExpr(self, ctx):

        if ctx.NOT():
            return NotExpr(
                self.visit(ctx.notExpr())
            )

        return self.visit(ctx.comparison())
    

    def visitComparison(self, ctx):

        left = self.visit(ctx.primary(0))

        if ctx.EQ():
            right = self.visit(ctx.primary(1))
            return EqualExpr(left, right)

        return left
    

    def visitPrimary(self, ctx):

        if ctx.ID():
            return VariableExpr(ctx.ID().getText())

        if ctx.NUMBER():
            return LiteralExpr(
                int(ctx.NUMBER().getText()),
                "int"
            )

        if ctx.STRING():
            txt = ctx.STRING().getText()[1:-1]
            return LiteralExpr(txt, "string")

        if ctx.TRUE():
            return LiteralExpr(True, "bool")

        if ctx.FALSE():
            return LiteralExpr(False, "bool")

        if ctx.expr():
            return self.visit(ctx.expr())