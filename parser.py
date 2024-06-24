import ply.yacc as yacc
from lexer import tokens

class Node:
    def __init__(self, type, children=None, value=None, lineno=0):
        self.type = type
        self.children = children if children is not None else []
        self.value = value
        self.lineno = lineno

def p_program(p):
    '''program : statement_list'''
    p[0] = Node('program', p[1], lineno=p.lineno(1))

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]
    p[0][0].lineno = p.lineno(1)

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | loop'''
    p[0] = p[1]
    p[0].lineno = p.lineno(1)

def p_declaration(p):
    '''declaration : INT ID ASSIGN NUM SEMI'''
    p[0] = Node('declaration', [p[2], p[4]], lineno=p.lineno(1))

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI'''
    p[0] = Node('assignment', [p[1], p[3]], lineno=p.lineno(1))

def p_expression(p):
    '''expression : term
                  | expression PLUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('plus', [p[1], p[3]], lineno=p.lineno(1))

def p_term(p):
    '''term : factor
            | term MUL factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('mul', [p[1], p[3]], lineno=p.lineno(1))

def p_factor(p):
    '''factor : NUM
              | ID'''
    p[0] = Node('factor', value=p[1], lineno=p.lineno(1))

def p_loop(p):
    '''loop : DO statement_list ENDDO WHILE LPAREN condition RPAREN ENDWHILE'''
    p[0] = Node('loop', [p[2], p[6]], lineno=p.lineno(1))

def p_condition(p):
    '''condition : ID ASSIGN NUM'''
    p[0] = Node('condition', [p[1], p[3]], lineno=p.lineno(1))

def p_error(p):
    raise SyntaxError(f"Error de sintaxis en línea {p.lineno}: '{p.value}'")

parser = yacc.yacc()
