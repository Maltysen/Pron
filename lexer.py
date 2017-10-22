import ply.lex as lex
from ast import literal_eval

t_ignore = ' \t'

reserved = {
	'adds': 'PLUS',
	'creams': 'TIMES',
	'pump': 'EQUALS',
	'squirt': 'PRINT',
	'blow': 'WHILE',
	'facial': 'ENDWHILE',
	'consent': 'IF',
	'rp': 'ELSE',
	'shot': 'ENDIF',
	'raw': 'FUNC',
	'pull': 'ENDFUNC',
	'lick': 'INDEX',
	'yes': 'STARTIF',
	'thrust': 'RETURN'
}

tokens = ['NAME', 'INT', 'FLOAT', 'STRING', 'COMMA', 'LPAREN', 'RPAREN', 'newline'] + list(reserved.values())
t_ignore_COMMENT = r'sleep.*' #TODO: Fix
t_COMMA = ','
t_LPAREN = '\('
t_RPAREN = '\)'
t_STRING='("(?:[^"\\\\]|\\\\.)*"|'+"'(?:[^'\\\\]|\\\\.)*')" # TODO: make better

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_FLOAT(t):
	r'((\d+\.\d+|\.\d+|\d+\.)([eE]-?\d+)?)|\d+[eE]-?\d+'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value.lower(), 'NAME')
	t.value = t.value if t.type=='NAME' else t.type
	return t

lexer = lex.lex()
