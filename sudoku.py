import time

class Cell:

    def __init__(self,row,col,subgrid,value=0) -> None:
        self.val = value
        self.row = row
        self.col = col
        self.grid = subgrid
        # candidates holds possible values for this cell (1-9)
        self.cands = set(range(1, 10))

def locateSubGrid(i,j) -> int:
    return (i // 3) * 3 + (j // 3) + 1

class Sudoku:

    def __init__(self) -> None:
        self.cells = []
        self.nodes_visited = 0

        for i in range(9):
            tmp = []
            for j in range(9):
                tmp.append(Cell(row=i,col=j,subgrid=locateSubGrid(i,j)))
            self.cells.append(tmp)

    def checkRow(self, row, num):
        for cell in self.cells[row]:
            if cell.val == num:
                return False
        return True
        
    def checkCol(self, col, num):
        for i in range(9):
            if self.cells[i][col].val == num:
                return False
        return True

    def checkGrid(self, row, col, num):
        grid = self.cells[row][col].grid
        for r in range((row//3)*3, (row//3)*3 + 3):
            for c in range((col//3)*3, (col//3)*3 + 3):
                if self.cells[r][c].grid == grid and self.cells[r][c].val == num:
                    return False
        return True

    def parseGrid(self, grid: str):
        """Expects Grid in format
            ... ... ... 
            ... ... ...
            ... ... ..."""
        grid = grid.replace(" ", "").replace("\n", "")
        idx = 0
        for i in range(9):
            for j in range(9):
                if grid[idx].isdigit():
                    self.cells[i][j].val = int(grid[idx])
                idx += 1
        # capture original board (string) before candidate changes
        self._original = self.__repr__()
        # initialize candidate sets after loading fixed values
        self.init_candidates()

    def get_row_values(self, row):
        return {c.val for c in self.cells[row] if c.val != 0}

    def get_col_values(self, col):
        return {self.cells[r][col].val for r in range(9) if self.cells[r][col].val != 0}

    def get_grid_values(self, row, col):
        g = self.cells[row][col].grid
        vals = set()
        for r in range((row//3)*3, (row//3)*3 + 3):
            for c in range((col//3)*3, (col//3)*3 + 3):
                if self.cells[r][c].grid == g and self.cells[r][c].val != 0:
                    vals.add(self.cells[r][c].val)
        return vals

    def init_candidates(self):
        """Initialize candidate sets for all empty cells based on current board"""
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                if cell.val != 0:
                    cell.cands.clear()
                else:
                    used = self.get_row_values(i) | self.get_col_values(j) | self.get_grid_values(i, j)
                    cell.cands = set(range(1, 10)) - used

    def choose_cell_mrv(self):
        """Choose the empty cell with Minimum Remaining Values (MRV). Returns (i,j) or None if full."""
        best = None
        best_count = 10
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                if cell.val == 0:
                    ccount = len(cell.cands)
                    if ccount == 0:
                        return (i, j)  # dead end
                    if ccount < best_count:
                        best_count = ccount
                        best = (i, j)
        return best

    def place_number(self, i, j, num):
        """Place number and update candidate sets of peers. Returns list of changes for backtracking."""
        self.cells[i][j].val = num
        changes = []  # list of (pi,pj,removed_value)
        # remove num from peers' candidates
        #peers in same column
        for col in range(9):
            if col == j:
                continue
            peer = self.cells[i][col]
            if peer.val == 0 and num in peer.cands:
                peer.cands.remove(num)
                changes.append((i, col, num))
        #peers in same row
        for row in range(9):
            if row == i:
                continue
            peer = self.cells[row][j]
            if peer.val == 0 and num in peer.cands:
                peer.cands.remove(num)
                changes.append((row, j, num))
        # peers in same grid
        g = self.cells[i][j].grid
        for r in range((i//3)*3, (i//3)*3 + 3):
            for c in range((j//3)*3, (j//3)*3 + 3):
                if self.cells[r][c].grid == g and (r != i or c != j):
                    peer = self.cells[r][c]
                    if peer.val == 0 and num in peer.cands:
                        peer.cands.remove(num)
                        changes.append((r, c, num))
        # clear this cell's candidates
        self.cells[i][j].cands.clear()
        return changes

    def unplace_number(self, i, j, num, changes):
        """Undo a placement and restore candidate removals."""
        self.cells[i][j].val = 0
        # restore candidates
        for (r, c, value) in changes:
            self.cells[r][c].cands.add(value)
        # recompute this cell's candidates (fast way)
        used = self.get_row_values(i) | self.get_col_values(j) | self.get_grid_values(i, j)
        self.cells[i][j].cands = set(range(1, 10)) - used

    def __repr__(self) -> str:
        board_str = ""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                board_str += "------+-------+------\n"
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    board_str += "| "
                val = self.cells[i][j].val
                board_str += f"{val if val != 0 else '.'} "
            board_str += "\n"
        return board_str
    
    def solve(self,verbose=False, delay=0.05):
        """Solve the Sudoku puzzle using backtracking algorithm using MRV + maintained candidates.

        Verbose=True depicts every step along the process
        """
        self.nodes_visited += 1

        # pick next empty cell using MRV
        choice = self.choose_cell_mrv()
        if choice is None:
            # no empty cell -> solved
            # if visual mode, show final comparison and reset flag
            if verbose and getattr(self, '_visual_started', False):
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                print("ORIGINAL PUZZLE:")
                print(getattr(self, '_original', ''))
                print("\nSOLVED PUZZLE:")
                print(self)
                print(f"\n{'='*30}")
                print(f"Nodes visited during solving: {self.nodes_visited}")
                print(f"{'='*30}")
                # reset visual flag for future runs
                self._visual_started = False
            return True
        i, j = choice
        # if a dead-end (zero candidates), fail
        if len(self.cells[i][j].cands) == 0:
            return False

        # try candidates (sorted for deterministic behavior)
        for num in sorted(self.cells[i][j].cands):
            # place and record changes
            changes = self.place_number(i, j, num)

            if verbose:
                import os, time
                os.system('cls' if os.name == 'nt' else 'clear')
                print("ORIGINAL PUZZLE:")
                print(getattr(self, '_original', ''))
                print("\n")
                print(f"Placed {num} at ({i}, {j}):")
                print(f"Nodes visited: {self.nodes_visited}")
                print(self)
                time.sleep(delay)

            # recurse
            if self.solve(verbose=verbose, delay=delay):
                return True

            # backtrack
            self.unplace_number(i, j, num, changes)

        return False
    
    def solve_with_comparison(self, original_board, verbose=False, delay=0.05):
        """Solve the puzzle and display original vs solved comparison"""
        start_time = time.time()
        self.solve(verbose=verbose, delay=delay)
        end_time = time.time()
        solve_time = end_time - start_time
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        tmp = Sudoku()
        tmp.parseGrid(original_board)
        print("ORIGINAL PUZZLE:")
        print(tmp)
        print("\nSOLVED PUZZLE:")
        print(self)
        print(f"\n{'='*30}")
        print(f"Nodes visited during solving: {self.nodes_visited}")
        print(f"Solving time: {solve_time:.4f} seconds")
        print(f"{'='*30}")

    def solve_basic(self, verbose=False, delay=0.05):
        self.nodes_visited += 1

        # Find first empty cell (row-major order)
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].val == 0:

                    # Try digits 1–9
                    for num in range(1, 10):

                        if (self.checkRow(i, num) and 
                            self.checkCol(j, num) and 
                            self.checkGrid(i, j, num)):

                            # Place number
                            self.cells[i][j].val = num

                            if verbose:
                                import os, time
                                os.system('cls' if os.name == 'nt' else 'clear')
                                print(f"Placed {num} at ({i}, {j})")
                                print(f"Nodes visited: {self.nodes_visited}")
                                print(self)
                                time.sleep(delay)

                            # Continue recursively
                            if self.solve_basic(verbose=verbose, delay=delay):
                                return True

                            # Backtrack
                            self.cells[i][j].val = 0

                    # None of 1–9 worked → failure
                    return False

        # No empty cells → success
        return True