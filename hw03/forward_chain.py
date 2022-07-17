#!/usr/bin/python3
import os
import sys
import time
from copy import deepcopy
from functools import wraps
import operator
from collections import OrderedDict
import re


kb_dict = OrderedDict()


def parse_files():
    # read user input on what word list and crossword to solve
    # ac3 optional
    kbase_file = sys.argv[1]

    if not os.path.isfile(kbase_file):
        print(f'file not found: {kbase_file = }\n')
        sys.exit("run: python forward_chain.py kb_00.txt ")


    with open(kbase_file, 'r') as fi:

        symbols_list = []; clauses_list = []
        symbols_count = 0; condional_count = 0

        line_count = 0
        for line in fi:
            line = line.strip()       # strip newline
            fields = line.split(' ')  # separate fields by spaces

            if len(fields) == 1:      # symbol if only one field per line
                symbols_count += 1
                symbols_list.append(fields[0])
            else:
                condional_count += 1
                clauses_list.append(line)

            for field in fields:
                if re.search('p\d+', field):
                    if field not in kb_dict.keys():
                        kb_dict[field] = ''

            line_count += 1

        print(f'\nKB has {condional_count} conditional clauses and {symbols_count} propositional symbols.')
        print(f'\nClauses:\n'); [print(x) for x in clauses_list]
        print(f'\nSymbols:\n'); [print(x) for x in symbols_list]

    return kbase_file





if __name__ == "__main__":

    kbase_file = parse_files()