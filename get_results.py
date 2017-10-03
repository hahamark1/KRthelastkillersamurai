from sudoku_decoder import*
from SATsolver_zchaff import*
import pycosat

from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time
from datetime import datetime


# path to the directory (relative or absolute)
dirpath = sys.argv[1] if len(sys.argv) == 2 else r'.' + '/pickle'

def get_pickles():
    # get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)
    # leave only regular files, insert creation date
    entries = ((stat[ST_CTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))
    files = (sorted(entries)[-3:])
    col_sudoku = pickle.load(open(files[0][1], 'rb'))
    norm_sudoku = pickle.load(open(files[1][1], 'rb'))
    gt_sudoku = pickle.load(open(files[2][1], 'rb'))
    return col_sudoku, norm_sudoku, gt_sudoku

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def empty_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def average_dict(list):
    avg_dict = {}
    for dict in list:
        for key, value in dict.items():
            if is_number(value):
                if key in avg_dict:
                    avg_dict[key] += float(value)
                else:
                    avg_dict[key] = float(value)
    return {key: value / len(list) for key, value in avg_dict.items()}

def data_to_dict(data):
    # print(data)
    data = str(data)
    data = data.split('\\n')
    data = [x.split('\\t') for x in data]
    data = [x for x in data if 1 < len(x)]
    data = [[x.replace('\\t', "")for x in y if x] for y in data]
    return {x:y for x,y in data[1:]}

if __name__ == '__main__':
    folder = 'cnfFiles/'
    empty_folder(folder)
    col_sudoku, norm_sudoku, gt_sudoku = get_pickles()
    # print(len(col_sudoku),len(gt_sudoku))
    # col_clauses_naive = [[generate_clauses(i[2], 'color', 'naive'),i[0],i[1]] for i in col_sudoku]
    # norm_clauses_naive = [[generate_clauses(i[2], 'nor', 'naive'),i[0],i[1]] for i in norm_sudoku]
    # gt_clauses_naive = [[generate_clauses(i[2], 'gt', 'naive'),i[0],i[1]] for i in gt_sudoku]
    # col_clauses_eff = [[generate_clauses(i[2], 'color', 'eff'),i[0],i[1]] for i in col_sudoku[:1]]
    # norm_clauses_eff = [[generate_clauses(i[2], 'nor', 'eff'),i[0],i[1]] for i in norm_sudoku]
    # gt_clauses_eff = [[generate_clauses(i[2], 'gt', 'eff'),i[0],i[1]] for i in gt_sudoku]
    # print(gt_clauses[0])
    # print(len(col_clauses_naive[0]))
    # print(len(col_clauses_eff[0]))
    col_naive_results = []
    l = 0
    for clauses in  col_sudoku:
        l+=1
        # print(clauses)
        col_naive_results.append((clauses[0], clauses[1],data_to_dict(testKb(generate_clauses(clauses[2], 'color', 'naive'),"cnf_col_naive_%s.cnf" % l)),"cnf_col_naive_%s.cnf" % l))
    col_results_eff = []
    l = 0
    # for clauses in col_clauses_eff[:1]:
    #     l+=1
    #     # print(clauses)
    #     col_results_eff.append((clauses[1], clauses[2],data_to_dict(testKb(clauses[0],"cnf_col_eff_%s.cnf" % l)),"cnf_col_eff_%s.cnf" % l))
    norm_results_naive = []
    l = 0
    for clauses in norm_sudoku:
        l+=1
        norm_results_naive.append((clauses[0], clauses[1],data_to_dict(testKb(generate_clauses(clauses[2], 'nor', 'naive'),"cnf_nor_naive_%s.cnf" % l)),"cnf_nor_naive_%s.cnf" % l))
    gt_results_naive = []
    l = 0
    for clauses in gt_sudoku:
        l+=1
        gt_results_naive.append((clauses[0], clauses[1], data_to_dict(testKb(generate_clauses(clauses[2], 'gt', 'naive'),"cnf_gt_naive_%s.cnf" % l)),"cnf_gt_naive_%s.cnf" % l))

    # Now write to grid and return statistics.
    # solutions = decoder(clauses)

    average_results_nor_naive = average_dict([x[2] for x in norm_results_naive])
    average_results_col_naive = average_dict([x[2] for x in col_naive_results])
    average_results_gt_naive = average_dict([x[2] for x in gt_results_naive])
    print(average_results_nor_naive)
    print(len(col_clauses_naive))
    print(average_results_col_naive)
    print(len(norm_clauses_naive))

    print(average_results_gt_naive)
    print(len(gt_clauses_naive))
    outcomes = [('nor, col, gt'), average_results_nor_naive, average_results_col_naive, average_results_gt_naive]
    pickle.dump(outcomes, open("outcomes.p", "wb"))
    # print(average_results_col_naive)
