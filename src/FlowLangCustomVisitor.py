# Recorre el árbol sintáctico producido por FlowLangParser usando el patrón
# Visitor de ANTLR4 y construye una representación estructurada de cada
# workflow: su nombre, sus transiciones y sus condiciones de guardia.
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FlowLangParser import FlowLangParser
    from .FlowLangVisitor import FlowLangVisitor
else:
    from FlowLangParser import FlowLangParser
    from FlowLangVisitor import FlowLangVisitor


class Transition:
    # Representa una transición: origen -> destino [if [not] condicion]
    def __init__(self, origen, destino, condicion=None, negada=False):
        self.origen = origen
        self.destino = destino
        self.condicion = condicion
        self.negada = negada

    def __str__(self):
        if self.condicion is None:
            return f"{self.origen} -> {self.destino}"
        guarda = f"if not {self.condicion}" if self.negada else f"if {self.condicion}"
        return f"{self.origen} -> {self.destino} {guarda}"


class Workflow:
    # Representa un workflow con su nombre y su lista de transiciones
    def __init__(self, nombre):
        self.nombre = nombre
        self.transiciones = []

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

    # workflow : WORKFLOW ID LBRACE transition+ RBRACE ;
    def visitWorkflow(self, ctx:FlowLangParser.WorkflowContext):
        workflow = Workflow(ctx.ID().getText())
        for transition_ctx in ctx.transition():
            workflow.transiciones.append(self.visit(transition_ctx))
        return workflow

    # transition : step ARROW step (IF NOT? condition)? ;
    def visitTransition(self, ctx:FlowLangParser.TransitionContext):
        origen = self.visit(ctx.step(0))
        destino = self.visit(ctx.step(1))
        condicion = None
        negada = False
        if ctx.IF() is not None:
            condicion = self.visit(ctx.condition())
            negada = ctx.NOT() is not None
        return Transition(origen, destino, condicion, negada)

    # step : ID | START | END ;
    def visitStep(self, ctx:FlowLangParser.StepContext):
        return ctx.getText()

    # condition : ID ;
    def visitCondition(self, ctx:FlowLangParser.ConditionContext):
        return ctx.getText()
