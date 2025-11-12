def is_variable(x):
    return isinstance(x, str) and x[0].islower()

def unify(x, y, subst):
    if subst is None:
        return None
    elif x == y:
        return subst
    elif is_variable(x):
        return unify_var(x, y, subst)
    elif is_variable(y):
        return unify_var(y, x, subst)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for a, b in zip(x, y):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    else:
        return None

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif occurs_check(var, x, subst):
        return None
    else:
        subst[var] = x
        return subst

def occurs_check(var, x, subst):
    if var == x:
        return True
    elif isinstance(x, list):
        return any(occurs_check(var, xi, subst) for xi in x)
    elif x in subst:
        return occurs_check(var, subst[x], subst)
    return False

def parse(expr):
    expr = expr.strip()
    if '(' not in expr:
        return expr
    functor = expr[:expr.index('(')]
    args_str = expr[expr.index('(')+1:-1]
    args = []
    balance = 0
    current = ''
    for c in args_str:
        if c == ',' and balance == 0:
            args.append(parse(current.strip()))
            current = ''
        else:
            if c == '(':
                balance += 1
            elif c == ')':
                balance -= 1
            current += c
    if current:
        args.append(parse(current.strip()))
    return [functor] + args

def apply_subst(expr, subst):
    if isinstance(expr, str):
        if expr in subst:
            return apply_subst(subst[expr], subst)
        else:
            return expr
    elif isinstance(expr, list):
        return [apply_subst(e, subst) for e in expr]
    else:
        return expr

def format_expr(expr):
    if isinstance(expr, str):
        return expr
    if len(expr) == 1:
        return expr[0]
    return f"{expr[0]}({', '.join(format_expr(e) for e in expr[1:])})"

def format_mgu(subst):
    return ', '.join(f"{v}:{format_expr(subst[v])}" for v in subst)

def unify_statements(s1, s2):
    t1 = parse(s1)
    t2 = parse(s2)
    if t1[0] != t2[0]:
        print("Not unifiable (different predicates).")
        return
    subst = unify(t1[1:], t2[1:], {})
    if subst is None:
        print("Not unifiable.")
    else:
        unified = [t1[0]] + [apply_subst(arg, subst) for arg in t1[1:]]
        print(f"MGU: {format_mgu(subst)}")
        print(f"Unified Statement: {format_expr(unified)}")

# --- Main ---
if __name__ == "__main__":
    s1 = input("Enter first statement: ").strip()
    s2 = input("Enter second statement: ").strip()
    unify_statements(s1, s2)
