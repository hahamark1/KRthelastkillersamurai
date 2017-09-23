import pickle
import requests
import time
from datetime import datetime
import random
from bs4 import BeautifulSoup

BASEURL = "http://www.menneske.no/sudoku/%s/eng/showpuzzle.html?diff=%e?number=%d"
COUNTGTURL = "http://www.menneske.no/sudokugt/eng/showpuzzle.html?diff=%e?number=%d"
COUNTCOLURL = "http://www.menneske.no/sudoku/dg/3/eng/showpuzzle.html?diff=%e?number=%d"
COUNTURL = "http://www.menneske.no/sudoku/eng/showpuzzle.html?diff=%e?number=%d"
SOLUTIONURL = "http://www.menneske.no/sudoku/eng/solution.html?number=%d"
SOLUTIONCOLURL = "http://www.menneske.no/sudoku/dg/3/eng/solution.html?number=%d"
SOLUTIONGTURL = "http://www.menneske.no/sudokugt/eng/solution.html?number=%d"

def gt(x,direc):
    if direc == 'L':
        return (x-1,x)
    if direc == 'R':
        return (x+1,x)
    if direc == 'B':
        return (x+9,x)
    if direc == 'T':
        return (x-9,x)

def solution(num,tp):
    if tp == 'gt':
        BASE = SOLUTIONGTURL
        grid = 'grid2'
    elif tp == 'col':
        BASE = SOLUTIONCOLURL
        grid = 'grid'
    else:
        BASE = SOLUTIONURL
        grid = 'grid'
    url = BASE % int(num)
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')
    print(url)
    puzzle = [x.find_all('td') for x in soup.find_all('tr',{"class": grid})]
    puzzle = [x for y in puzzle for x in y]
    sudoku = [int(x.getText()) if x.getText() !=u'\xa0' else 0 for x in puzzle]
    return sudoku

def gen_gt_puzzles(n):
    puzzles = []
    for p in range(1,9):
        num = random.sample(range(1000), int(n/8))
        for i in num:
            # print(type(i))
            # print(type(j))
            url = COUNTGTURL % (p,i)
            page = requests.get(url).content
            soup = BeautifulSoup(page, 'html.parser')
            puzzle = soup.find_all('tr',{"class": 'grid2'})
            diff = str(soup.find('div',{"class": 'grid2'})).split('<br/>')[1][12:]
            numb = str(soup.find('div',{"class": 'grid2'})).split('</table>')[1].split('<br/>')[0][23:]
            print(numb)
            row = 0
            blocks = [str(j)[19:].split('.png')[0] for x in puzzle for j in x.find_all('td')]
            clauses = []
            clauses = [gt(idx+1, direc) for idx, o in enumerate(blocks) for direc in o[2:] if len(o)>2]
            gtsudoku = (diff, i, clauses)
            puzzles.append(gtsudoku)
            answer = solution(numb,'gt')
            pzfile = open('gtpuzzles/'+ str(i) + '_' + diff + '.puzzle','w')
            for clause in clauses:
                pzfile.write(str(clauses))
            pzfile.close()
            ansfile = open('gtpuzzles/' + str(i) + '_' + diff + '.ans','w+')
            for l in answer:
                ansfile.write(str(l))
            ansfile.close()

    pickle.dump(puzzles, open("pickle/gtsudokus-%s.p" % datetime.now(), "wb"))
    return puzzles
colours = {'#ff6666' : 'red', '#6666ff':'blue' ,'#ffff66':'yellow', '#ff66ff':'pink', '#66ff66':'green' , '#66ffff':'lblue' , '#666666': 'black', '#ffcccc': 'brown', '#ccccff': 'grey' }

def col(col):
    return colours[col]

def gen_colour_puzzles(n):
    puzzles = []
    for j in range(1,9):
        # j = int(j)
        num = random.sample(range(1000), int(n/8))
        for i in num:
            url = COUNTCOLURL % (j,i)
            page = requests.get(url).content
            soup = BeautifulSoup(page, 'html.parser')
            puzzle = [x.find_all('td') for x in soup.find_all('tr',{"class": 'grid'})]
            puzzle = [x for y in puzzle for x in y]
            diff = str(soup.find('div',{"class": 'grid'})).split('<br/>')[3][12:]
            numb = str(soup.find('div',{"class": 'grid'})).split('</table>')[1].split('<br/>')[0][23:]
            row = 0
            sudoku = [(int(x.getText()), col(x['style'][18:-1])) if x.getText() !=u'\xa0' else (0,col(x['style'][18:-1])) for x in puzzle]
            gtsudoku = (diff, i, sudoku)
            puzzles.append(gtsudoku)
            answer = solution(numb,'col')
            pzfile = open('colpuzzles/' + str(i) + '_' + diff + '.puzzle','w+')
            # sudoku1 = [str(x) for x in sudoku]
            # for x in sudoku1
            for l in sudoku:
                pzfile.write(str(l))
            pzfile.close()
            ansfile = open('colpuzzles/' + str(i) + '_' + diff + '.ans','w+')
            for l in answer:
                ansfile.write(str(l))
            ansfile.close()

    pickle.dump(puzzles, open("pickle/colsudokus-%s.p" % datetime.now(), "wb"))
    return puzzles

def gen_puzzles(n):
    puzzles = []
    for j in range(1,9):
        num = random.sample(range(1000), int(n/8))
        for i in num:
            url = COUNTURL % (j,i)
            page = requests.get(url).content
            soup = BeautifulSoup(page, 'html.parser')
            puzzle = [x.find_all('td') for x in soup.find_all('tr',{"class": 'grid'})]
            puzzle = [x for y in puzzle for x in y]
            diff = str(soup.find('div',{"class": 'grid'})).split('<br/>')[3][12:]
            numb = str(soup.find('div',{"class": 'grid'})).split('</table>')[1].split('<br/>')[0][23:]
            row = 0
            sudoku = [int(x.getText()) if x.getText() !=u'\xa0' else 0 for x in puzzle]
            gtsudoku = (diff, i, sudoku)
            puzzles.append(gtsudoku)
            answer = solution(numb,'nor')
            pzfile = open('norpuzzles/'+str(i) + '_' + diff + '.puzzle','w')
            for l in sudoku:
                pzfile.write(str(l))
            pzfile.close()
            ansfile = open('norpuzzles/' + str(i) + '_' + diff + '.ans','w+')
            for l in answer:
                ansfile.write(str(l))
            ansfile.close()
    pickle.dump(puzzles, open("pickle/normsudokus-%s.p" % datetime.now(), "wb"))
    return puzzles

if __name__ == '__main__':
    gen_colour_puzzles(8)
    gen_puzzles(8)
    gen_gt_puzzles(8)
