import ply.lex as lex

tokens = (
    'INT', 'ID', 'NUM', 'ASSIGN', 'PLUS', 'MUL', 'SEMI', 'WHILE', 'DO', 'ENDDO', 'ENDWHILE', 'LPAREN', 'RPAREN'
)

t_ASSIGN = r'='
t_PLUS = r'\+'
t_MUL = r'\*'
t_SEMI = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_INT(t):
    r'int'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_ENDDO(t):
    r'enddo'
    return t

def t_ENDWHILE(t):
    r'endwhile'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
