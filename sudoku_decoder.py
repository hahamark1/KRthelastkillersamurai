"""
The implementation of this Sudoku solver is based on the paper:
    "A SAT-based Sudoku solver" by Tjark Weber
    https://www.lri.fr/~conchon/mpri/weber.pdf
If you want to understand the code below, in particular the function valid(),
which calculates the 324 clauses corresponding to 9 cells, you are strongly
encouraged to read the paper first.  The paper is very short, but contains
all necessary information.
"""
import pycosat
import pickle
import textwrap
# from scraper import *


def v(i, j, d):
    """
    Return the number of the variable of cell i, j and digit d,
    which is an integer in the range of 1 to 729 (including).
    """
    return 81 * (i - 1) + 9 * (j - 1) + d

def to_grid(str):
    parts = [str[i:i+9] for i in range(0, len(str), 9)]
    return parts

def naive_sudoku_clauses():
    """
    Create the (11745) Sudoku clauses, and return them as a list.
    Note that these clauses are *independent* of the particular
    Sudoku puzzle at hand.
    """
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                for dp in range(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    # ensure rows and columns have distinct values
    for i in range(1, 10):
        valid([(i, j) for j in range(1, 10)], res)
        valid([(j, i) for j in range(1, 10)], res)
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid([(i + k % 3, j + k // 3) for k in range(9)], res)

    assert len(res) == 81 * (1 + 36) + 27 * 324

    return res

def variables():
    """
    Create the (11745) Sudoku clauses, and return them as a list.
    Note that these clauses are *independent* of the particular
    Sudoku puzzle at hand.
    """
    res = []
    cell_u = []
    row_u = []
    col_u = []
    block_u = []
    cell_d = []
    row_d = []
    col_d = []
    block_d = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)

            cell_d.append([(i, j, d) for d in range(1,10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                res.append((i, j, d) )
            for d in range(1, 9):
                for dp in range(d + 1, 10):
                    cell_u.append([(i, j, -d), (i, j, -dp)])

    # ensure rows and columns have distinct values
    # for i in range(1, 10):
    #     valid_eff([(i, j) for j in range(1, 10)], res)
    #     valid_eff([(j, i) for j in range(1, 10)], res)

    for r in range(1, 10):
        for v in range(1, 10):
            row_d.append([(c,r, v) for c in range(1,10)])
            col_d.append([(r, c, v) for c in range(1,10)])
            for c in range(1,9):

                for cp in range(c+1,10):
                    row_u.append([(r, c, -v), (r,cp, -v)])
                    col_u.append([(c, r, -v), (cp,r, -v)])

    for r_o in [1,4,7]:
        for c_o in [1,4,7]:
            for v in range(1, 10):
                block_d.append([((r_o),(c_o), v) for r in range(1,4) for c in range(1,4)])
                for r in range(1, 10):
                    for c in range(r+1,10):
                        block_u.append([((r_o+(r%3)),(c_o+(r%3)), -v), ((r_o+(c%3)),(c_o+(c%3)), -v)])
    # # ensure 3x3 sub-grids "regions" have distinct values
    # for i in 1, 4, 7:
    #     for j in 1, 4 ,7:
    #         valid([(i + k % 3, j + k // 3) for k in range(9)], res)
    #
    # assert len(res) == 81 * (1 + 36) + 27 * 324

    return res, cell_d, row_d, col_d, block_d, cell_u, row_u, col_u, block_u


def valid_eff(cells, clauses):
    # Append 324 clauses, corresponding to 9 cells, to the result.
    # The 9 cells are represented by a list tuples.  The new clauses
    # ensure that the cells contain distinct values.
    for i, xi in enumerate(cells):
        for j, xj in enumerate(cells):
            if i < j:
                for d in range(1, 10):
                    clauses.append([(xi[0], xi[1], -d), (xj[0], xj[1], -d)])


def small_arrow(clauses, V):
    res = []
    for x in clauses:
        x = [i for i in x if i not in V]
        if x:
            res.append(x)
    clauses = [[(x[0],x[1],x[2]) for x in y] for y in res]
    return clauses

def big_arrow_min(clauses,literals):
    res = []
    literals = [(x[0],x[1],-x[2]) for x in literals]
    for x in clauses:
        if not set(x) & set(literals):
            res.append(x)
    return(res)

def big_arrow_plus(clauses,literals):
    res = []
    # literals = [(x[0],x[1],-x[2]) for x in literals]
    for x in clauses:
        if not set(x) & set(literals):
            res.append(x)

    return(res)

def sameCell(V_plus,clause):
    for x in V_plus:
        if (x[0],x[1]) == (clause[0],clause[1]):
            return True
    return False

def sameRow(V_plus,clause):
    for x in V_plus:
        if (x[0],x[2]) == (clause[0],clause[2]):
            return True
    return False

def sameColumn(V_plus,clause):
    for x in V_plus:
        if (x[1],x[2]) == (clause[1],clause[2]):
            return True
    return False

def sameBlock(V_plus,clause):
    for x in V_plus:
        if (x[2]) == (clause[2]):
            if x[0] <= 3:
                lucRow = 1
            else:
                lucRow = (int((x[0]-1)/3)*3)+1
            if x[1] <= 3:
                lucCol = 1
            else:
                lucCol = (int((x[1]-1)/3)*3)+1
            if (lucRow <= x[0] and clause[0] <= lucRow + 3) and  (lucCol <= x[1] and clause[1] <= lucCol + 3):
                return True
    return False


def eff_sudoku_clauses(grid):
    assigned = [(i, j, grid[i - 1][j - 1]) for j in range(1, 10) for i in range(1, 10) if grid[i - 1][j - 1]]

    # all clauses
    clauses, cell_d, row_d, col_d, block_d, cell_u, row_u, col_u, block_u = variables()
    V_min = []

    for x in clauses:
        if sameCell(assigned, x):
            V_min.append(x)
        elif sameRow(assigned, x):
            V_min.append(x)
        elif sameColumn(assigned, x):
            V_min.append(x)
        elif sameBlock(assigned, x):
            V_min.append(x)

    clauses =  [big_arrow_plus(assigned, assigned)] + big_arrow_min(cell_u+row_u+col_u+block_u, V_min) + small_arrow(cell_d+row_d+col_d+block_d, V_min)

    clauses = [[v(x[0],x[1],x[2])  if x[2] > 0 else -v(x[0],x[1],-x[2])for x in y] for y in clauses ]
    return clauses





def valid(cells, clauses):
    # Append 324 clauses, corresponding to 9 cells, to the result.
    # The 9 cells are represented by a list tuples.  The new clauses
    # ensure that the cells contain distinct values.
    for i, xi in enumerate(cells):
        for j, xj in enumerate(cells):
            if i < j:
                for d in range(1, 10):
                    clauses.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

def generate_clauses(grid, type, encoding):
    if type == 'nor':
        grid = to_grid(grid)
    if encoding == 'naive':
        clauses = naive_sudoku_clauses()
    else:
        if(type == 'color'):
            grid1 = col_convert_to_grid(grid)
        else: grid1 = convert_to_grid(grid)
        clauses = eff_sudoku_clauses(grid1)


    colors = {'red': [], 'blue' : [], 'yellow': [], 'green': [], 'pink': [],
        'black': [], 'lblue': [], 'brown': [], 'grey': []}
    if(type == 'color'):
        grid = convert_to_grid(grid)
        for i in range(1,10):
            for j in range(1,10):
                d = grid[i-1][j-1]
                colors[d[1]].append((i,j))
        for c, values in colors.items():
            c1 = []
            for row, col in values:
                c1.append((row, col))
            valid(c1, clauses)
        # compute regular sudoku clauses using the grid without colors
        reg_grid = [[0 for x in range(9)] for y in range(9)]
        for i in range(1, 10):
            reg_grid[i-1] = [i[0] for i in grid[i-1]]
        grid = reg_grid

    if(type == 'gt'):
        for pair in grid:
            pair = convert_int_to_pos(pair)
            clauses.append([v(pair[0][0], pair[0][1],l) for l in range(2,10)])
            clause = []
            for i in range(1,9):
                clause = [v(pair[1][0], pair[1][1], j) for j in range(1,i+1)]
                clause += [v(pair[0][0], pair[0][1],l) for l in range(i+2,10)]
                clauses.append(clause)
        grid = [ [0] * 9 for _ in range(9)]

    for i in range(1, 10):
        for j in range(1, 10):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal).
            if d:
                clauses.append([v(i, j, d)])
    return clauses

def read_cell(i, j):
    # return the digit of cell i, j according to the solution
    for d in range(1, 10):
        if v(i, j, d) in sol:
            return d

def solve(clauses):
    # solve the SAT problem
    sol = set(pycosat.solve(clauses, verbose=1))
    # print(sol)
    return sol

def decoder(sol):
    for i in range(1, 10):
        for j in range(1, 10):
            grid[i - 1][j - 1] = read_cell(i, j)
    return grid

def convert_to_grid(sudoku_list):
    return [sudoku_list[i::9] for i in range(10)]

def col_convert_to_grid(sudoku_list):
    l = [sudoku_list[i::9] for i in range(10)]
    return [[x[0]for x in y] for y in l]

def convert_int_to_pos(pair):
    x1 = pair[0]
    x2 = pair[1]
    def col(x):
        col = x%9
        if col == 0:
            return 9
        return col
    def row(x):
        if x%9 == 0:
            return row(x-1)
        return x//9 + 1
    return ((row(x1), col(x1)), (row(x2), col(x2)))



# if __name__ == '__main__':
#     from pprint import pprint
#
# # hard Sudoku problem, see Fig. 3 in paper by Weber
# hard = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 6, 0, 0, 0, 0, 3],
#         [0, 7, 4, 0, 8, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 3, 0, 0, 2],
#         [0, 8, 0, 0, 4, 0, 0, 1, 0],
#         [6, 0, 0, 5, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 7, 8, 0],
#         [5, 0, 0, 0, 0, 9, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 4, 0]]
#
# # puzzles = gen_colour_puzzles(10)
# # print("Puzzle nr: ", puzzles[1][1])
# # puzzle1 = convert_to_grid(puzzles[1][2])
# # solve(puzzle1, 'color')
#
# # puzzles_gt = gen_gt_puzzles(10)
# puzzle_gt = puzzles_gt[1][2]
# print('Puzzle number: ', puzzles_gt[1][1])
# solve(generate_clauses(puzzle_gt, 'gt', 'naive'))
# print(puzzle_gt)
