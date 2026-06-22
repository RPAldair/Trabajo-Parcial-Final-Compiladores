# Generated from grammar/FlowLang.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FlowLangParser import FlowLangParser
else:
    from FlowLangParser import FlowLangParser

# This class defines a complete generic visitor for a parse tree produced by FlowLangParser.

class FlowLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FlowLangParser#root.
    def visitRoot(self, ctx:FlowLangParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#workflow.
    def visitWorkflow(self, ctx:FlowLangParser.WorkflowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#transition.
    def visitTransition(self, ctx:FlowLangParser.TransitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#step.
    def visitStep(self, ctx:FlowLangParser.StepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#condition.
    def visitCondition(self, ctx:FlowLangParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#varDecl.
    def visitVarDecl(self, ctx:FlowLangParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#dataType.
    def visitDataType(self, ctx:FlowLangParser.DataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#expr.
    def visitExpr(self, ctx:FlowLangParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#orExpr.
    def visitOrExpr(self, ctx:FlowLangParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#andExpr.
    def visitAndExpr(self, ctx:FlowLangParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#notExpr.
    def visitNotExpr(self, ctx:FlowLangParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#comparison.
    def visitComparison(self, ctx:FlowLangParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlowLangParser#primary.
    def visitPrimary(self, ctx:FlowLangParser.PrimaryContext):
        return self.visitChildren(ctx)



del FlowLangParser