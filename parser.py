import ply.yacc as yacc
import lexer
from pprint import pprint
from nodes import *
import nodes
from funcs import *
import argparse

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
				 | setitem
				 | print
				 | return
				 | break
				 | continue
				 | while
				 | expr
				 | if
				 | funcdef'''
	p[0]=p[1]

def p_if_chain(p):
	'''if_chain : if_chain ELIF expr STARTIF block
				| IF expr STARTIF block'''

	if len(p)==5:
		p[0] = If_Chain((p[2], p[4]))

	else:
		p[1].append_child((p[3], p[5]))
		p[0] = p[1]

def p_else(p):
	'''else : ELSE block ENDIF'''
	p[0] = (Literal(True), p[2])

def p_if(p):
	'''if : if_chain ENDIF
		  | if_chain else'''
	if p[2]!='ENDIF':
		p[1].append_child(p[2])
	p[0] = p[1]

def p_while(p):
	'''while : WHILE expr block ENDWHILE'''
	p[0] = While(p[2], p[3])

def p_return(p):
	'''return : RETURN expr'''
	p[0] = Return(p[2])

def p_break(p):
	'''break : BREAK1 BREAK2'''
	p[0] = Literal(BREAK)

def p_continue(p):
	'''continue : CONTINUE'''
	p[0] = Literal(CONTINUE)

def p_print(p):
	'''print : PRINT expr'''
	p[0] = Unary(operators[p[1]], p[2])

def p_binary(p):
	'''expr : expr PLUS expr
			| expr MINUS expr
			| expr INDEX expr
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

def p_setitem(p):
	'''setitem : expr INDEX expr EQUALS expr'''
	p[0] = Setitem(p[1], p[3], p[5])

def p_val_seq(p):
	'''valseq : valseq COMMA expr
			  | expr'''

	if len(p)==2:
		p[0] = p[1],

	else:
		p[1] += p[3],
		p[0] = p[1]

def p_name_seq(p):
	'''nameseq : nameseq COMMA NAME
			   | NAME'''

	if len(p)==2:
		p[0] = p[1],

	else:
		p[1] += p[3],
		p[0] = p[1]

def p_funcdef(p):
	'''funcdef : FUNC NAME LPAREN nameseq RPAREN block ENDFUNC'''
	p[0] = Funcdef(p[2], p[4], p[6])

def p_call(p):
	'''expr : expr LPAREN valseq RPAREN'''
	p[0] = Call(p[1], p[3])

def p_error(p):
	raise SyntaxError("Invalid Syntax")

def run(code):
	parser=yacc.yacc(errorlog=yacc.NullLogger())
	root = parser.parse(code)
	
	nodes.env = {}
	root.eval()

if __name__=='__main__':
	parser = argparse.ArgumentParser(description = 'XXX version 0.9 interpreter. Made by perverts, for perverts.')

	parser.add_argument('file', type=argparse.FileType('r'), help='Input file with code to run.')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.9')

	args = parser.parse_args()
	run(args.file.read())
