# ----------------- Forward Chaining -----------------

def forward_chaining(kb_rules, facts, query):
    inferred = set(facts)  # already known facts
    agenda = list(facts)   # facts to process
    steps = []             # to print inference steps

    while agenda:
        p = agenda.pop(0)
        for rule in kb_rules:
            premise, conclusion = rule
            if premise.issubset(inferred) and conclusion not in inferred:
                inferred.add(conclusion)
                agenda.append(conclusion)
                steps.append(f"Inferred {conclusion} from {', '.join(premise)}")
                if conclusion == query:
                    return True, steps
    return query in inferred, steps

# ----------------- Example -----------------
if __name__ == "__main__":
    # Knowledge base: list of (premise set, conclusion)
    # Example: ({"A", "B"}, "C") means "A ∧ B ⇒ C"
    kb_rules = [
        ({"A", "B"}, "C"),
        ({"C"}, "D"),
        ({"D", "E"}, "F")
    ]

    facts = {"A", "B", "E"}  # initial facts
    query = "F"

    print("Knowledge Base Rules:")
    for prem, concl in kb_rules:
        print(f"{' ∧ '.join(prem)} ⇒ {concl}")

    print("\nFacts:", ", ".join(facts))
    print(f"Query: {query}\n")

    result, steps = forward_chaining(kb_rules, facts, query)

    print("Inference Steps:")
    for step in steps:
        print(step)

    if result:
        print(f"\nConclusion: {query} is entailed by KB.")
    else:
        print(f"\nConclusion: {query} is NOT entailed by KB.")
