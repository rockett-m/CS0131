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


def parse_files():
    xword_file = sys.argv[1]
    dict_file = sys.argv[2]

    for file in [xword_file, dict_file]:
        if not os.path.isfile(file):
            print(f'file not found: {file}\n')
            sys.exit()

    return xword_file, dict_file


def read_file(xword_file, dict_file):

    word_dict = OrderedDict()
    xword_dict = OrderedDict()

    with open(dict_file, 'r') as fi:
        for line in fi:
            line = line.strip()
            word_dict[line] = len(line)  # set word equal to word length

    with open(xword_file, 'r') as fi:

        grid_valid = np.zeros((0, 0))
        grid_words = np.zeros((0, 0))
        lcount = -1
        width = height = ccount = 0


        for line in fi:

            if lcount == -1:  # zeros grid to match input dimensions
                result = re.match(r'\s+(\d)\s+(\d)\s*', line)
                if result:
                    width =  int(result.group(1))
                    height = int(result.group(2))
                grid_valid = np.zeros((width, height))  # populate with 1 if char belongs
                grid_words = np.zeros((width, height))  # populate with 1 if char belongs

            else:  # add 1's to grid x,y coords if letter belongs there
                # word_list = [lcount, ccount, 1, 1, 'horz']  # [line #, word_len, start_pos, end_pos, vert_horz]
                # ccount = 0
                for char in line:  # build word list horizontal of words in a line
                    char.rstrip('\n')
                    print(f'>{char}<')

                    if re.search(r'\d+', char):
                        print(f'line: {lcount}; char: {ccount}; char: {char}; line: {line};')
                        grid_valid[lcount, ccount] = 1
                        grid_words[lcount, ccount] = 2
                        ccount += 1

                    elif re.search('_', char):  # word begin
                        print(f'line: {lcount}; char: {ccount}; char: {char}; line: {line};')
                        grid_valid[lcount, ccount] = 1
                        grid_words[lcount, ccount] = 1
                        ccount += 1

                    elif re.search(r'X', char):  # end and reset counts
                        pass
                    elif re.search(r' ', char):
                        pass

                    # if ccount == height:
                    #     continue
                    # ccount += 1
            lcount += 1

    print(grid_valid)
    print(grid_words)

    return word_dict, xword_dict


def print_dict(my_dict: dict):
    for key, value in my_dict.items():
        print(f'key: {key}  :  value: {value}')


def crossword_solver(word_dict):
    pass




if __name__ == "__main__":

    xword_file, dict_file = parse_files()

    word_dict, xword_dict = read_file(xword_file, dict_file)

    # print_dict(word_dict)
    # print_dict(xword_dict)

    sys.exit()
