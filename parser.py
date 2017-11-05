import ply.yacc as yacc
import lexer
from pprint import pprint
from nodes import *
import nodes
from funcs import *

tokens=lexer.tokens

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES'),
	('left', 'INDEX')
)

def p_block(p):
	'''block : block statement
			 | statement'''
	if len(p)==3:
		p[1].append_child(p[2])
		p[0] = p[1]
	else:
		p[0] = Block(p[1])

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
	p[0] = While(p[2], p[3])

def p_funcdef(p):
	'''funcdef : FUNC block ENDFUNC'''
	p[0] = ('FUNCDEF', p[2])

def p_return(p):
	'''return : RETURN expr'''
	p[0] = ('RETURN', p[2])

def p_print(p):
	'''print : PRINT expr'''
	p[0] = Unary(operators[p[1]], p[2])

def p_binary(p):
	'''expr : expr PLUS expr
			| expr MINUS expr
			| expr TIMES expr'''
	p[0] = Binary(operators[p[2]], p[1], p[3])

def p_literal(p):
	'''expr : INT
			| FLOAT
			| STRING'''
	p[0] = Literal(p[1][1:-1]if isinstance(p[1], str) else p[1])

def p_parens(p):
	'''expr : LPAREN expr RPAREN'''
	p[0] = p[2]

def p_name(p):
	'''expr : NAME'''
	p[0] = Symbol_Lookup(p[1])

def p_assign(p):
	'''assign : NAME EQUALS expr'''
	p[0] = Assign(p[1], p[3])

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

root = parser.parse('''
x pump 0 minus 10
blow x
squirt (x adds 10) creams 5
x pump x adds 1
facial''')
nodes.env = {}
root.eval()
