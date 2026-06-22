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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\33")
        buf.write("m\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16\t")
        buf.write("\16\3\2\6\2\36\n\2\r\2\16\2\37\3\2\3\2\3\3\3\3\3\3\3\3")
        buf.write("\7\3(\n\3\f\3\16\3+\13\3\3\3\6\3.\n\3\r\3\16\3/\3\3\3")
        buf.write("\3\3\4\3\4\3\4\3\4\3\4\5\49\n\4\3\5\3\5\3\6\3\6\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\n\7\nK\n\n\f")
        buf.write("\n\16\nN\13\n\3\13\3\13\3\13\7\13S\n\13\f\13\16\13V\13")
        buf.write("\13\3\f\3\f\3\f\5\f[\n\f\3\r\3\r\3\r\5\r`\n\r\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16k\n\16\3\16\2")
        buf.write("\2\17\2\4\6\b\n\f\16\20\22\24\26\30\32\2\4\4\2\6\7\31")
        buf.write("\31\3\2\r\17\2l\2\35\3\2\2\2\4#\3\2\2\2\6\63\3\2\2\2\b")
        buf.write(":\3\2\2\2\n<\3\2\2\2\f>\3\2\2\2\16C\3\2\2\2\20E\3\2\2")
        buf.write("\2\22G\3\2\2\2\24O\3\2\2\2\26Z\3\2\2\2\30\\\3\2\2\2\32")
        buf.write("j\3\2\2\2\34\36\5\4\3\2\35\34\3\2\2\2\36\37\3\2\2\2\37")
        buf.write("\35\3\2\2\2\37 \3\2\2\2 !\3\2\2\2!\"\7\2\2\3\"\3\3\2\2")
        buf.write("\2#$\7\3\2\2$%\7\31\2\2%)\7\t\2\2&(\5\f\7\2\'&\3\2\2\2")
        buf.write("(+\3\2\2\2)\'\3\2\2\2)*\3\2\2\2*-\3\2\2\2+)\3\2\2\2,.")
        buf.write("\5\6\4\2-,\3\2\2\2./\3\2\2\2/-\3\2\2\2/\60\3\2\2\2\60")
        buf.write("\61\3\2\2\2\61\62\7\n\2\2\62\5\3\2\2\2\63\64\5\b\5\2\64")
        buf.write("\65\7\b\2\2\658\5\b\5\2\66\67\7\4\2\2\679\5\n\6\28\66")
        buf.write("\3\2\2\289\3\2\2\29\7\3\2\2\2:;\t\2\2\2;\t\3\2\2\2<=\5")
        buf.write("\20\t\2=\13\3\2\2\2>?\7\13\2\2?@\7\31\2\2@A\7\f\2\2AB")
        buf.write("\5\16\b\2B\r\3\2\2\2CD\t\3\2\2D\17\3\2\2\2EF\5\22\n\2")
        buf.write("F\21\3\2\2\2GL\5\24\13\2HI\7\21\2\2IK\5\24\13\2JH\3\2")
        buf.write("\2\2KN\3\2\2\2LJ\3\2\2\2LM\3\2\2\2M\23\3\2\2\2NL\3\2\2")
        buf.write("\2OT\5\26\f\2PQ\7\20\2\2QS\5\26\f\2RP\3\2\2\2SV\3\2\2")
        buf.write("\2TR\3\2\2\2TU\3\2\2\2U\25\3\2\2\2VT\3\2\2\2WX\7\5\2\2")
        buf.write("X[\5\26\f\2Y[\5\30\r\2ZW\3\2\2\2ZY\3\2\2\2[\27\3\2\2\2")
        buf.write("\\_\5\32\16\2]^\7\22\2\2^`\5\32\16\2_]\3\2\2\2_`\3\2\2")
        buf.write("\2`\31\3\2\2\2ak\7\31\2\2bk\7\25\2\2ck\7\26\2\2dk\7\27")
        buf.write("\2\2ek\7\30\2\2fg\7\23\2\2gh\5\20\t\2hi\7\24\2\2ik\3\2")
        buf.write("\2\2ja\3\2\2\2jb\3\2\2\2jc\3\2\2\2jd\3\2\2\2je\3\2\2\2")
        buf.write("jf\3\2\2\2k\33\3\2\2\2\13\37)/8LTZ_j")
        return buf.getvalue()


