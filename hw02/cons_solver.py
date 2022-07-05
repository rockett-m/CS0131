#!/usr/bin/python3
import os
import sys
import time
from functools import wraps

from classes import Crossword

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
        print(f'{key = };  {value = }')


def parse_files():
    xword_file = sys.argv[1]
    word_file = sys.argv[2]

    for file in [xword_file, word_file]:
        if not os.path.isfile(file):
            print(f'file not found: {file}\n')
            sys.exit("run: python cons_solver.py xword00.txt dictionary_small.txt ")

    return xword_file, word_file


class Crossword_Solver:
    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        # update with only words the same size as the blank space
        for k, v in self.domains.items():
            list_words = []
            for word in crossword.words:
                if k.length == len(word):
                    list_words.append(word)
            self.domains.update({k:list_words})

        for k, v in self.domains.items():  # fatal error
            if len(v) == 0:
                sys.exit(f'No possible words (with {k.length=} for {k = }. Exiting...')

    def letter_grid(self, assignment):
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                row = variable.row + (k if direction == variable.DOWN else 0)
                col = variable.col + (k if direction == variable.ACROSS else 0)
                letters[row][col] = word[k]
        return letters

    def print_crossword(self, assignment):

        letters = self.letter_grid(assignment)
        for row in range(self.crossword.height):
            for col in range(self.crossword.width):
                if self.crossword[row][col]:
                    print(letters[row][col] or " ", end="")
                else:
                    print("#", end="")
            print()

    def solve(self):
        self.enforce_node_consistency()
        return self.backtrack_search()

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        def check_length(string, length):
            if len(string) != length:
                return string

        for variable, domain in self.domains.items():
            keys2delete = map(check_length, domain, [variable.length for x in range(len(domain))])
            for key in list(keys2delete):
                if key is not None:
                    self.domains[variable].remove(key)

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
                crossing = self.crossword.intersections[(var, var2)]
                if crossing is not None:
                    x = crossing[0]
                    y = crossing[1]
                    if assignment[var][x] != assignment[var2][y]:
                        return False
        return True

    def order_domains_values(self, var, assignment):
        def cost_calc(list1, list2):
            cost_inner = []
            for charr in list1:
                cost_inner.append(sum(map(lambda x: x == charr, list2)))
            return cost_inner

        cost = [0 for x in self.domains[var]]
        cost2 = []
        for neighbor in self.crossword.neighbors(var):
            crossing = self.crossword.intersections([var, neighbor])
            character1 = [x[crossing[0]] for x in self.domains[var]]
            character2 = [x[crossing[1]] for x in self.domains[neighbor]]
            cost2 = cost_calc(character1, character2)
            cost = [sum(x) for x in zip(cost, cost2)]

        return [x for _, x in sorted(zip(cost2, self.domains[var]))]

    def select_unassigned_variable(self, assignment):
        remaining = 1e10
        degree = 0

        var = None
        for variable in self.crossword.variables:
            if variable not in assignment:
                if len(self.domains[variable]) < remaining:
                    remaining = len(self.domains[variable])
                    var = variable
                elif len(self.domains[variable]) == remaining:
                    if len(self.crossword.neighbors(variable)) > degree:
                        degree = len(self.crossword.neighbors(variable))
                        var = variable
        return var

    def backtrack_search(self, assignment):

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domains_values(var, assignment):
            copy_assn = assignment.copy()
            copy_assn.update({var:value})
            consistent = self.is_consistent(copy_assn)
            if consistent:
                assignment.update({var:value})
                result = self.backtrack_search(assignment)
                if result is not None:
                    return result
                else:
                    assignment.pop(var)
        return None


def solve_crossword(xword_file, word_file):

    crossword = Crossword(xword_file, word_file)

    # crossword.print_input_files()
    # crossword.print_grids()
    # crossword.print_xword_and_words()
    crossword.print_words_to_solve()
    # crossword.print_domains()
    crossword_solver = Crossword_Solver(crossword)

    assignment = crossword_solver.solve()
    # sys.exit()
    if assignment is None:
        print('No Solution')
    else:
        crossword_solver.print_crossword(assignment)
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