import random
import math

def compute_cost(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def random_permutation(n):
    arr = list(range(n))
    random.shuffle(arr)
    return arr

def neighbors_by_swaps(state):
    n = len(state)
    for i in range(n - 1):
        for j in range(i + 1, n):
            nb = state.copy()
            nb[i], nb[j] = nb[j], nb[i]
            yield nb

def hill_climb_with_restarts(n, max_restarts=None):
    visited = set()
    total_states = math.factorial(n)
    restarts = 0

    while True:
        if len(visited) >= total_states:
            raise RuntimeError("All states visited — giving up (no solution found).")

        state = random_permutation(n)
        while tuple(state) in visited:
            state = random_permutation(n)
        visited.add(tuple(state))

        while True:
            cost = compute_cost(state)
            if cost == 0:
                return state, restarts

            best_neighbor = None
            best_cost = float("inf")
            for nb in neighbors_by_swaps(state):
                c = compute_cost(nb)
                if c < best_cost:
                    best_cost = c
                    best_neighbor = nb

            if best_cost < cost:
                state = best_neighbor
                visited.add(tuple(state))
            else:
                restarts += 1
                if max_restarts is not None and restarts >= max_restarts:
                    raise RuntimeError(f"Stopped after {restarts} restarts.")
                break

def format_board(state):
    n = len(state)
    lines = []
    for r in range(n):
        row = []
        for c in range(n):
            if state[c] == r:
                row.append("Q")
            else:
                row.append("-")
        lines.append(" ".join(row))
    return "\n".join(lines)

if __name__ == "__main__":
    n = 4
    solution, restarts = hill_climb_with_restarts(n)
    print("Found solution:", solution)
    print("Restarts:", restarts)
    print(format_board(solution))
