# Generated from grammar/FlowLang.g4 by ANTLR 4.9.3
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\r")
        buf.write(",\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\6\2\16\n")
        buf.write("\2\r\2\16\2\17\3\2\3\2\3\3\3\3\3\3\3\3\6\3\30\n\3\r\3")
        buf.write("\16\3\31\3\3\3\3\3\4\3\4\3\4\3\4\3\4\5\4#\n\4\3\4\5\4")
        buf.write("&\n\4\3\5\3\5\3\6\3\6\3\6\2\2\7\2\4\6\b\n\2\3\4\2\6\7")
        buf.write("\13\13\2*\2\r\3\2\2\2\4\23\3\2\2\2\6\35\3\2\2\2\b\'\3")
        buf.write("\2\2\2\n)\3\2\2\2\f\16\5\4\3\2\r\f\3\2\2\2\16\17\3\2\2")
        buf.write("\2\17\r\3\2\2\2\17\20\3\2\2\2\20\21\3\2\2\2\21\22\7\2")
        buf.write("\2\3\22\3\3\2\2\2\23\24\7\3\2\2\24\25\7\13\2\2\25\27\7")
        buf.write("\t\2\2\26\30\5\6\4\2\27\26\3\2\2\2\30\31\3\2\2\2\31\27")
        buf.write("\3\2\2\2\31\32\3\2\2\2\32\33\3\2\2\2\33\34\7\n\2\2\34")
        buf.write("\5\3\2\2\2\35\36\5\b\5\2\36\37\7\b\2\2\37%\5\b\5\2 \"")
        buf.write("\7\4\2\2!#\7\5\2\2\"!\3\2\2\2\"#\3\2\2\2#$\3\2\2\2$&\5")
        buf.write("\n\6\2% \3\2\2\2%&\3\2\2\2&\7\3\2\2\2\'(\t\2\2\2(\t\3")
        buf.write("\2\2\2)*\7\13\2\2*\13\3\2\2\2\6\17\31\"%")
        return buf.getvalue()


class FlowLangParser ( Parser ):

    grammarFileName = "FlowLang.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'workflow'", "'if'", "'not'", "'start'", 
                     "'end'", "'->'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>", "WORKFLOW", "IF", "NOT", "START", "END", 
                      "ARROW", "LBRACE", "RBRACE", "ID", "WS", "COMMENT" ]

    RULE_root = 0
    RULE_workflow = 1
    RULE_transition = 2
    RULE_step = 3
    RULE_condition = 4

    ruleNames =  [ "root", "workflow", "transition", "step", "condition" ]

    EOF = Token.EOF
    WORKFLOW=1
    IF=2
    NOT=3
    START=4
    END=5
    ARROW=6
    LBRACE=7
    RBRACE=8
    ID=9
    WS=10
    COMMENT=11

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(FlowLangParser.EOF, 0)

        def workflow(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FlowLangParser.WorkflowContext)
            else:
                return self.getTypedRuleContext(FlowLangParser.WorkflowContext,i)


        def getRuleIndex(self):
            return FlowLangParser.RULE_root

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = FlowLangParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 10
                self.workflow()
                self.state = 13 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==FlowLangParser.WORKFLOW):
                    break

            self.state = 15
            self.match(FlowLangParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WorkflowContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORKFLOW(self):
            return self.getToken(FlowLangParser.WORKFLOW, 0)

        def ID(self):
            return self.getToken(FlowLangParser.ID, 0)

        def LBRACE(self):
            return self.getToken(FlowLangParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(FlowLangParser.RBRACE, 0)

        def transition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FlowLangParser.TransitionContext)
            else:
                return self.getTypedRuleContext(FlowLangParser.TransitionContext,i)


        def getRuleIndex(self):
            return FlowLangParser.RULE_workflow

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWorkflow" ):
                return visitor.visitWorkflow(self)
            else:
                return visitor.visitChildren(self)




    def workflow(self):

        localctx = FlowLangParser.WorkflowContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_workflow)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.match(FlowLangParser.WORKFLOW)
            self.state = 18
            self.match(FlowLangParser.ID)
            self.state = 19
            self.match(FlowLangParser.LBRACE)
            self.state = 21 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 20
                self.transition()
                self.state = 23 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << FlowLangParser.START) | (1 << FlowLangParser.END) | (1 << FlowLangParser.ID))) != 0)):
                    break

            self.state = 25
            self.match(FlowLangParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def step(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FlowLangParser.StepContext)
            else:
                return self.getTypedRuleContext(FlowLangParser.StepContext,i)


        def ARROW(self):
            return self.getToken(FlowLangParser.ARROW, 0)

        def IF(self):
            return self.getToken(FlowLangParser.IF, 0)

        def condition(self):
            return self.getTypedRuleContext(FlowLangParser.ConditionContext,0)


        def NOT(self):
            return self.getToken(FlowLangParser.NOT, 0)

        def getRuleIndex(self):
            return FlowLangParser.RULE_transition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTransition" ):
                return visitor.visitTransition(self)
            else:
                return visitor.visitChildren(self)




    def transition(self):

        localctx = FlowLangParser.TransitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_transition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.step()
            self.state = 28
            self.match(FlowLangParser.ARROW)
            self.state = 29
            self.step()
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==FlowLangParser.IF:
                self.state = 30
                self.match(FlowLangParser.IF)
                self.state = 32
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==FlowLangParser.NOT:
                    self.state = 31
                    self.match(FlowLangParser.NOT)


                self.state = 34
                self.condition()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(FlowLangParser.ID, 0)

        def START(self):
            return self.getToken(FlowLangParser.START, 0)

        def END(self):
            return self.getToken(FlowLangParser.END, 0)

        def getRuleIndex(self):
            return FlowLangParser.RULE_step

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStep" ):
                return visitor.visitStep(self)
            else:
                return visitor.visitChildren(self)




    def step(self):

        localctx = FlowLangParser.StepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_step)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << FlowLangParser.START) | (1 << FlowLangParser.END) | (1 << FlowLangParser.ID))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(FlowLangParser.ID, 0)

        def getRuleIndex(self):
            return FlowLangParser.RULE_condition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondition" ):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)




    def condition(self):

        localctx = FlowLangParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(FlowLangParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





