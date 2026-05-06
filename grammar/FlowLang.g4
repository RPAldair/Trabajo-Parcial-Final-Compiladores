grammar FlowLang;

root        : workflow+ EOF ;
workflow    : WORKFLOW ID LBRACE transition+ RBRACE ;
transition  : step ARROW step (IF NOT? condition)? ;
step        : ID | START | END ;
condition   : ID ;

WORKFLOW    : 'workflow' ;
IF          : 'if' ;
NOT         : 'not' ;
START       : 'start' ;
END         : 'end' ;
ARROW       : '->' ;
LBRACE      : '{' ;
RBRACE      : '}' ;
ID          : [a-zA-Z_][a-zA-Z0-9_]* ;
WS          : [ \t\r\n]+ -> skip ;
COMMENT     : '//' ~[\r\n]* -> skip ;