def check_semantics(tree):
    if tree is None:
        return ["Árbol de sintaxis vacío"]

    declarations = {}
    errors = []

    def check_node(node):
        if node.type == 'declaration':
            var, value = node.children
            if var in declarations:
                errors.append(f"Línea {node.lineno}: Variable '{var}' redeclarada")
            else:
                declarations[var] = value
        elif node.type == 'assignment':
            var, expr = node.children
            if var not in declarations:
                errors.append(f"Línea {node.lineno}: Variable '{var}' no declarada")
            check_expr(expr, node.lineno)
        elif node.type == 'loop':
            statements, condition = node.children
            for stmt in statements:
                check_node(stmt)
            check_condition(condition, node.lineno)

    def check_expr(expr, lineno):
        if isinstance(expr, Node):
            if expr.type in ('plus', 'mul'):
                left, right = expr.children
                check_expr(left, lineno)
                check_expr(right, lineno)
            elif expr.type == 'factor' and isinstance(expr.value, str):
                if expr.value not in declarations:
                    errors.append(f"Línea {lineno}: Variable '{expr.value}' no declarada")

    def check_condition(condition, lineno):
        var, _ = condition.children
        if var not in declarations:
            errors.append(f"Línea {lineno}: Variable '{var}' no declarada en la condición")

    check_node(tree)
    return errors
