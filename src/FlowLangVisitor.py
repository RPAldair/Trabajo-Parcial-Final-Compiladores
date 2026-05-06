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



del FlowLangParser