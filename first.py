from validation import validateBoard

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Find next empty cell
                for num in range(1, 10):
                    board[row][col] = num   # Place the number
                    if validateBoard(board):  # Check whole board
                        result = solve_sudoku(board)
                        if result:  # Found a solution down this path
                            return result
                    board[row][col] = 0  # Backtrack
                return None  # Dead end
    return [row[:] for row in board]  # No empty cells left → return solved board


if __name__=="__main__":
    board = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
    ]
    # print(validateBoard(board))

    sol = solve_sudoku(board)

    for i in sol:
        print(i)
