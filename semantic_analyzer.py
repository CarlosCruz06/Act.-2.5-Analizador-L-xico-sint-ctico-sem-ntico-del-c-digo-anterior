def check_semantics(tree):
    if tree is None:
        return ["Árbol de sintaxis vacío"]

    declarations = {}
    errors = []

    def check_node(node):
        if node[0] == 'declaration':
            _, var, value = node
            if var in declarations:
                errors.append(f"Variable '{var}' redeclarada")
            else:
                declarations[var] = value
        elif node[0] == 'assignment':
            _, var, expr = node
            if var not in declarations:
                errors.append(f"Variable '{var}' no declarada")
            check_expr(expr)
        elif node[0] == 'loop':
            _, statements, condition = node
            for stmt in statements:
                check_node(stmt)
            check_condition(condition)

    def check_expr(expr):
        if isinstance(expr, tuple):
            _, left, right = expr
            check_expr(left)
            check_expr(right)
        elif isinstance(expr, str):
            if expr not in declarations:
                errors.append(f"Variable '{expr}' no declarada")

    def check_condition(condition):
        _, var, _ = condition
        if var not in declarations:
            errors.append(f"Variable '{var}' no declarada en la condición")

    check_node(tree)
    return errors
