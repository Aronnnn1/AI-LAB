# ----------------- Helpers -----------------

skolem_count = 0

def fresh_skolem():
    global skolem_count
    skolem_count += 1
    return f"f{skolem_count}()"

def eliminate_implications(expr):
    if isinstance(expr, list):
        op = expr[0]
        if op == "=>":
            return ["∨", ["¬", eliminate_implications(expr[1])], eliminate_implications(expr[2])]
        elif op == "⇔":
            A = eliminate_implications(expr[1])
            B = eliminate_implications(expr[2])
            return ["∨", ["∧", A, B], ["∧", ["¬", A], ["¬", B]]]
        else:
            return [op] + [eliminate_implications(x) for x in expr[1:]]
    else:
        return expr

def move_not_inward(expr):
    if isinstance(expr, list):
        op = expr[0]
        if op == "¬":
            sub = expr[1]
            if isinstance(sub, list):
                if sub[0] == "¬":
                    return move_not_inward(sub[1])
                elif sub[0] == "∧":
                    return ["∨"] + [move_not_inward(["¬", x]) for x in sub[1:]]
                elif sub[0] == "∨":
                    return ["∧"] + [move_not_inward(["¬", x]) for x in sub[1:]]
                elif sub[0] == "∀":
                    return ["∃", sub[1], move_not_inward(["¬", sub[2]])]
                elif sub[0] == "∃":
                    return ["∀", sub[1], move_not_inward(["¬", sub[2]])]
            return ["¬", move_not_inward(sub)]
        elif op in ["∧", "∨", "∀", "∃"]:
            return [op] + [move_not_inward(x) for x in expr[1:]]
    return expr

def skolemize(expr, bound_vars=None):
    if bound_vars is None:
        bound_vars = set()
    if isinstance(expr, list):
        op = expr[0]
        if op == "∀":
            return ["∀", expr[1], skolemize(expr[2], bound_vars | {expr[1]})]
        elif op == "∃":
            sk = fresh_skolem()
            sub = replace_var(expr[2], expr[1], sk)
            return skolemize(sub, bound_vars)
        else:
            return [op] + [skolemize(x, bound_vars) for x in expr[1:]]
    return expr

def replace_var(expr, var, value):
    if isinstance(expr, list):
        return [expr[0]] + [replace_var(x, var, value) for x in expr[1:]]
    else:
        return value if expr == var else expr

def drop_universal(expr):
    if isinstance(expr, list):
        op = expr[0]
        if op == "∀":
            return drop_universal(expr[2])
        else:
            return [op] + [drop_universal(x) for x in expr[1:]]
    return expr

def distribute_or_over_and(expr):
    if isinstance(expr, list):
        op = expr[0]
        if op == "∨":
            A = distribute_or_over_and(expr[1])
            B = distribute_or_over_and(expr[2])
            if isinstance(A, list) and A[0] == "∧":
                return ["∧"] + [distribute_or_over_and(["∨", x, B]) for x in A[1:]]
            elif isinstance(B, list) and B[0] == "∧":
                return ["∧"] + [distribute_or_over_and(["∨", A, x]) for x in B[1:]]
            else:
                return ["∨", A, B]
        elif op == "∧":
            return ["∧"] + [distribute_or_over_and(x) for x in expr[1:]]
        else:
            return [op] + [distribute_or_over_and(x) for x in expr[1:]]
    return expr

def cnf(expr):
    step1 = eliminate_implications(expr)
    step2 = move_not_inward(step1)
    step3 = skolemize(step2)
    step4 = drop_universal(step3)
    step5 = distribute_or_over_and(step4)
    return step5

# ----------------- Pretty-print with proper symbols -----------------
def print_expr(expr):
    if isinstance(expr, list):
        op = expr[0]
        if op in ["∀", "∃"]:
            return f"{op}{expr[1]} {print_expr(expr[2])}"
        else:
            return "(" + f" {op} ".join([print_expr(x) for x in expr[1:]]) + ")"
    else:
        return str(expr)

# ----------------- Example -----------------
if __name__ == "__main__":
    # Input formula: ∀x (P(x) => Q(x)) ∧ ∃y P(y)
    formula = ["∧", ["∀", "x", ["=>", ["P", "x"], ["Q", "x"]]], ["∃", "y", ["P", "y"]]]

    print("Input formula:")
    print(print_expr(formula))

    cnf_formula = cnf(formula)

    print("\nCNF formula:")
    print(print_expr(cnf_formula))
