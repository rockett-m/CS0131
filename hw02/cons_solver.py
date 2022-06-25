#!/usr/bin/python3
import math
import os
import sys
import re
import time
from collections import OrderedDict
from functools import wraps
import networkx as nx
from math import *
import heapq
import numpy as np

global WIDTH, HEIGHT


# run as ./cons_solver.py ./inputData/xword00.txt ./inputData/dictionary_small.txt
def timeit(func):
    @wraps(func)
    def measure_time(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("@timefn: {} took {} seconds.\n".format(func.__name__, round(end_time - start_time, 2)))
        return result
    return measure_time


def print_dict(my_dict: dict):
    for key, value in my_dict.items():
        print(f'key: {key}  :  value: {value}')


def parse_files():
    xword_file = sys.argv[1]
    dict_file = sys.argv[2]

    for file in [xword_file, dict_file]:
        if not os.path.isfile(file):
            print(f'file not found: {file}\n')
            sys.exit()

    return xword_file, dict_file


def read_word_file(dict_file):

    word_dict = OrderedDict()

    with open(dict_file, 'r') as fi:
        for line in fi:
            line = line.strip()
            word_dict[line] = len(line)  # set word equal to word length

    return word_dict


def read_xword_file(xword_file):

    # xword_dict = OrderedDict()

    with open(xword_file, 'r') as fi:

        global WIDTH, HEIGHT

        WIDTH = HEIGHT = ccount = 0
        lcount = -1

        grid_valid = np.zeros((0, 0))
        grid_words = np.zeros((0, 0))

        for line in fi:
            if lcount == -1:  # zeros grid to match input dimensions
                result = re.match(r'\s+(\d)\s+(\d)\s*', line)
                if result:
                    WIDTH =  int(result.group(1))
                    HEIGHT = int(result.group(2))
                grid_valid = np.zeros((WIDTH, HEIGHT))  # populate with 1 if char belongs
                grid_words = np.zeros((WIDTH, HEIGHT))  # populate with 1 if char belongs

            else:  # add 1's to grid x,y coords if letter belongs there
                line = line.strip()
                fields = line.split(' ')

                for char in fields:  # build word list horizontal of words in a line
                    char.rstrip('\n')

                    if re.search(r'\d+', char):
                        # print(f'line: {lcount}; char: {ccount}; char: >{char}<; line: {line};')
                        grid_valid[lcount, ccount] = 1
                        grid_words[lcount, ccount] = 2
                        ccount += 1

                    elif re.search('_', char):  # word begin
                        # print(f'line: {lcount}; char: {ccount}; char: >{char}<; line: {line};')
                        grid_valid[lcount, ccount] = 1
                        grid_words[lcount, ccount] = 1
                        ccount += 1

                    elif re.search(r'X', char):  # end and reset counts
                        ccount += 1

                    elif re.search(r' ', char):
                        pass

            ccount = 0; lcount += 1

    # print(f'grid_valid:\n{grid_valid}\n')
    print(f'grid_words:\n{grid_words}\n')

    return grid_words


def crossword_solver(word_dict, grid_words):

    answer = grid_words.copy()

    # for word in word_dict.sorted():
    row_idx = 0
    for row in grid_words:

        col_idx = streak = start_col_idx = end_col_idx = prev_item = prev_col_idx = 0
        for item in row:
            item = int(item)

            if (item == 0) and (streak > 0):  # at least one letter position before here
                end_col_idx = col_idx - 1  # prior col - last letter location
                print(f'streak {streak} over: begin @ {row_idx, start_col_idx} end @ {row_idx, end_col_idx}')

                for word in word_dict.keys():
                    if len(word) == streak:
                        

            # elif (item == 0) and (streak == 0):  # don't care about 'X' without prior letters
            #     start_col_idx = end_col_idx = 0

            elif item > 0:  # start of word or blank

                if streak > 0:  # word has been detected already
                    streak += 1

                # prev was border or an 'X' and current is a '#'
                if (item == 2) and ((prev_item == 0) or (prev_col_idx == 0)):  # beginning of horz word - must start from boundary
                    streak = 1
                    start_col_idx = col_idx

                if (col_idx == WIDTH-1) and (streak > 0):  # word over due to end of line
                    end_col_idx = col_idx
                    print(f'streak {streak} over: begin @ {row_idx, start_col_idx} end @ {row_idx, end_col_idx}')

                    for word in word_dict.keys():
                        if len(word) == streak:


            prev_item = item
            prev_col_idx = col_idx

            col_idx += 1
        row_idx += 1


if __name__ == "__main__":

    xword_file, dict_file = parse_files()

    word_dict = read_word_file(dict_file)  # dict of all  words : lengths

    grid_words = read_xword_file(xword_file)  #  np matrix  with 2 = #;  1 = blank;  0 = X

    crossword_solver(word_dict, grid_words)
    # print_dict(word_dict)
    # print_dict(xword_dict)

    sys.exit()



"""
./cons_solver.py ./inputData/xword00.txt ./inputData/dictionary_small.txt

 7 7
 1  _  _  _  _  _  2
 _  X  X  X  X  X  _
 _  X  X  X  X  X  _
 _  X  X  X  X  X  _
 _  X  X  X  X  X  _
 _  X  X  X  X  X  _
 3  _  _  _  _  _  _

grid_words : 

[[2. 1. 1. 1. 1. 1. 2.]
 [1. 0. 0. 0. 0. 0. 1.]
 [1. 0. 0. 0. 0. 0. 1.]
 [1. 0. 0. 0. 0. 0. 1.]
 [1. 0. 0. 0. 0. 0. 1.]
 [1. 0. 0. 0. 0. 0. 1.]
 [2. 1. 1. 1. 1. 1. 1.]]
"""
