from sudoku_decoder import*
from SATsolver_zchaff import*

from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time
import pickle


# path to the directory (relative or absolute)
dirpath = sys.argv[1] if len(sys.argv) == 2 else r'.' + '/pickle'


def get_pickles():
    # get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)

    # leave only regular files, insert creation date
    entries = ((stat[ST_CTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))
    #NOTE: on Windows `ST_CTIME` is a creation date
    #  but on Unix it could be something else
    #NOTE: use `ST_MTIME` to sort by a modification date

    files = (sorted(entries)[-3:])
    col_sudoku = pickle.load(open(files[0][1], 'rb'))
    norm_sudoku = pickle.load(open(files[1][1], 'rb'))
    gt_sudoku = pickle.load(open(files[2][1], 'rb'))
    return col_sudoku, norm_sudoku, gt_sudoku

if __name__ == '__main__':
    col_sudoku, norm_sudoku, gt_sudoku = get_pickles()
    col_clauses = [generate_clauses(i[2], 'color') for i in col_sudoku]
    norm_clauses = [generate_clauses(i[2], 'norm') for i in norm_sudoku]
    gt_clauses = [generate_clauses(i[2], 'gt') for i in gt_sudoku]
    print(gt_clauses[0])
    col_results = []
    for clauses in col_clauses:
        col_results.append(testKb(clauses))
    norm_results = []
    for clauses in norm_clauses:
        norm_results.append(testKb(clauses))
    gt_results = []
    for clauses in gt_clauses:
        gt_results.append(testKb(clauses))
    # Now write to grid and return statistics.
