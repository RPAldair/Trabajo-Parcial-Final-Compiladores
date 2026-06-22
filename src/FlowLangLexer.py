# Generated from grammar/FlowLang.g4 by ANTLR 4.9.3
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\33")
        buf.write("\u00ac\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5")
        buf.write("\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3")
        buf.write("\n\3\n\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3")
        buf.write("\16\3\16\3\16\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17")
        buf.write("\3\20\3\20\3\20\3\21\3\21\3\21\3\22\3\22\3\23\3\23\3\24")
        buf.write("\6\24|\n\24\r\24\16\24}\3\25\3\25\7\25\u0082\n\25\f\25")
        buf.write("\16\25\u0085\13\25\3\25\3\25\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\30\3\30\7\30\u0096\n")
        buf.write("\30\f\30\16\30\u0099\13\30\3\31\6\31\u009c\n\31\r\31\16")
        buf.write("\31\u009d\3\31\3\31\3\32\3\32\3\32\3\32\7\32\u00a6\n\32")
        buf.write("\f\32\16\32\u00a9\13\32\3\32\3\32\2\2\33\3\3\5\4\7\5\t")
        buf.write("\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20")
        buf.write("\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\3")
        buf.write("\2\b\3\2\62;\6\2\f\f\17\17$$^^\5\2C\\aac|\6\2\62;C\\a")
        buf.write("ac|\5\2\13\f\17\17\"\"\4\2\f\f\17\17\2\u00b0\2\3\3\2\2")
        buf.write("\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25")
        buf.write("\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3")
        buf.write("\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write("\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2")
        buf.write("\2\61\3\2\2\2\2\63\3\2\2\2\3\65\3\2\2\2\5>\3\2\2\2\7A")
        buf.write("\3\2\2\2\tE\3\2\2\2\13K\3\2\2\2\rO\3\2\2\2\17R\3\2\2\2")
        buf.write("\21T\3\2\2\2\23V\3\2\2\2\25Z\3\2\2\2\27\\\3\2\2\2\31a")
        buf.write("\3\2\2\2\33e\3\2\2\2\35l\3\2\2\2\37p\3\2\2\2!s\3\2\2\2")
        buf.write("#v\3\2\2\2%x\3\2\2\2\'{\3\2\2\2)\177\3\2\2\2+\u0088\3")
        buf.write("\2\2\2-\u008d\3\2\2\2/\u0093\3\2\2\2\61\u009b\3\2\2\2")
        buf.write("\63\u00a1\3\2\2\2\65\66\7y\2\2\66\67\7q\2\2\678\7t\2\2")
        buf.write("89\7m\2\29:\7h\2\2:;\7n\2\2;<\7q\2\2<=\7y\2\2=\4\3\2\2")
        buf.write("\2>?\7k\2\2?@\7h\2\2@\6\3\2\2\2AB\7p\2\2BC\7q\2\2CD\7")
        buf.write("v\2\2D\b\3\2\2\2EF\7u\2\2FG\7v\2\2GH\7c\2\2HI\7t\2\2I")
        buf.write("J\7v\2\2J\n\3\2\2\2KL\7g\2\2LM\7p\2\2MN\7f\2\2N\f\3\2")
        buf.write("\2\2OP\7/\2\2PQ\7@\2\2Q\16\3\2\2\2RS\7}\2\2S\20\3\2\2")
        buf.write("\2TU\7\177\2\2U\22\3\2\2\2VW\7x\2\2WX\7c\2\2XY\7t\2\2")
        buf.write("Y\24\3\2\2\2Z[\7<\2\2[\26\3\2\2\2\\]\7d\2\2]^\7q\2\2^")
        buf.write("_\7q\2\2_`\7n\2\2`\30\3\2\2\2ab\7k\2\2bc\7p\2\2cd\7v\2")
        buf.write("\2d\32\3\2\2\2ef\7u\2\2fg\7v\2\2gh\7t\2\2hi\7k\2\2ij\7")
        buf.write("p\2\2jk\7i\2\2k\34\3\2\2\2lm\7c\2\2mn\7p\2\2no\7f\2\2")
        buf.write("o\36\3\2\2\2pq\7q\2\2qr\7t\2\2r \3\2\2\2st\7?\2\2tu\7")
        buf.write("?\2\2u\"\3\2\2\2vw\7*\2\2w$\3\2\2\2xy\7+\2\2y&\3\2\2\2")
        buf.write("z|\t\2\2\2{z\3\2\2\2|}\3\2\2\2}{\3\2\2\2}~\3\2\2\2~(\3")
        buf.write("\2\2\2\177\u0083\7$\2\2\u0080\u0082\n\3\2\2\u0081\u0080")
        buf.write("\3\2\2\2\u0082\u0085\3\2\2\2\u0083\u0081\3\2\2\2\u0083")
        buf.write("\u0084\3\2\2\2\u0084\u0086\3\2\2\2\u0085\u0083\3\2\2\2")
        buf.write("\u0086\u0087\7$\2\2\u0087*\3\2\2\2\u0088\u0089\7v\2\2")
        buf.write("\u0089\u008a\7t\2\2\u008a\u008b\7w\2\2\u008b\u008c\7g")
        buf.write("\2\2\u008c,\3\2\2\2\u008d\u008e\7h\2\2\u008e\u008f\7c")
        buf.write("\2\2\u008f\u0090\7n\2\2\u0090\u0091\7u\2\2\u0091\u0092")
        buf.write("\7g\2\2\u0092.\3\2\2\2\u0093\u0097\t\4\2\2\u0094\u0096")
        buf.write("\t\5\2\2\u0095\u0094\3\2\2\2\u0096\u0099\3\2\2\2\u0097")
        buf.write("\u0095\3\2\2\2\u0097\u0098\3\2\2\2\u0098\60\3\2\2\2\u0099")
        buf.write("\u0097\3\2\2\2\u009a\u009c\t\6\2\2\u009b\u009a\3\2\2\2")
        buf.write("\u009c\u009d\3\2\2\2\u009d\u009b\3\2\2\2\u009d\u009e\3")
        buf.write("\2\2\2\u009e\u009f\3\2\2\2\u009f\u00a0\b\31\2\2\u00a0")
        buf.write("\62\3\2\2\2\u00a1\u00a2\7\61\2\2\u00a2\u00a3\7\61\2\2")
        buf.write("\u00a3\u00a7\3\2\2\2\u00a4\u00a6\n\7\2\2\u00a5\u00a4\3")
        buf.write("\2\2\2\u00a6\u00a9\3\2\2\2\u00a7\u00a5\3\2\2\2\u00a7\u00a8")
        buf.write("\3\2\2\2\u00a8\u00aa\3\2\2\2\u00a9\u00a7\3\2\2\2\u00aa")
        buf.write("\u00ab\b\32\2\2\u00ab\64\3\2\2\2\b\2}\u0083\u0097\u009d")
        buf.write("\u00a7\3\b\2\2")
        return buf.getvalue()


class FlowLangLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    WORKFLOW = 1
    IF = 2
    NOT = 3
    START = 4
    END = 5
    ARROW = 6
    LBRACE = 7
    RBRACE = 8
    VAR = 9
    COLON = 10
    BOOLTYPE = 11
    INTTYPE = 12
    STRINGTYPE = 13
    AND = 14
    OR = 15
    EQ = 16
    LPAREN = 17
    RPAREN = 18
    NUMBER = 19
    STRING = 20
    TRUE = 21
    FALSE = 22
    ID = 23
    WS = 24
    COMMENT = 25

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'workflow'", "'if'", "'not'", "'start'", "'end'", "'->'", "'{'", 
            "'}'", "'var'", "':'", "'bool'", "'int'", "'string'", "'and'", 
            "'or'", "'=='", "'('", "')'", "'true'", "'false'" ]

    symbolicNames = [ "<INVALID>",
            "WORKFLOW", "IF", "NOT", "START", "END", "ARROW", "LBRACE", 
            "RBRACE", "VAR", "COLON", "BOOLTYPE", "INTTYPE", "STRINGTYPE", 
            "AND", "OR", "EQ", "LPAREN", "RPAREN", "NUMBER", "STRING", "TRUE", 
            "FALSE", "ID", "WS", "COMMENT" ]

    ruleNames = [ "WORKFLOW", "IF", "NOT", "START", "END", "ARROW", "LBRACE", 
                  "RBRACE", "VAR", "COLON", "BOOLTYPE", "INTTYPE", "STRINGTYPE", 
                  "AND", "OR", "EQ", "LPAREN", "RPAREN", "NUMBER", "STRING", 
                  "TRUE", "FALSE", "ID", "WS", "COMMENT" ]

    grammarFileName = "FlowLang.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


