import re
import numpy as np

class Variable():

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, direction, length, x, y):
        self.direction = direction
        self.length =    length
        self.x =         x
        self.y =         y

    def __hash__(self):  # dictionary
        return hash((self.direction, self.length, self.x, self.y))

    def __eq__(self, other):  # intersection
        equality_bool = False

        if ((self.direction == other.direction) and
                (self.length == other.length) and
                (self.x == other.x) and
                (self.y == other.y)):
            equality_bool = True

        return equality_bool

    def __str__(self):
        return f"{self.direction} : {self.length}; {self.x}, {self.y}"

    def __repr__(self):
        direction = self.direction
        return f"Variable({direction}, {self.length}, {self.x}, {self.y})"


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
                else:  # add 1's to grid x,y coords if letter belongs there
                    line = line.strip(); fields = line.split(' ')
                    for char in fields:  # build word list horizontal of words in a line
                        char.rstrip('\n')
                        if re.search(r'\d+', char):
                            # print(f'line: {lcount}; char: {ccount}; char: >{char}<; line: {line};')
                            grid_words[lcount, ccount] = 2; ccount += 1
                        elif re.search('_', char):  # word begin
                            # print(f'line: {lcount}; char: {ccount}; char: >{char}<; line: {line};')
                            grid_words[lcount, ccount] = 1; ccount += 1
                        elif re.search(r'X', char):  # end and reset counts
                            ccount += 1
                        elif re.search(r' ', char):
                            pass
                ccount = 0; lcount += 1

            self.grid_horz = grid_words
            self.grid_vert = grid_words.transpose()


    def print_input_files(self):
        print(f'\n{self.width} x {self.height} crossword detected\n')
        print(f'\nxword_file:\t{self.xword_file}\n')
        [ print(x) for x in open(self.xword_file, 'r').read().splitlines() ]

        print(f'\nword_file:\t{self.word_file}\n')
        [ print(x) for x in open(self.word_file, 'r').read().splitlines() ]; print()

    def print_xword_and_words(self):
        print(f'self.words: {self.words}\n')
        print(f'self.orig_xword: {self.orig_xword}\n')

    def print_grids(self):
        print(f'\ngrid_horz:\n{self.grid_horz}\n')
        print(f'grid_vert:\n{self.grid_vert}\n')
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
