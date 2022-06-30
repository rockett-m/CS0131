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

from classes import Variable, Crossword

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
    word_file = sys.argv[2]

    for file in [xword_file, word_file]:
        if not os.path.isfile(file):
            print(f'file not found: {file}\n')
            sys.exit("run: python cons_solver.py xword00.txt dictionary_small.txt ")

    return xword_file, word_file


def crossword_solver(word_dict, grid_horz):

    grid_vert = grid_horz.transpose()
    crossword = Crossword(word_dict, grid_horz, grid_vert)


    word = Variable(direction, length, x, y)

    # for word in word_dict.sorted():
    row_idx = 0
    for row in grid_horz:

        col_idx = streak = start_col_idx = end_col_idx = prev_item = prev_col_idx = 0
        for item in row:
            item = int(item)

            if (item == 0) and (streak > 0):  # at least one letter position before here
                end_col_idx = col_idx - 1  # prior col - last letter location
                print(f'streak {streak} over: begin @ {row_idx, start_col_idx} end @ {row_idx, end_col_idx}')

                for word in word_dict.keys():  # fill in words that could fit
                    if len(word) == streak:
                        pass

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
                            pass

            prev_item = item
            prev_col_idx = col_idx

            col_idx += 1
        row_idx += 1




    # for recursive, call backtrack from inside backtrack

    # assignment aka solution says what each word should be - to each var

    # every time backtrack is called, partial solution is called

    # on outer loop, the entire solution is returned



    # each var is say 1-down

    # for each value in domain list - has to be same number of letters as blank

    # violations - intersections have to work ok


    # keep class for keeping track of variable



    # do the same thing here


def solve_crossword(xword_file, word_file):

    crossword = Crossword(xword_file, word_file)

    crossword.print_input_files()
    crossword.print_grids()
    crossword.print_xword_and_words()


if __name__ == "__main__":

    xword_file, word_file = parse_files()

    solve_crossword(xword_file, word_file)

    sys.exit()


    crossword_solver(word_dict, grid_horz=grid_words)




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
 
 grid_words_vert : 

 [[2. 1. 1. 1. 1. 1. 2.]
  [1. 0. 0. 0. 0. 0. 1.]
  [1. 0. 0. 0. 0. 0. 1.]
  [1. 0. 0. 0. 0. 0. 1.]
  [1. 0. 0. 0. 0. 0. 1.]
  [1. 0. 0. 0. 0. 0. 1.]
  [2. 1. 1. 1. 1. 1. 1.]]
"""
