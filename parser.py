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

parser=yacc.yacc()

root = parser.parse('''
x pump 0
blow x dumps 10
	squirt x creams 5
	squirt "helloworld" lick x
	x pump x adds 1
facial

squirt""

consent 0 creams 10 yes
	squirt "b1"
just 1 yes
	squirt "b2"
rp
	squirt "else"
shot

squirt""

y pump 0
blow 1
	squirt y
	y pump y adds 1
	consent y dumps 5 yes
		"pass"
	rp
		consent 7 yes
			harder
		shot
	shot
	squirt"blah"
	consent y dumps 10 yes
		"pass"
	rp
		pop CHERRY
	shot
facial

squirt""

raw my_func (a, b, c)
	consent a yes
		thrust a adds b adds c
	rp thrust 2 creams (b adds c) shot
pull

a pump 7
squirt a
squirt my_func(1, 2, a) creams 3
squirt my_func(0, 10, 10)
squirt a
squirt""

squirt "end"
''')
nodes.env = {}
root.eval()
