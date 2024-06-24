import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | loop'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : INT ID ASSIGN NUM SEMI'''
    p[0] = ('declaration', p[2], p[4])

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI'''
    p[0] = ('assignment', p[1], p[3])

def p_expression(p):
    '''expression : term
                  | expression PLUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('plus', p[1], p[3])

def p_term(p):
    '''term : factor
            | term MUL factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('mul', p[1], p[3])

def p_factor(p):
    '''factor : NUM
              | ID'''
    p[0] = p[1]

def p_loop(p):
    '''loop : DO statement_list ENDDO WHILE LPAREN condition RPAREN ENDWHILE'''
    p[0] = ('loop', p[2], p[6])

def p_condition(p):
    '''condition : ID ASSIGN NUM'''
    p[0] = ('condition', p[1], p[3])

def p_error(p):
    raise SyntaxError(f"Error de sintaxis en '{p.value}'")

parser = yacc.yacc()
