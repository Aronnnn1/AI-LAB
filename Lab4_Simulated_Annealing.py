import random
import math

def cost(state):
    """Return number of attacking pairs."""
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def get_neighbor(state):
    """Swap two columns to stay in permutation space."""
    neighbor = state[:]
    i, j = random.sample(range(len(state)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def simulated_annealing(n=8, max_iter=50000, temp=100.0, cooling=0.999):
    current = list(range(n))
    random.shuffle(current)
    current_cost = cost(current)

    temperature = temp

    best = current[:]
    best_cost = current_cost

    for _ in range(max_iter):
        if temperature <= 1e-8 or best_cost == 0:
            break

        neighbor = get_neighbor(current)
        neighbor_cost = cost(neighbor)

        delta = current_cost - neighbor_cost

        if delta > 0 or random.random() < math.exp(delta / temperature):
            current, current_cost = neighbor, neighbor_cost
            if current_cost < best_cost:
                best, best_cost = current[:], current_cost

        temperature *= cooling

    return best, best_cost

def print_board(state):
    n = len(state)
    for row in range(n):
        print(" ".join("Q" if state[col] == row else "." for col in range(n)))
    print()

if __name__ == "__main__":
    n = 8
    solution, cost_val = simulated_annealing(n)
    print("Best state:", solution)
    print("Conflicts:", cost_val)
    print("Non-attacking pairs:", n*(n-1)//2 - cost_val)
    print("\nBoard:")
    print_board(solution)
