import time
from collections import deque

# --------------------------------------------------
#  PRINT STATE AS 3×3 PUZZLE
# --------------------------------------------------
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
    print()  # blank line


# --------------------------------------------------
#  MOVE GENERATOR (automatic, no hard-coding)
# --------------------------------------------------
def get_neighbors(state):
    neighbors = []
    blank = state.index('_')

    r, c = divmod(blank, 3)
    moves = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_blank = nr * 3 + nc
            new_state = list(state)
            new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]
            neighbors.append(tuple(new_state))

    return neighbors


# --------------------------------------------------
#  BFS ALGORITHM
# --------------------------------------------------
def bfs(start, goal):

    start = tuple(start)
    goal = tuple(goal)

    queue = deque([start])
    visited = {start}
    parent = {start: None}

    states_explored = 0

    while queue:
        state = queue.popleft()
        states_explored += 1

        if state == goal:
            # reconstruct path
            path = []
            while state is not None:
                path.append(list(state))
                state = parent[state]
            return path[::-1], states_explored

        for next_state in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = state
                queue.append(next_state)

    return None, states_explored


# --------------------------------------------------
#  TEST INPUT
# --------------------------------------------------
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

# --------------------------------------------------
#  RUN BFS
# --------------------------------------------------
start_time = time.time()
solution, explored = bfs(initial_state, goal_state)
end_time = time.time()


# --------------------------------------------------
#  OUTPUT
# --------------------------------------------------
if solution is None:
    print("❌ No solution exists.")
else:
    print("✔️ Solution found in", len(solution)-1, "moves")
    print("------------------------------\n")

    for i, state in enumerate(solution):
        print(f"Step {i}:")
        print_puzzle(state)

print("Total states explored:", explored)
print("Execution time: {:.6f} seconds".format(end_time - start_time))
