import math

# -----------------------------------
# Print board with nice grid
# -----------------------------------
def print_board(board):
    print()
    for r in range(3):
        print(" {} | {} | {} ".format(board[3*r], board[3*r+1], board[3*r+2]))
        if r < 2:
            print("---+---+---")
    print()

# -----------------------------------
# Check winner or draw
# -----------------------------------
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

# -----------------------------------
# Minimax with Alpha-Beta Pruning
# -----------------------------------
def minimax(board, depth, alpha, beta, maximizing):
    result = check_winner(board)
    
    # Terminal states
    if result == "X": return -10 + depth
    if result == "O": return 10 - depth
    if result == "Draw": return 0

    if maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                eval = minimax(board, depth+1, alpha, beta, False)
                board[i] = " "
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break   # prune
        return max_eval

    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                eval = minimax(board, depth+1, alpha, beta, True)
                board[i] = " "
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break   # prune
        return min_eval

# -----------------------------------
# Find best move for AI (O)
# -----------------------------------
def best_move(board):
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# -----------------------------------
# Main Game Loop
# -----------------------------------
def play_game():
    board = [" "] * 9
    print("You are X. AI is O.")
    print_board(board)

    while True:
        # Your move
        while True:
            try:
                pos = int(input("Enter your move (0-8): "))
                if pos < 0 or pos > 8 or board[pos] != " ":
                    print("Invalid move, try again.")
                else:
                    break
            except:
                print("Enter a number!")

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
