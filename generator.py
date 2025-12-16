import random

# Helpers

def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None

def is_valid(board, r, c, num):
    if num in board[r]:    # Check row
        return False

    for i in range(9):     # Check column
        if board[i][c] == num:
            return False

    br = (r // 3) * 3      # Check box
    bc = (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if board[i][j] == num:
                return False

    return True

def solve_backtrack(board):
    empty = find_empty(board)
    if not empty:
        return True

    r, c = empty
    nums = list(range(1, 10))
    random.shuffle(nums)  # Adds randomness to generation

    for num in nums:
        if is_valid(board, r, c, num):
            board[r][c] = num
            if solve_backtrack(board):
                return True
            board[r][c] = 0

    return False

def generate_full_board():
    board = [[0]*9 for _ in range(9)]
    solve_backtrack(board)
    return board

# Difficulty presets

DIFFICULTY_HOLES = {
    "easy": 30,
    "medium": 40,
    "hard": 50,
    "expert": 60
}

# Public function: generateSudoku()

def generateSudoku(difficulty="medium") -> str:
    """
    Returns a Sudoku puzzle as a 9×9 matrix, with 0 representing empty cells.
    Difficulty can be: "easy", "medium", "hard", "expert".
    """

    difficulty = difficulty.lower()
    if difficulty not in DIFFICULTY_HOLES:
        raise ValueError(f"Unknown difficulty: {difficulty}")

    holes = DIFFICULTY_HOLES[difficulty]

    # 1. Generate full valid board
    full_board = generate_full_board()

    # 2. Remove cells according to difficulty
    puzzle = [row[:] for row in full_board]
    removed = 0

    while removed < holes:
        r = random.randint(0, 8)
        c = random.randint(0, 8)

        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            removed += 1

    # Convert puzzle (list of lists) to a string format compatible with Sudoku.parseGrid
    rows = []
    for row in puzzle:
        rows.append(''.join(str(cell) if cell != 0 else '.' for cell in row))

    return '\n'.join(rows)
