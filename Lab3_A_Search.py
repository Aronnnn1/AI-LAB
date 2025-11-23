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
    for num in range(1, 9):
        idx_s = state.index(num)
        idx_g = goal.index(num)
        x_s, y_s = divmod(idx_s, 3)
        x_g, y_g = divmod(idx_g, 3)
        distance += abs(x_s - x_g) + abs(y_s - y_g)
    return distance

# ---------------------------
# A* SEARCH
# ---------------------------
def astar_manhattan(start, goal):
    start = tuple(start)
    goal = tuple(goal)

    visited = set()
    parent = {start: None}
    g_cost = {start: 0}  # cost so far
    states_explored = 0

    counter = itertools.count()  # tie-breaker for heap
    heap = []
    f_start = g_cost[start] + manhattan_distance(start, goal)
    heappush(heap, (f_start, next(counter), start))

    while heap:
        f, _, state = heappop(heap)
        states_explored += 1

        if state == tuple(goal):
            # reconstruct path
            path = []
            node = state
            while node is not None:
                path.append(list(node))
                node = parent[node]
            return path[::-1], states_explored

        if state not in visited:
            visited.add(state)
            for nxt in get_neighbors(list(state)):
                tentative_g = g_cost[state] + 1
                if nxt not in g_cost or tentative_g < g_cost[nxt]:
                    g_cost[nxt] = tentative_g
                    f_nxt = tentative_g + manhattan_distance(list(nxt), goal)
                    parent[nxt] = state
                    heappush(heap, (f_nxt, next(counter), nxt))

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

print("=== A* SEARCH WITH MANHATTAN DISTANCE ===\n")
start_time = time.time()
solution_path, explored = astar_manhattan(initial_state, goal_state)
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
