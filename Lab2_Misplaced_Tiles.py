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
# MISPLACED TILES HEURISTIC
# ---------------------------
def misplaced_tiles(state, goal):
    count = 0
    for i in range(9):
        if state[i] != '_' and state[i] != goal[i]:
            count += 1
    return count

# ---------------------------
# GREEDY BEST-FIRST SEARCH
# ---------------------------
def greedy_bfs_misplaced(start, goal):
    start = tuple(start)
    goal = tuple(goal)
    
    visited = set()
    parent = {start: None}
    states_explored = 0

    counter = itertools.count()  # tie-breaker for heap
    heap = []
    heappush(heap, (misplaced_tiles(start, goal), next(counter), start))

    while heap:
        h, _, state = heappop(heap)
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
                if nxt not in visited:
                    parent[nxt] = state
                    heappush(heap, (misplaced_tiles(list(nxt), goal), next(counter), nxt))

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

print("=== GREEDY BEST-FIRST SEARCH (Misplaced Tiles) ===\n")
start_time = time.time()
solution_path, explored = greedy_bfs_misplaced(initial_state, goal_state)
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
