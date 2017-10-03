import os
import numpy as np
filenames = os.listdir()

file = open('1.ans', 'r+')
puzzles_ans = [open(name, 'r+').read() for name in filenames if name.endswith('.ans')]
puzzles_kill = [open(name, 'r+').read() for name in filenames if name.endswith('.killer')]

def last_square(x):
    last_rows = x[-3:]
    return last_rows.T[-3:].T

def first_square(x):
    last_rows = x[:3]
    return last_rows.T[:3].T

def second_square(x):
    last_rows = x[:3]
    return last_rows.T[-3:].T

def third_square(x):
    last_rows = x[-3:]
    return last_rows.T[:3].T

def read_sudoku(sudoku):
    return np.array([[int(x) for x in y.split(',')] for y in sudoku.replace('[','').replace(']','').replace(' ','').splitlines()[:-2]])

def samurai(v,w,x,y,z):
    if last_square(v) is first_square(z) and second_square(z) is third_square(w) and third_square(z) is second_square(x) and first_square(y) is last_square(z):
        return True

def read_killer(killer):
    print(killer)
    err

sudokus = [read_sudoku(puzzle) for puzzle in puzzles_ans][:10]
killer_fields = [read_killer(puzzle) for puzzle in puzzles_kill][:10]
samurai_sudokus = []
for v in sudokus:
    for w in sudokus:
        for x in sudokus:
            for y in sudokus:
                for z in sudokus:
                    for a in sudokus:
                        if samurai(v,w,x,y,z):
                            samurai_sudokus.append([v,w,x,y,z])
print(len(samurai_sudokus))

#
# for x in puzzles_kill:
#     print(x)
