def negate(lit):
    return lit[1:] if lit.startswith("¬") else "¬" + lit

def format_clause(clause):
    if len(clause) == 0:
        return "⟂"
    return " ∨ ".join(sorted(clause))

def resolve(C1, C2):
    resolvents = []
    for lit in C1:
        neg = negate(lit)
        if neg in C2:
            new_clause = (C1 - {lit}) | (C2 - {neg})
            resolvents.append(new_clause)
    return resolvents

def resolution(KB, alpha):
    clauses = [set(c) for c in KB]
    clauses.append({negate(alpha)})

    print("Initial clauses:")
    for c in clauses:
        print(" ", format_clause(c))
    print()

    new = set()
    seen = set(frozenset(c) for c in clauses)

    while True:
        added_any = False
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i+1, len(clauses))]

        for (C1, C2) in pairs:
            for r in resolve(C1, C2):
                r_frozen = frozenset(r)
                if r_frozen not in seen:
                    print(f"{format_clause(C1)}  &  {format_clause(C2)}  →  {format_clause(r)}")
                    seen.add(r_frozen)
                    new.add(r_frozen)
                    added_any = True

                    if len(r) == 0:
                        print("\nEmpty clause derived → KB ⊨ α")
                        return True

        if not added_any:
            print("\nNo new clauses → KB ⊭ α")
            return False

        for c in new:
            clauses.append(set(c))
        new.clear()


# ---------------- Example ----------------
if __name__ == "__main__":
    KB = [
        {"A", "B"},
        {"¬A", "C"},
        {"¬B", "C"}
    ]
    alpha = "C"

    resolution(KB, alpha)
