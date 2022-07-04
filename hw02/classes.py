import re
import sys

import numpy as np
from collections import OrderedDict

class Variable():

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, x, y, length, direction):
        self.x =         x
        self.y =         y
        self.length =    length
        self.direction = direction.upper()

    def __hash__(self):  # dictionary
        return hash((self.x, self.y, self.length, self.direction))

    def __eq__(self, other):  # intersection
        equality_bool = False

        if ((self.x == other.x) and
            (self.y == other.y) and
            (self.length == other.length) and
            (self.direction == other.direction)): equality_bool = True

        return equality_bool

    def __str__(self):
        return f"{self.x}, {self.y}, {self.length}, {self.direction}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.x}, {self.y}, {self.length}, {direction})"


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
                    self.grid_values = np.zeros((self.width, self.height))  # populate with 1 if char belongs

                    self.grid_numbers = self.grid_numbers.astype('int')
                    self.grid_values = self.grid_values.astype('int')

                else:  # add 1's to grid x,y coords if letter belongs there
                    line = line.strip(); fields = line.split(' ')
                    new_fields = []
                    for i in fields:
                        if i != '':
                            new_fields.append(i)
                    # print(f'{new_fields=}')

                    for char in new_fields:  # build word list horizontal of words in a line

                        # char.rstrip('\n')
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
                        # elif re.search(r' ', char):
                        #     pass
                ccount = 0; lcount += 1

            self.grid_horz = grid_words
            self.grid_vert = grid_words.transpose()






        self.variables = set()

        grid_dict = OrderedDict({'across' : self.grid_horz, 'down' : self.grid_vert})
        # grid_dict = OrderedDict({'across' : self.grid_horz})

        word_place_dict = OrderedDict()

        print(f'{self.grid_numbers=}')

        """
        # = #
        X = -1
        _ = 0
        """

        store_words = []
        # store_words = [[row, col, length, direction='Across'|'Down'],[row, col, length, direction='Across'|'Down']]

        for row in range(self.height):
            streak = 0
            begin = False
            word_index = []

            for col_idx in range(self.width):

                char = self.grid_numbers[row][col_idx]

                if (char > 0) and ((col_idx == 0) or (len(word_index) == 0)):
                    word_index = [row, col_idx, 1, f'{char}-ACROSS']

                elif (char >= 0) and (len(word_index) > 0):  # add length   if _ or #
                    word_index[2] += 1
                    if col_idx == (self.width - 1):
                        store_words.append(word_index)
                        word_index = []

                elif (char == -1) and (col_idx != self.width - 1) and (len(word_index) > 0):  # stop - end
                    store_words.append(word_index)
                    word_index = []

                elif (char == -1) and (col_idx == self.width - 1) and (len(word_index) > 0):  # stop - end
                    store_words.append(word_index)
                    word_index = []

                elif (char == -1) and (len(word_index) == 0):  # stop - end
                    word_index = []

        for i in store_words:
            print(i)

        print(f'{len(store_words)}')




        # print(f'{store_words=}')
                # if (streak == 0) and (char > 0):  # ACROSS
                #
                # if (streak > 1) and (char == 0):


        sys.exit()
        # print(f'r: {row}; c: {col_idx}; {self.grid_numbers[row][col_idx]}')




        # for dxn, grid in grid_dict.items():
        for x in range(len(self.grid_horz)):
            word_len = 0
            # print(f'{len(self.grid_horz)}')
            start_y = 0
            for y in range(len(self.grid_horz)):

                word_len = y - start_y
                coordinate = int(self.grid_horz[x][y])  # 0, 1, 2
                num = -1

                if (coordinate == 2) and (y == 0 or y != self.width - 1):
                    if word_len == 0:
                        num = int(self.grid_numbers[x][y])
                        word_place_dict[num] = ['across', 0]
                        start_y = y

                if y == self.width - 1:
                    if (coordinate == 1) and (word_len > 1):
                        self.variables.add(Variable(x=x, y=start_y, length=word_len, direction='across'))
                        word_place_dict[num] = ['across', word_len]
                        # start_y = y + 1

                    elif (coordinate == 0) and (word_len > 2):
                        self.variables.add(Variable(x=x, y=start_y, length=word_len-1, direction='across'))
                        word_place_dict[num] = ['across', word_len-1]
                        # start_y = y + 1
                #
                # else:  # not the edge boundary
                #     if (coordinate == 0) and (word_len > 2):
                #         self.variables.add(Variable(x=x, y=start_y, length=word_len-1, direction='across'))
                #         word_place_dict[num] = ['across', word_len-1]
                #     elif (coordinate == 1) and (word_len > 1):
                #         self.variables.add(Variable(x=x, y=start_y, length=word_len, direction='across'))
                #         word_place_dict[num] = ['across', word_len]
                # if word_len > 1:
                #     if (coordinate == 0) or (y == self.width - 1):
                #         self.variables.add(Variable(x=x, y=start_y, length=word_len, direction='across'))
                #         word_place_dict[num] = ['across', word_len]
                #         start_y = y + 1
                #
                # elif word_len == 1:
                #     if coordinate == 0:
                #         start_y = y + 1
                        # and (y == self.width - 1):
                    # print(f'{x=} {y=} {coordinate=}')

        print(f'{self.grid_numbers=}')
        print(f'{self.grid_horz=}')


        for key, value in word_place_dict.items(): print(f'{key=} : {value=}')

        sys.exit()
        # def find_word_locations(self):
        word_location_dict = OrderedDict()
        word_location_dict = {}
        for var in self.variables:  # Variable(0, 3, 12, 'DOWN')
            x = int(var.x)
            y = int(var.y)
            dxn = var.direction.lower()
            if self.grid_numbers[x][y] > 0:
                num = str(int(self.grid_numbers[x][y]))
                key = f'{num}-{dxn}'
                word_location_dict[key] = ['NO_VALUE', var.length]

        for key, value in word_location_dict.items(): print(f'{key=} : {value=}')

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
