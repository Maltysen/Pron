import ply.yacc as yacc
import lexer
from pprint import pprint

tokens=lexer.tokens

precedence = (
	('left', 'PLUS'),
	('left', 'TIMES')
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
				 | expr'''
	p[0]=p[1]

def p_binary(p):
	'''expr : expr PLUS expr
			| expr TIMES expr'''
	if p[2]=='adds':
		p[0] = ('PLUS', p[1], p[3])
	if p[2]=='creams':
		p[0] = ('TIMES', p[1], p[3])

def p_literal(p):
	'''expr : INT'''
	p[0] = p[1]

def p_name(p):
	'''expr : NAME'''
	p[0] = ('NAME LOOKUP', p[1])

def p_assign(p):
	'''assign : NAME EQUALS expr'''
	p[0] = ('ASSIGN', p[1], p[3])

parser=yacc.yacc()

pprint(parser.parse('''abc pump 7 adds 8 creams 9
def pump 9 adds abc
'''), width=4)
