# FlowLangCustomVisitor.py
# Recorre el arbol sintactico producido por FlowLangParser usando el patron
# Visitor de ANTLR4 y construye la representacion intermedia (model.Workflow):
# nombre del workflow, variables tipadas, transiciones y arboles de expresion
# de las condiciones de guardia. Esta IR es la entrada de todos los backends.
from exprs import (
    VariableExpr,
    LiteralExpr,
    EqualExpr,
    AndExpr,
    OrExpr,
    NotExpr,
)
from model import Workflow, Transition

if __name__ is not None and "." in __name__:
    from .FlowLangParser import FlowLangParser
    from .FlowLangVisitor import FlowLangVisitor
else:
    from FlowLangParser import FlowLangParser
    from FlowLangVisitor import FlowLangVisitor


class FlowLangCustomVisitor(FlowLangVisitor):
    """Construye la lista de workflows recorriendo el arbol con el Visitor."""

    def __init__(self):
        self.workflows = []

    # root : workflow+ EOF ;
    def visitRoot(self, ctx: FlowLangParser.RootContext):
        for workflow_ctx in ctx.workflow():
            self.workflows.append(self.visit(workflow_ctx))
        return self.workflows

    # workflow : WORKFLOW ID LBRACE varDecl* transition+ RBRACE ;
    def visitWorkflow(self, ctx: FlowLangParser.WorkflowContext):
        workflow = Workflow(ctx.ID().getText(), line=ctx.start.line)
        for var_ctx in ctx.varDecl():
            workflow.variables.append(self.visit(var_ctx))
        for transition_ctx in ctx.transition():
            workflow.transiciones.append(self.visit(transition_ctx))
        return workflow

    # varDecl : VAR ID COLON dataType ;
    def visitVarDecl(self, ctx: FlowLangParser.VarDeclContext):
        return (ctx.ID().getText(), ctx.dataType().getText(), ctx.start.line)

    # transition : step ARROW step (IF condition)? ;
    def visitTransition(self, ctx: FlowLangParser.TransitionContext):
        origen = self.visit(ctx.step(0))
        destino = self.visit(ctx.step(1))
        condicion = None
        if ctx.IF() is not None:
            condicion = self.visit(ctx.condition())
        return Transition(origen, destino, condicion, line=ctx.start.line)

    # step : ID | START | END ;
    def visitStep(self, ctx: FlowLangParser.StepContext):
        return ctx.getText()

    # condition : expr ;
    def visitCondition(self, ctx: FlowLangParser.ConditionContext):
        return self.visit(ctx.expr())

    # expr : orExpr ;
    def visitExpr(self, ctx):
        return self.visit(ctx.orExpr())

    # orExpr : andExpr (OR andExpr)* ;   (asociatividad izquierda)
    def visitOrExpr(self, ctx):
        exprs = [self.visit(x) for x in ctx.andExpr()]
        result = exprs[0]
        for e in exprs[1:]:
            result = OrExpr(result, e)
        return result

    # andExpr : notExpr (AND notExpr)* ;  (asociatividad izquierda)
    def visitAndExpr(self, ctx):
        exprs = [self.visit(x) for x in ctx.notExpr()]
        result = exprs[0]
        for e in exprs[1:]:
            result = AndExpr(result, e)
        return result

    # notExpr : NOT notExpr | comparison ;
    def visitNotExpr(self, ctx):
        if ctx.NOT():
            return NotExpr(self.visit(ctx.notExpr()))
        return self.visit(ctx.comparison())

    # comparison : primary (EQ primary)? ;
    def visitComparison(self, ctx):
        left = self.visit(ctx.primary(0))
        if ctx.EQ():
            right = self.visit(ctx.primary(1))
            return EqualExpr(left, right)
        return left

    # primary : ID | NUMBER | STRING | TRUE | FALSE | LPAREN expr RPAREN ;
    def visitPrimary(self, ctx):
        if ctx.ID():
            return VariableExpr(ctx.ID().getText())
        if ctx.NUMBER():
            return LiteralExpr(int(ctx.NUMBER().getText()), "int")
        if ctx.STRING():
            return LiteralExpr(ctx.STRING().getText()[1:-1], "string")
        if ctx.TRUE():
            return LiteralExpr(True, "bool")
        if ctx.FALSE():
            return LiteralExpr(False, "bool")
        return self.visit(ctx.expr())
