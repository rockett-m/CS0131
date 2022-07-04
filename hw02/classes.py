import re
import sys

import numpy as np
from collections import OrderedDict

class Variable():

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, row, col, length, direction, name):
        self.row =       row
        self.col =       col
        self.length =    length
        self.direction = direction.upper()
        self.name =      name

    def __hash__(self):  # dictionary
        return hash((self.row, self.col, self.length, self.direction, self.name))

    def __eq__(self, other):  # intersection
        equality_bool = False

        if ((self.row == other.row) and
            (self.col == other.col) and
            (self.length == other.length) and
            (self.direction == other.direction) and
            (self.name == other.name)): equality_bool = True

        return equality_bool

    def __str__(self):
        return f"{self.row}, {self.col}, {self.length}, {self.direction}, {self.name}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.row}, {self.col}, {self.length}, {direction}, {self.name})"


class Crossword():
    def __init__(self, xword_file, word_file):
        self.xword_file = xword_file
        self.word_file =  word_file

        self.words = open(word_file, 'r').read().splitlines()
        self.orig_xword = (open(xword_file, 'r').read().splitlines())[1:]  # skip dimensions

        with open(xword_file, 'r') as fi:

            grid_words = np.zeros((0, 0))
            ccount = 0; lcount = -1

            for line in fi:
                if lcount == -1:  # zeros grid to match input dimensions
                    result = re.match(r'\s*(\d+)\s+(\d+)\s*', line)
                    if result:
                        self.width = int(result.group(1)); self.height = int(result.group(2))
                    grid_words = np.zeros((self.width, self.height))  # populate with 1 if char belongs
                    self.grid_numbers = np.zeros((self.width, self.height))  # populate with 1 if char belongs
                    self.grid_numbers = self.grid_numbers.astype('int')

                else:  # add 1's to grid x,y coords if letter belongs there
                    line = line.strip(); fields = line.split(' '); new_fields = []
                    for i in fields:
                        if i != '':
                            new_fields.append(i)

                    for char in new_fields:  # build word list horizontal of words in a line
                        if re.search(r'\d+', char):  # word begin
                            # print(f'line: {lcount}; char: {ccount}; char: >{char}<; line: {line};')
                            grid_words[lcount, ccount] = 2
                            self.grid_numbers[lcount, ccount] = int(char)
                            ccount += 1
                        elif re.search('_', char):
                            # print(f'line: {lcount}; char: {ccount}; char: >{char}<; line: {line};')
                            grid_words[lcount, ccount] = 1
                            self.grid_numbers[lcount, ccount] = 0
                            ccount += 1
                        elif re.search(r'X', char):  # end and reset counts
                            self.grid_numbers[lcount, ccount] = -1
                            ccount += 1
                ccount = 0; lcount += 1


        print(f'{self.grid_numbers=}')

        self.variables = set()

        """
        # ==  #
        X == -1
        _ ==  0
        """

        store_words = []
        # store_words = [[row, col, length, direction='Across'|'Down'],[row, col, length, direction='Across'|'Down']]

        for row in range(self.height):
            word_index = []; name = ''

            for col_idx in range(self.width):

                char = self.grid_numbers[row][col_idx]

                if (char > 0) and ((col_idx == 0) or (len(word_index) == 0)):
                    name = f'{char}-ACROSS'
                    word_index = [row, col_idx, 1, f'{char}-ACROSS']

                elif (char >= 0) and (len(word_index) > 0):  # add length   if _ or #
                    word_index[2] += 1
                    if col_idx == (self.width - 1):
                        store_words.append(word_index)
                        self.variables.add(Variable(row=word_index[0], col=word_index[1], length=word_index[2], direction='ACROSS', name=name))
                        word_index = []

                elif (char == -1) and (col_idx != self.width - 1) and (len(word_index) > 0):  # stop - end
                    store_words.append(word_index)
                    self.variables.add(Variable(row=word_index[0], col=word_index[1], length=word_index[2], direction='ACROSS', name=name))
                    word_index = []

                elif (char == -1) and (col_idx == self.width - 1) and (len(word_index) > 0):  # stop - end
                    store_words.append(word_index)
                    self.variables.add(Variable(row=word_index[0], col=word_index[1], length=word_index[2], direction='ACROSS', name=name))
                    word_index = []

                elif (char == -1) and (len(word_index) == 0):  # stop - end
                    word_index = []

        for i in store_words:
            print(i)

        print(f'{len(store_words)}')


        store_words = []

        for row in range(self.height):
            word_index = []; name = ''

            for col_idx in range(self.width):

                char = self.grid_numbers[col_idx][row]

                if (char > 0) and ((col_idx == 0) or (len(word_index) == 0)):
                    name = f'{char}-DOWN'
                    word_index = [col_idx, row, 1, f'{char}-DOWN']

                elif (char >= 0) and (len(word_index) > 0):  # add length   if _ or #
                    word_index[2] += 1
                    if col_idx == (self.width - 1):
                        store_words.append(word_index)
                        self.variables.add(Variable(row=word_index[0], col=word_index[1], length=word_index[2], direction='DOWN', name=name))
                        word_index = []

                elif (char == -1) and (col_idx != self.width - 1) and (len(word_index) > 0):  # stop - end
                    store_words.append(word_index)
                    self.variables.add(Variable(row=word_index[0], col=word_index[1], length=word_index[2], direction='DOWN', name=name))
                    word_index = []

                elif (char == -1) and (col_idx == self.width - 1) and (len(word_index) > 0):  # stop - end
                    store_words.append(word_index)
                    self.variables.add(Variable(row=word_index[0], col=word_index[1], length=word_index[2], direction='DOWN', name=name))
                    word_index = []

                elif (char == -1) and (len(word_index) == 0):  # stop - end
                    word_index = []

        for i in store_words:
            print(i)

        print(f'{len(store_words)}')


    def print_input_files(self):
        print(f'\n{self.width} x {self.height} crossword detected\n')
        print(f'\n{self.xword_file = }\n')
        [ print(x) for x in open(self.xword_file, 'r').read().splitlines() ]

        print(f'\n{self.word_file = }\n')
        [ print(x) for x in open(self.word_file, 'r').read().splitlines() ]; print()

    def print_xword_and_words(self):
        print(f'\n{self.words = }\n')
        print(f'\n{self.orig_xword = }\n')

    def print_grids(self):
        print(f'\nself.grid_horz:\n{self.grid_horz}\n')
        print(f'\nself.grid_vert:\n{self.grid_vert}\n')

    def print_words_to_solve(self):
        print(f'\nwords to solve: {len(self.variables)}\n{self.variables = }\n')
        # [ print(i) for i in self.variables ]
        vert_words = 0; across_words = 0

        for var in self.variables:
            if var.direction == 'DOWN': vert_words += 1
            elif var.direction == 'ACROSS' : across_words += 1

        print(f'\n{vert_words = }\n'); print(f'\n{across_words = }\n')



# word class / streak - start location, length, direction

# int start row, start col
# constraint - relationship between words

# intersection - constraint (letter needs to be the same)

# domain - list of strings

# create word objects
# create constraint objects

# then do constraint satisfaction

# make Variable (word class)
# store number - like 0, 1, 2
# down/across
# bool /
#

# constraint
# intersection letters
# if intersection works between variable objects - consistent
# else fails