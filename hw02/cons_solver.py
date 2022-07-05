#!/usr/bin/python3
import math
import os
import sys
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



class Crossword_Solver():
    def __init__(self, crossword):
        self.crossword = crossword
        # self.domains = {
        #     var: self.crossword.words.copy()
        #     for var in self.crossword.variables
        # }
        # self.domains = {
        #     var: [ x for x in self.crossword.words if len(x) == var ]
        #     # for var in self.crossword.variables
        # }
        #
        # self.domains = {
        #
        # domain_list = []
        # for var in self.crossword.variables:
        #     for word in self.crossword.words:
        #         if len(word) == var.length:
        #             domain_list.append(word)
        #             var: self.domains = domain_list
        # }

    def assignment_complete(self, assignment):
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def is_consistent(self, assignment):
        if len(assignment) == 1:
            return True
        for var in assignment:
            copy = assignment.copy()
            copy.pop(var)

            for var2 in copy:
                if assignment[var] == assignment[var2]:
                    return False
                crossing = self.crossword.intersections((var, var2))
                if crossing is not None:
                    x = crossing[0]
                    y = crossing[1]
                    if assignment[var][x] != assignment[var2][y]:
                        return False

        return True
# def domain_updater(word_file):
#
#     words = open(word_file, 'r').read().splitlines()
#
#     for
#
#     domain = []


def solve_crossword(xword_file, word_file):

    crossword = Crossword(xword_file, word_file)

    # crossword.print_input_files()
    # crossword.print_grids()
    # crossword.print_xword_and_words()
    crossword.print_words_to_solve()

    # crossword.print_domains()

    crossword_solver = Crossword_Solver(crossword)
    # print(f'{crossword_solver.domains=}')
    # crossword.find_word_locations()


if __name__ == "__main__":

    xword_file, word_file = parse_files()

    solve_crossword(xword_file, word_file)

    sys.exit()


# for recursive, call backtrack from inside backtrack

# assignment aka solution says what each word should be - to each var

# every time backtrack is called, partial solution is called

# on outer loop, the entire solution is returned



# each var is say 1-down

# for each value in domain list - has to be same number of letters as blank

# violations - intersections have to work ok


# keep class for keeping track of variable



# do the same thing here






"""
./cons_solver.py ./inputData/xword00.txt ./inputData/dictionary_small.txt



15 15
 1  2  3  4  X  5  6  7  8  X  X  9 10 11 12
13  _  _  _  X 14  _  _  _ 15  X 16  _  _  _
17  _  _  _ 18  _  _  _  _  _ 19  _  _  _  _
20  _  _  _  _  _  X 21  _  _  _  X 22  _  _
 X  X  X  X 23  _ 24  _  _  X 25 26  _  _  _
27 28 29 30  _  _  _  _  _  X 31  _  _  X  X
32  _  _  _  X 33  _  _  X 34  _  _  _ 35  X
36  _  _  _ 37  _  _  X 38  _  _  _  _  _ 39
 X 40  _  _  _  _  X 41  _  _  X 42  _  _  _
 X  X 43  _  _  X 44  _  _  _ 45  _  _  _  _
46 47  _  _  _  X 48  _  _  _  _  X  X  X  X
49  _  _  X 50 51  _  _  X 52  _ 53 54 55 56
57  _  _ 58  _  _  _  _ 59  _  _  _  _  _  _
60  _  _  _  X 61  _  _  _  _  X 62  _  _  _
63  _  _  _  X  X 64  _  _  _  X 65  _  _  _

"""