#!/usr/bin/python3
import os
import sys
import time
from copy import deepcopy
from functools import wraps
import operator




def parse_files():
    # read user input on what word list and crossword to solve
    # ac3 optional
    kbase_file = sys.argv[1]

    for file in [kbase_file]:
        if not os.path.isfile(file):
            print(f'file not found: {file}\n')
            sys.exit("run: python forward_chain.py kb_00.txt ")

    with open(kbase_file, 'r') as fi:
        for line in fi:
            fields = line.strip().split(' ')
            print(f'{fields}')

    return kbase_file





if __name__ == "__main__":

    kbase_file = parse_files()