from sudoku import Sudoku
from generator import generateSudoku
import time

board = Sudoku()
example = {"easy":"""
        53..7....
        6..195...
        .98....6.
        8...6...3
        4..8.3..1
        7...2...6
        .6....28.
        ...419..5
        ....8..79""",
        "extreme": """
        9.6..8.51
        ........3
        8..2.....
        .....53..
        ..9...2..
        .1.4...95
        .4..7....
        ......9..
        ..1..2.68"""
    }
board.parseGrid(example["extreme"])

st = time.time()
board.solve_with_comparison(original_board=example["extreme"],verbose=True,delay=0.15)


toNext = input("\n\n\nReady to See the Program Solve a Self Generated Puzzle?")

new_puzzle = Sudoku()
puzzle = generateSudoku("hard")
new_puzzle.parseGrid(puzzle)
new_puzzle.solve_with_comparison(puzzle,verbose=True,delay=0.15)


