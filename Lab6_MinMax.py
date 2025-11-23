import math

# -------------------------
# Print board with lines
# -------------------------
def print_board(board):
    print()
    for r in range(3):
        row = " {} | {} | {} ".format(board[3*r], board[3*r+1], board[3*r+2])
        print(row)
        if r < 2:
            print("---+---+---")
    print()

# -------------------------
# Check winner
# -------------------------
def check_winner(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),    # rows
        (0,3,6), (1,4,7), (2,5,8),    # cols
        (0,4,8), (2,4,6)              # diagonals
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != " ":
            return board[a]  # "X" or "O"

    if " " not in board:
        return "Draw"
    return None

# -------------------------
# Minimax
# -------------------------
def minimax(board, depth, maximizing):
    result = check_winner(board)
    if result == "X": return -10 + depth
    if result == "O": return 10 - depth
    if result == "Draw": return 0

    if maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                val = minimax(board, depth+1, False)
                board[i] = " "
                best = max(best, val)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                val = minimax(board, depth+1, True)
                board[i] = " "
                best = min(best, val)
        return best

# -------------------------
# Best move for AI (O)
# -------------------------
def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# -------------------------
# Game loop
# -------------------------
def play_game():
    board = [" "] * 9
    print("You are X, AI is O.")
    print_board(board)

    while True:
        # Player move
        while True:
            try:
                pos = int(input("Enter position (0-8): "))
                if pos < 0 or pos > 8 or board[pos] != " ":
                    print("Invalid move. Try again.")
                else:
                    break
            except:
                print("Enter a valid number!")

        board[pos] = "X"
        print_board(board)

        result = check_winner(board)
        if result:
            print("Result:", result)
            break

        # AI move
        print("AI is thinking...")
        move = best_move(board)
        board[move] = "O"
        print_board(board)

        result = check_winner(board)
        if result:
            print("Result:", result)
            break

play_game()
