from flask import Flask, request, render_template
from lexer import lexer
from parser import parser
from semantic_analyzer import check_semantics

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form['code']
    
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_type = classify_token(tok)
        tokens.append({
            'line': tok.lineno,
            'value': tok.value,
            'type': token_type
        })
    
    # Intentar parsear el código
    try:
        parse_result = parser.parse(code)
    except Exception as e:
        parse_result = None
        error_message = str(e)

    # Si hay errores de parsing, devolverlos
    if parse_result is None:
        return render_template('index.html', tokens=tokens, parse_result=parse_result, semantic_errors=[error_message])
    
    # Analizar semánticamente si el parsing fue exitoso
    semantic_errors = check_semantics(parse_result)

    return render_template('index.html', tokens=tokens, parse_result=parse_result, semantic_errors=semantic_errors)

def classify_token(tok):
    if tok.type in ('INT', 'WHILE', 'DO', 'ENDDO', 'ENDWHILE'):
        return 'reservada'
    elif tok.type == 'ID':
        return 'identificador'
    elif tok.type == 'NUM':
        return 'numero'
    elif tok.type in ('ASSIGN', 'PLUS', 'MUL', 'SEMI'):
        return 'simbolo'
    elif tok.type == 'LPAREN':
        return 'parentesis izquierdo'
    elif tok.type == 'RPAREN':
        return 'parentesis derecho'
    elif tok.type == 'LBRACE':
        return 'llave izquierda'
    elif tok.type == 'RBRACE':
        return 'llave derecha'
    return 'desconocido'

if __name__ == '__main__':
    app.run(debug=True)