class FlowLangParser ( Parser ):

    grammarFileName = "FlowLang.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'workflow'", "'if'", "'not'", "'start'", 
                     "'end'", "'->'", "'{'", "'}'", "'var'", "':'", "'bool'", 
                     "'int'", "'string'", "'and'", "'or'", "'=='", "'('", 
                     "')'", "<INVALID>", "<INVALID>", "'true'", "'false'" ]

    symbolicNames = [ "<INVALID>", "WORKFLOW", "IF", "NOT", "START", "END", 
                      "ARROW", "LBRACE", "RBRACE", "VAR", "COLON", "BOOLTYPE", 
                      "INTTYPE", "STRINGTYPE", "AND", "OR", "EQ", "LPAREN", 
                      "RPAREN", "NUMBER", "STRING", "TRUE", "FALSE", "ID", 
                      "WS", "COMMENT" ]

    RULE_root = 0
    RULE_workflow = 1
    RULE_transition = 2
    RULE_step = 3
    RULE_condition = 4
    RULE_varDecl = 5
    RULE_dataType = 6
    RULE_expr = 7
    RULE_orExpr = 8
    RULE_andExpr = 9
    RULE_notExpr = 10
    RULE_comparison = 11
    RULE_primary = 12

    ruleNames =  [ "root", "workflow", "transition", "step", "condition", 
                   "varDecl", "dataType", "expr", "orExpr", "andExpr", "notExpr", 
                   "comparison", "primary" ]

    EOF = Token.EOF
    WORKFLOW=1
    IF=2
    NOT=3
    START=4
    END=5
    ARROW=6
    LBRACE=7
    RBRACE=8
    VAR=9
    COLON=10
    BOOLTYPE=11
    INTTYPE=12
    STRINGTYPE=13
    AND=14
    OR=15
    EQ=16
    LPAREN=17
    RPAREN=18
    NUMBER=19
    STRING=20
    TRUE=21
    FALSE=22
    ID=23
    WS=24
    COMMENT=25

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
            self.state = 27 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 26
                self.workflow()
                self.state = 29 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==FlowLangParser.WORKFLOW):
                    break

            self.state = 31
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

        def varDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FlowLangParser.VarDeclContext)
            else:
                return self.getTypedRuleContext(FlowLangParser.VarDeclContext,i)


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
            self.state = 33
            self.match(FlowLangParser.WORKFLOW)
            self.state = 34
            self.match(FlowLangParser.ID)
            self.state = 35
            self.match(FlowLangParser.LBRACE)
            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==FlowLangParser.VAR:
                self.state = 36
                self.varDecl()
                self.state = 41
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 43 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 42
                self.transition()
                self.state = 45 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << FlowLangParser.START) | (1 << FlowLangParser.END) | (1 << FlowLangParser.ID))) != 0)):
                    break

            self.state = 47
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
            self.state = 49
            self.step()
            self.state = 50
            self.match(FlowLangParser.ARROW)
            self.state = 51
            self.step()
            self.state = 54
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==FlowLangParser.IF:
                self.state = 52
                self.match(FlowLangParser.IF)
                self.state = 53
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
            self.state = 56
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

        def expr(self):
            return self.getTypedRuleContext(FlowLangParser.ExprContext,0)


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
            self.state = 58
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(FlowLangParser.VAR, 0)

        def ID(self):
            return self.getToken(FlowLangParser.ID, 0)

        def COLON(self):
            return self.getToken(FlowLangParser.COLON, 0)

        def dataType(self):
            return self.getTypedRuleContext(FlowLangParser.DataTypeContext,0)


        def getRuleIndex(self):
            return FlowLangParser.RULE_varDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDecl" ):
                return visitor.visitVarDecl(self)
            else:
                return visitor.visitChildren(self)




    def varDecl(self):

        localctx = FlowLangParser.VarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_varDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(FlowLangParser.VAR)
            self.state = 61
            self.match(FlowLangParser.ID)
            self.state = 62
            self.match(FlowLangParser.COLON)
            self.state = 63
            self.dataType()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DataTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOLTYPE(self):
            return self.getToken(FlowLangParser.BOOLTYPE, 0)

        def INTTYPE(self):
            return self.getToken(FlowLangParser.INTTYPE, 0)

        def STRINGTYPE(self):
            return self.getToken(FlowLangParser.STRINGTYPE, 0)

        def getRuleIndex(self):
            return FlowLangParser.RULE_dataType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDataType" ):
                return visitor.visitDataType(self)
            else:
                return visitor.visitChildren(self)




    def dataType(self):

        localctx = FlowLangParser.DataTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_dataType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << FlowLangParser.BOOLTYPE) | (1 << FlowLangParser.INTTYPE) | (1 << FlowLangParser.STRINGTYPE))) != 0)):
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


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def orExpr(self):
            return self.getTypedRuleContext(FlowLangParser.OrExprContext,0)


        def getRuleIndex(self):
            return FlowLangParser.RULE_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = FlowLangParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.orExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def andExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FlowLangParser.AndExprContext)
            else:
                return self.getTypedRuleContext(FlowLangParser.AndExprContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(FlowLangParser.OR)
            else:
                return self.getToken(FlowLangParser.OR, i)

        def getRuleIndex(self):
            return FlowLangParser.RULE_orExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)




    def orExpr(self):

        localctx = FlowLangParser.OrExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_orExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.andExpr()
            self.state = 74
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==FlowLangParser.OR:
                self.state = 70
                self.match(FlowLangParser.OR)
                self.state = 71
                self.andExpr()
                self.state = 76
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def notExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FlowLangParser.NotExprContext)
            else:
                return self.getTypedRuleContext(FlowLangParser.NotExprContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(FlowLangParser.AND)
            else:
                return self.getToken(FlowLangParser.AND, i)

        def getRuleIndex(self):
            return FlowLangParser.RULE_andExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)




    def andExpr(self):

        localctx = FlowLangParser.AndExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_andExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.notExpr()
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==FlowLangParser.AND:
                self.state = 78
                self.match(FlowLangParser.AND)
                self.state = 79
                self.notExpr()
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NotExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(FlowLangParser.NOT, 0)

        def notExpr(self):
            return self.getTypedRuleContext(FlowLangParser.NotExprContext,0)


        def comparison(self):
            return self.getTypedRuleContext(FlowLangParser.ComparisonContext,0)


        def getRuleIndex(self):
            return FlowLangParser.RULE_notExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotExpr" ):
                return visitor.visitNotExpr(self)
            else:
                return visitor.visitChildren(self)




    def notExpr(self):

        localctx = FlowLangParser.NotExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_notExpr)
        try:
            self.state = 88
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FlowLangParser.NOT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 85
                self.match(FlowLangParser.NOT)
                self.state = 86
                self.notExpr()
                pass
            elif token in [FlowLangParser.LPAREN, FlowLangParser.NUMBER, FlowLangParser.STRING, FlowLangParser.TRUE, FlowLangParser.FALSE, FlowLangParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.comparison()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FlowLangParser.PrimaryContext)
            else:
                return self.getTypedRuleContext(FlowLangParser.PrimaryContext,i)


        def EQ(self):
            return self.getToken(FlowLangParser.EQ, 0)

        def getRuleIndex(self):
            return FlowLangParser.RULE_comparison

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = FlowLangParser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.primary()
            self.state = 93
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==FlowLangParser.EQ:
                self.state = 91
                self.match(FlowLangParser.EQ)
                self.state = 92
                self.primary()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(FlowLangParser.ID, 0)

        def NUMBER(self):
            return self.getToken(FlowLangParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(FlowLangParser.STRING, 0)

        def TRUE(self):
            return self.getToken(FlowLangParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(FlowLangParser.FALSE, 0)

        def LPAREN(self):
            return self.getToken(FlowLangParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(FlowLangParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(FlowLangParser.RPAREN, 0)

        def getRuleIndex(self):
            return FlowLangParser.RULE_primary

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimary" ):
                return visitor.visitPrimary(self)
            else:
                return visitor.visitChildren(self)




    def primary(self):

        localctx = FlowLangParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_primary)
        try:
            self.state = 104
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FlowLangParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 95
                self.match(FlowLangParser.ID)
                pass
            elif token in [FlowLangParser.NUMBER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 96
                self.match(FlowLangParser.NUMBER)
                pass
            elif token in [FlowLangParser.STRING]:
                self.enterOuterAlt(localctx, 3)
                self.state = 97
                self.match(FlowLangParser.STRING)
                pass
            elif token in [FlowLangParser.TRUE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 98
                self.match(FlowLangParser.TRUE)
                pass
            elif token in [FlowLangParser.FALSE]:
                self.enterOuterAlt(localctx, 5)
                self.state = 99
                self.match(FlowLangParser.FALSE)
                pass
            elif token in [FlowLangParser.LPAREN]:
                self.enterOuterAlt(localctx, 6)
                self.state = 100
                self.match(FlowLangParser.LPAREN)
                self.state = 101
                self.expr()
                self.state = 102
                self.match(FlowLangParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





