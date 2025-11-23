import time
from heapq import heappush, heappop
import itertools

# ---------------------------
# PRINT 3x3 PUZZLE
# ---------------------------
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
    print()

# ---------------------------
# MOVE GENERATOR
# ---------------------------
def get_neighbors(state):
    neighbors = []
    blank = state.index('_')
    r, c = divmod(blank, 3)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nb = nr*3 + nc
            new_state = list(state)
            new_state[blank], new_state[nb] = new_state[nb], new_state[blank]
            neighbors.append(tuple(new_state))
    return neighbors

# ---------------------------
# MANHATTAN DISTANCE HEURISTIC
# ---------------------------
def manhattan_distance(state, goal):
    distance = 0
    for num in range(1, 9):  # ignore blank
        idx_s = state.index(num)
        idx_g = goal.index(num)
        x_s, y_s = divmod(idx_s, 3)
        x_g, y_g = divmod(idx_g, 3)
        distance += abs(x_s - x_g) + abs(y_s - y_g)
    return distance

# ---------------------------
# GREEDY BEST-FIRST SEARCH
# ---------------------------
def greedy_bfs(start, goal):
    start = tuple(start)
    goal = tuple(goal)
    
    visited = set()
    parent = {start: None}
    states_explored = 0

    counter = itertools.count()  # tie-breaker to avoid tuple comparisons
    heap = []
    heappush(heap, (manhattan_distance(start, goal), next(counter), start))

    while heap:
        h, _, state = heappop(heap)
        states_explored += 1

        if state == tuple(goal):
            path = []
            node = state
            while node is not None:
                path.append(list(node))
                node = parent[node]
            return path[::-1], states_explored

        if state not in visited:
            visited.add(state)
            for nxt in get_neighbors(list(state)):
                if nxt not in visited:
                    parent[nxt] = state
                    heappush(heap, (manhattan_distance(list(nxt), goal), next(counter), nxt))

    return None, states_explored

# ---------------------------
# MAIN
# ---------------------------
initial_state = [
    1, 2, 3,
    4, 8, '_',
    7, 6, 5
]

goal_state = [
    1, 2, 3,
    4, 5, 6,
    7, 8, '_'
]

print("=== GREEDY BEST-FIRST SEARCH (Manhattan) ===\n")
start_time = time.time()
solution_path, explored = greedy_bfs(initial_state, goal_state)
end_time = time.time()

if solution_path:
    print(f"Solution found in {len(solution_path)-1} moves!")
    print(f"Total states explored: {explored}\n")
    for i, step in enumerate(solution_path):
        print(f"Step {i}:")
        print_puzzle(step)
else:
    print(f"No solution found. Total states explored: {explored}")

print("Execution time:", end_time - start_time, "seconds")
