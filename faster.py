from validation import efficient_Check
from first import print_board
import time

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Find next empty cell
                for num in range(1, 10):
                    if efficient_Check(board,row,col,num): 
                        board[row][col] = num 
                        result = solve_sudoku(board)
                        if result:  # Found a solution down this path
                            return result
                    board[row][col] = 0  # Backtrack
                return None  # Dead end
    return [row[:] for row in board]  # No empty cells left → return solved board

if __name__=="__main__":
    
    zeroes = [
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]
    ]


    board = [
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 4, 3, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 6],
        [0, 0, 0, 5, 0, 9, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 8, 0, 7, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 5, 0]
    ]

    print("\nInitial Puzzle:")
    print_board(board)

    st = time.time()
    solved = solve_sudoku(board)
    et = time.time()
    
    if not solved:
        print("\nUnsolvable")
    else:
        print("\nSolution:")
        print_board(solved) 

    print(f"\nTime taken : {et-st:.6f} seconds")