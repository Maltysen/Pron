import ply.lex as lex


t_ignore = ' \t'

reserved = {
	'adds': 'PLUS',
	'creams': 'TIMES',
	'pump': 'EQUALS'
}

tokens = ['NAME', 'INT', 'newline'] + list(reserved.values())
t_ignore_COMMENT = r'sleep.*'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')
    return t

lexer = lex.lex()
