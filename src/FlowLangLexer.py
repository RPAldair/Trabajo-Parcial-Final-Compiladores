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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\r")
        buf.write("S\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\b")
        buf.write("\3\b\3\t\3\t\3\n\3\n\7\n=\n\n\f\n\16\n@\13\n\3\13\6\13")
        buf.write("C\n\13\r\13\16\13D\3\13\3\13\3\f\3\f\3\f\3\f\7\fM\n\f")
        buf.write("\f\f\16\fP\13\f\3\f\3\f\2\2\r\3\3\5\4\7\5\t\6\13\7\r\b")
        buf.write("\17\t\21\n\23\13\25\f\27\r\3\2\6\5\2C\\aac|\6\2\62;C\\")
        buf.write("aac|\5\2\13\f\17\17\"\"\4\2\f\f\17\17\2U\2\3\3\2\2\2\2")
        buf.write("\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3")
        buf.write("\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2")
        buf.write("\2\2\2\27\3\2\2\2\3\31\3\2\2\2\5\"\3\2\2\2\7%\3\2\2\2")
        buf.write("\t)\3\2\2\2\13/\3\2\2\2\r\63\3\2\2\2\17\66\3\2\2\2\21")
        buf.write("8\3\2\2\2\23:\3\2\2\2\25B\3\2\2\2\27H\3\2\2\2\31\32\7")
        buf.write("y\2\2\32\33\7q\2\2\33\34\7t\2\2\34\35\7m\2\2\35\36\7h")
        buf.write("\2\2\36\37\7n\2\2\37 \7q\2\2 !\7y\2\2!\4\3\2\2\2\"#\7")
        buf.write("k\2\2#$\7h\2\2$\6\3\2\2\2%&\7p\2\2&\'\7q\2\2\'(\7v\2\2")
        buf.write("(\b\3\2\2\2)*\7u\2\2*+\7v\2\2+,\7c\2\2,-\7t\2\2-.\7v\2")
        buf.write("\2.\n\3\2\2\2/\60\7g\2\2\60\61\7p\2\2\61\62\7f\2\2\62")
        buf.write("\f\3\2\2\2\63\64\7/\2\2\64\65\7@\2\2\65\16\3\2\2\2\66")
        buf.write("\67\7}\2\2\67\20\3\2\2\289\7\177\2\29\22\3\2\2\2:>\t\2")
        buf.write("\2\2;=\t\3\2\2<;\3\2\2\2=@\3\2\2\2><\3\2\2\2>?\3\2\2\2")
        buf.write("?\24\3\2\2\2@>\3\2\2\2AC\t\4\2\2BA\3\2\2\2CD\3\2\2\2D")
        buf.write("B\3\2\2\2DE\3\2\2\2EF\3\2\2\2FG\b\13\2\2G\26\3\2\2\2H")
        buf.write("I\7\61\2\2IJ\7\61\2\2JN\3\2\2\2KM\n\5\2\2LK\3\2\2\2MP")
        buf.write("\3\2\2\2NL\3\2\2\2NO\3\2\2\2OQ\3\2\2\2PN\3\2\2\2QR\b\f")
        buf.write("\2\2R\30\3\2\2\2\6\2>DN\3\b\2\2")
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
    ID = 9
    WS = 10
    COMMENT = 11

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'workflow'", "'if'", "'not'", "'start'", "'end'", "'->'", "'{'", 
            "'}'" ]

    symbolicNames = [ "<INVALID>",
            "WORKFLOW", "IF", "NOT", "START", "END", "ARROW", "LBRACE", 
            "RBRACE", "ID", "WS", "COMMENT" ]

    ruleNames = [ "WORKFLOW", "IF", "NOT", "START", "END", "ARROW", "LBRACE", 
                  "RBRACE", "ID", "WS", "COMMENT" ]

    grammarFileName = "FlowLang.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


