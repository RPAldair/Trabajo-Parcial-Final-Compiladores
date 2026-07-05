grammar FlowLang;

root        : workflow+ EOF ;
workflow    : WORKFLOW ID LBRACE varDecl* transition+ RBRACE ;
transition  : step ARROW step (IF condition)? ;
step        : ID | START | END ;
condition   : expr ;

varDecl     : VAR ID COLON dataType ;
dataType        : BOOLTYPE | INTTYPE | STRINGTYPE ;

expr        : orExpr ;
orExpr      : andExpr (OR andExpr)* ;
andExpr     : notExpr (AND notExpr)* ;
notExpr     : NOT notExpr | comparison ;
comparison  : primary (EQ primary)? ;
primary     : ID
			| NUMBER
			| STRING
			| TRUE
			| FALSE
			| LPAREN expr RPAREN
			;

WORKFLOW    : 'workflow' ;
IF          : 'if' ;
NOT         : 'not' ;
START       : 'start' ;
END         : 'end' ;
ARROW       : '->' ;
LBRACE      : '{' ;
RBRACE      : '}' ;
VAR         : 'var' ;
COLON       : ':' ;
BOOLTYPE    : 'bool' ;
INTTYPE     : 'int' ;
STRINGTYPE  : 'string' ;
AND         : 'and' ;
OR          : 'or' ;
EQ          : '==' ;
LPAREN      : '(' ;
RPAREN      : ')' ;
NUMBER      : [0-9]+ ;
STRING      : '"' (~["\\\r\n])* '"' ;
TRUE        : 'true' ;
FALSE       : 'false' ;

ID          : [a-zA-Z_][a-zA-Z0-9_]* ;
WS          : [ \t\r\n]+ -> skip ;
COMMENT     : '//' ~[\r\n]* -> skip ;




