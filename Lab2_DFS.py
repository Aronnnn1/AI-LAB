import time

# ---------------------------
# PRINT 3×3 PUZZLE
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
    moves = [(-1,0),(1,0),(0,-1),(0,1)]  # up, down, left, right

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nb = nr*3 + nc
            new_state = list(state)
            new_state[blank], new_state[nb] = new_state[nb], new_state[blank]
            neighbors.append(tuple(new_state))
    return neighbors

# ---------------------------
# ITERATIVE DFS WITH DEPTH LIMIT
# ---------------------------
def dfs_limited_iterative(start, goal, depth_limit=30):
    start = tuple(start)
    goal = tuple(goal)

    # Stack: (state, depth)
    stack = [(start, 0)]
    visited = set()
    parent = {start: None}
    states_explored = 0

    while stack:
        state, depth = stack.pop()
        states_explored += 1

        if state == goal:
            # reconstruct path
            path = []
            node = goal
            while node is not None:
                path.append(list(node))
                node = parent[node]
            return path[::-1], states_explored

        if state not in visited and depth < depth_limit:
            visited.add(state)
            for nxt in reversed(get_neighbors(list(state))):
                if nxt not in visited and nxt not in [s for s,_ in stack]:
                    parent[nxt] = state
                    stack.append((nxt, depth + 1))

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

print("=== ITERATIVE DFS WITH DEPTH LIMIT ===\n")
start_time = time.time()
solution_path, states_explored = dfs_limited_iterative(initial_state, goal_state, depth_limit=25)
end_time = time.time()

if solution_path:
    print(f"DFS found a solution in {len(solution_path)-1} moves!")
    print(f"Total states explored: {states_explored}\n")
    for i, step in enumerate(solution_path):
        print(f"Step {i}:")
        print_puzzle(step)
else:
    print(f"DFS did NOT find a solution. Total states explored: {states_explored}")
    print("Try increasing the depth limit.")

print("Execution time:", end_time - start_time, "seconds")
