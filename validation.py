def validateBoard(board):

    # Make sure the board is of correct size
    if (len(board)!=9 or len(board[0])!=9):
        return False

    # Check if all the rows are valid
    if not validateRows(board):
        return False
    
    # Check if all the columns are valid
    if not validateColumns(board):
        return False

    # Validate each of the Nine Boxes
    if not iterateNineBoxes(board):
        return False
    
    return True
            
def validateRows(board) ->bool:
    # Iterate through the rows validating each
    for outer in range(9):
        seen = set()
        for inner in range (9):
            current = board[outer][inner]
            if (current!=0 and current not in seen):
                seen.add(current)
            elif (current == 0):
                continue
            else:
                return False
    return True

def validateColumns(board)->bool:
    # Iterate through the columns validating each
    for outer in range(9):
        seen = set()
        for inner in range (9):
            current = board[inner][outer]
            if (current!=0 and current not in seen):
                seen.add(current)
            elif (current == 0):
                continue
            else:
                return False
    return True

def validateBox(board,row,column):
    seen = set()
    for outer in range(3):
        for inner in range(3):
            current = board[outer + row][inner + column]
            if (current!=0 and current not in seen):
                seen.add(current)
            elif (current == 0):
                continue
            else:
                return False
    return True 

def iterateNineBoxes(board):
    r =0
    c =0

    for i in range(3):
        for j in range(3):
            r = i * 3
            c = j * 3
            if not validateBox(board,r,c):
                return False
    return True

def efficient_Check(board, row, col, num):
    # Check row
    if num in board[row]:
        return False

    # Check column
    for r in range(9):
        if board[r][col] == num:
            return False

    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(3):
        for c in range(3):
            if board[start_row + r][start_col + c] == num:
                return False

    return True

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

    print(validateBoard(board))