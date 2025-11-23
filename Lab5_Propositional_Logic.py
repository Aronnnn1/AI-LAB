import itertools
import re

def safe_replace(formula, truth_assignment):
    """Replace variables with True/False safely using word boundaries."""
    for symbol, value in truth_assignment.items():
        formula = re.sub(rf'\b{symbol}\b', str(value), formula)
    return formula

def evaluate_formula(formula, truth_assignment):
    eval_formula = safe_replace(formula, truth_assignment)
    return eval(eval_formula)

def generate_truth_table(variables):
    return list(itertools.product([False, True], repeat=len(variables)))

def is_entailed(KB_formula, alpha_formula, variables):
    truth_combinations = generate_truth_table(variables)

    print(f"{' '.join(variables)} | KB | α")
    print("-" * (len(variables) * 2 + 10))

    for combination in truth_combinations:
        truth_assignment = dict(zip(variables, combination))

        KB_value = evaluate_formula(KB_formula, truth_assignment)
        alpha_value = evaluate_formula(alpha_formula, truth_assignment)

        row = " ".join("T" if v else "F" for v in combination)
        print(f"{row} | {'T' if KB_value else 'F'}  | {'T' if alpha_value else 'F'}")

        # entailment violation:
        if KB_value and not alpha_value:
            return False

    return True

# Example
KB = "(A or C) and (B or not C)"
alpha = "A or B"
variables = ['A', 'B', 'C']

if is_entailed(KB, alpha, variables):
    print("\nKB ⊨ α   (The knowledge base entails alpha)")
else:
    print("\nKB ⊭ α   (The knowledge base does NOT entail alpha)")
