import ply.yacc as yacc
import lexer
from pprint import pprint

tokens=lexer.tokens

precedence = (
	('left', 'PLUS'),
	('left', 'TIMES'),
	('left', 'INDEX')
)

def p_block(p):
	'''block : block statement
			 | statement'''
	if len(p)==3:
		p[0] = p[1] + (p[2],)
	else:
		p[0] = ('BLOCK', p[1])

def p_statement(p):
	'''statement : assign
				 | print
				 | return
				 | while
				 | expr
				 | if
				 | funcdef'''
	p[0]=p[1]

def p_ifcond(p):
	'''ifcond : IF expr STARTIF'''
	p[0] = p[2]

def p_if(p):
	'''if : ifcond block ENDIF
		  | ifcond block if
		  | ifcond block else'''
	p[0] = ('IF', p[1], p[2])
	if p[3]!='ENDIF': p[0]+=(p[3],)

def p_else(p):
	'''else : ELSE block ENDIF'''
	p[0] = p[2]

def p_while(p):
	'''while : WHILE expr block ENDWHILE'''
	p[0] = ('WHILE', p[2], p[3])

def p_funcdef(p):
	'''funcdef : FUNC block ENDFUNC'''
	p[0] = ('FUNCDEF', p[2])

def p_return(p):
	'''return : RETURN expr'''
	p[0] = ('RETURN', p[2])

def p_print(p):
	'''print : PRINT expr'''
	p[0] = ('PRINT', p[2])

def p_binary(p):
	'''expr : expr PLUS expr
			| expr TIMES expr'''
	if p[2]=='PLUS':
		p[0] = ('PLUS', p[1], p[3])
	if p[2]=='TIMES':
		p[0] = ('TIMES', p[1], p[3])

def p_literal(p):
	'''expr : INT
			| FLOAT
			| STRING'''
	p[0] = p[1][1:-1]if isinstance(p[1], str) else p[1]

def p_parens(p):
	'''expr : LPAREN expr RPAREN'''
	p[0] = p[2]

def p_name(p):
	'''expr : NAME'''
	p[0] = ('SYMBOL_LOOKUP', p[1])

def p_assign(p):
	'''assign : NAME EQUALS expr'''
	p[0] = ('ASSIGN', p[1], p[3])

def p_getitem(p):
	'''getitem : expr INDEX expr'''
	p[0] = ('GETITEM', p[1], p[3])

def p_expr_getitem(p):
	'''expr : getitem'''
	p[0] = p[1]

def p_setitem(p):
	'''setitem : expr INDEX expr EQUALS expr'''
	p[0] = ('SETITEM', p[1], p[3], p[5])

parser=yacc.yacc()

pprint(parser.parse('''abc pump (.7E-2 adds 8) creams 9
def pump 9 adds abc
x pump 0
BLOW x
	x pump x adds 1
	squirt'hello how are you '
FACIal
consent 0 yes
SQUIRT 4
consent 1 yes
SQUIRT 5
rp
SQUIRT 7
shot
'''), width=4)
