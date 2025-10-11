from validation import validateBoard
import time

"""
This is a working version however, due to validation logic being excessive time complexity is inefficient
"""
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
        [0,0,0,2,6,0,7,0,1],
        [6,8,0,0,7,0,0,9,0],
        [1,9,0,0,0,4,5,0,0],
        [8,2,0,1,0,0,0,4,0],
        [0,0,4,6,0,2,9,0,0],
        [0,5,0,0,0,3,0,2,8],
        [0,0,9,3,0,0,0,7,4],
        [0,4,0,0,5,0,0,3,6],
        [7,0,3,0,1,8,0,0,0]
    ]
    # print(validateBoard(board))

    st = time.time()

    sol = solve_sudoku(board)

    et = time.time()
    
    if not sol:
        print("Unsolvable")
    for i in sol:
        print(i)

    print(f"\n\n\n\tTime taken : {et-st} seconds")


    zeroes = [
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
    ]