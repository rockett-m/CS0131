#!/usr/bin/python3
import os
import sys
import time
from copy import deepcopy
from functools import wraps
import operator
from classes import *

global calls
calls = 0
# run as ./cons_solver.py ./inputData/xword00.txt ./inputData/dictionary_small.txt
def parse_files():
    xword_file = sys.argv[1]
    word_file = sys.argv[2]
    arc_consistency = False
    if len(sys.argv) > 3: arc_consistency = True

    for file in [xword_file, word_file]:
        if not os.path.isfile(file):
            print(f'file not found: {file}\n')
            sys.exit("run: python cons_solver.py xword00.txt dictionary_small.txt [true]")

    return xword_file, word_file, arc_consistency


class Crossword_Solver:
    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

        # sorted_x = sorted(self.domains.items(), key=self.domains.keys(Variable.__name__)
        # self.crossword.variables = list(self.crossword.variables.Variable.name).sort()
        # self.crossword.variables = list(self.crossword.variables)

        print(f'\n{len(self.crossword.variables)} words')

    def letter_grid(self, assignment):
        letters = [[None for _ in range(self.crossword.width)]
                    for _ in range(self.crossword.height)]

        for variable, word in assignment.items():
            # print(f'{variable = }  {word = }')
            for k in range(len(word)):
                row = variable.row + (k if variable.direction == 'DOWN' else 0)
                col = variable.col + (k if variable.direction == 'ACROSS' else 0)
                letters[row][col] = word[k]
                # print(f'{letters[row][col] = }  {word[k] = }')

        return letters

    def print_crossword(self, assignment):

        letters = self.letter_grid(assignment)
        # print(f'{letters = }')
        for row in range(self.crossword.height):
            for col in range(self.crossword.width):
                if self.crossword.grid_numbers[row][col] != -1:  # not a 'X'
                    print(letters[row][col], end="")
                else:
                    print("█", end="")
            print()

    def enforce_node_consistency(self):
        # # update with only words the same size as the blank space
        for variable, domain in self.domains.items():
            list_words = []
            for word in crossword.words:
                if variable.length == len(word):
                    list_words.append(word)
            self.domains.update({variable:list_words})

        for variable, domains in self.domains.items():  # fatal error
            if len(domains) == 0:
                sys.exit(f'No possible words (with {variable.length=} for {variable = }. Exiting...')

        print(f'\nInitial assignment and domain sizes:\n')
        for key in self.domains.keys():
            print(f'{key.name} = NO_VALUE ({len(self.domains[key])} values possible)')
        print()

    def solve(self, arc_consistency=False):
        self.enforce_node_consistency()
        if arc_consistency:
            self.ac3(arcs=None)
        return self.backtrack(dict())

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        i, j = self.crossword.overlaps[x, y]

        for x_word in set(self.domains[x]):
            remove = True

            for y_word in self.domains[y]:
                if x_word[i] == y_word[j]:
                    remove = False

            if remove:
                self.domains[x].remove(x_word)
                revised = True

        return revised

    def ac3(self, arcs=None):

        print('\nDoing arc-consistency pre-processing...')

        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = list()
            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))

        while arcs:
            x, y = arcs.pop()

            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x) - self.domains[y]:
                    arcs.append((z, x))

        print('\nInitial assignment with pre-processed domain sizes:')

        for key in self.domains.keys():
            print(f'{key.name} = NO_VALUE ({len(self.domains[key])} values possible)')

        return True

    def assignment_complete(self, assignment):
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def is_consistent(self, assignment):
        # if len(assignment) == 1:
        #     return True
        # for var1 in assignment:
        #     copy = assignment.copy()
        #     copy.pop(var1)
        #
        #     for var2 in copy:
        #         # if assignment[var1] == assignment[var2]:  # we are allowed to repeat words
        #         #     print(f'{assignment[var1] = }  {assignment[var2] = }')
        #         #     return False
        #         crossing = self.crossword.overlaps[(var1, var2)]
        #         if crossing is not None:
        #             x = crossing[0]
        #             y = crossing[1]
        #             if assignment[var1][x] != assignment[var2][y]:
        #                 return False
        # return True

        used_words = set()

        for var in assignment:

            # # All values must be distinct
            # if assignment[var] not in used_words:
            #     used_words.add(assignment[var])
            # else:
            #     return False

            # Every value must have the correct length
            if len(assignment[var]) != var.length:
                return False

            # There are no conflicts between neighbors
            for neighbor in self.crossword.neighbors(var):
                print(f'{neighbor = }\n')
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    print(f'{self.crossword.overlaps[var, neighbor] = }')
                    if assignment[var][i] != assignment[neighbor][j]:
                        print(f'{assignment[var][i]} {assignment[neighbor][j]}')
                        return False

        return True
    # def order_domains_values(self, var):
    #     def cost_calc(list1, list2):
    #         cost_inner = []
    #         for character1 in list1:
    #             cost_inner.append(sum(map(lambda x: x == character1, list2)))
    #         return cost_inner
    #
    #     cost = [0 for x in self.domains[var]]
    #     for neighbor in self.crossword.neighbors(var):
    #         crossing = self.crossword.overlaps[(var,neighbor)]
    #         character1 = [x[crossing[0]] for x in self.domains[var]]
    #         character2 = [x[crossing[1]] for x in self.domains[neighbor]]
    #         cost2 = cost_calc(character1, character2)
    #         cost = [sum(x) for x in zip(cost, cost2)]
    #
    #
    #     values = [x for _, x in sorted(zip(cost2, self.domains[var]))]
    #     print(f'{values = }')
    #     return [x for _, x in sorted(zip(cost2, self.domains[var]))]

    def select_unassigned_variable(self, assignment):
        best = None

        for var in self.crossword.variables - set(assignment):
            if (best is None or
                len(self.domains[var]) < len(self.domains[best]) or
                len(self.crossword.neighbors(var)) > len(self.crossword.neighbors(best))):
                    best = var

        print(f'{best = }')
        return best

    def order_domains_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        n = dict()

        for value in self.domains[var]:
            n[value] = 0
            for neighbor in self.crossword.neighbors(var) - set(assignment):
            # for neighbor in self.crossword.neighbors(var):
                if value in self.domains[neighbor]:
                    n[value] += 1

        return sorted(n, key=n.get)
        #
        # vals_ruleout = {val: 0 for val in self.domains[var]}
        #
        # # Iterate through all possible values of var:
        # for val in self.domains[var]:
        #
        #     # Iterate through neighboring variables and values:
        #     for other_var in self.crossword.neighbors(var):
        #         # for other_val in self.domains[other_var]:
        #
        #             # If val rules out other val, add to ruled_out count
        #         if not self.crossword.overlaps[(var, other_var)]:
        #             vals_ruleout[val] += 1
        #
        # # Return list of vals sorted from fewest to most other_vals ruled out:
        # return sorted([x for x in vals_ruleout], key = lambda x: vals_ruleout[x])





    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domains_values(var, assignment):
            assignment[var] = value
            print(f'{assignment = }')
            if self.is_consistent(assignment):
                print(f'consistent: {assignment = }')
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None

    def backtrack_ac3(self, assignment):
        # Otherwise select an unassigned variable:
        var = self.select_unassigned_variable(assignment)
        pre_assignment_domains = deepcopy(self.domains)
        for val in self.order_domains_values(var):
            assignment[var] = val
            # WORDS_TESTED += 1
            if self.is_consistent(assignment):
                # Update variable domain to be assigned value
                self.domains[var] = {val}
                # Use ac3 to remove inconcistent values from neighbouring variables
                self.ac3([(other_var, var) for other_var in self.crossword.neighbors(var)])
                result = self.backtrack_ac3(assignment)
                if result:
                    return result
            # If assignment does not produce solution, remove assignment and reset domains
            del assignment[var]
            self.domains = pre_assignment_domains
        return None


    def backtrack_search(self, assignment):

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        print(f'{var = }\n{assignment = }\n')
        for value in self.order_domains_values(var):
            print(f'value in self.order_domains_values(var) {value = }')
            # print(f'\n{var = }{assignment = } {value = }\n')
            copy_assn = assignment.copy()
            copy_assn.update({var:value})
            consistent = self.is_consistent(copy_assn)
            # print(f'{var = }{assignment = } {value = } {consistent = }')
            if consistent:
                assignment.update({var:value})
                # print(f'{assignment = }')

                # print(f'{var = }; {assignment = }; {value = }; {consistent = };\n')
                result = self.backtrack_search(assignment)
                if result is not None:
                    print(f'{result = }')
                    return result
                else:
                    assignment.pop(var)
            # else:
            #     # print(f'NOT CONSISTENT: {var = }{assignment = } {value = } {consistent = }')
            #     pass
            # print(f'{assignment.items() = }')
        return None


if __name__ == "__main__":

    xword_file, word_file, arc_consistency = parse_files()

    crossword =        Crossword(xword_file, word_file)
    crossword_solver = Crossword_Solver(crossword)
    assignment =       crossword_solver.solve(arc_consistency)
    # print(crossword_solver.letter_grid(dict()))

    if assignment is None:
        print('\nNo Solution\n')
    else:
        print(f'\nSUCCESS! Solution found after {calls} recursive calls to search.\n')
        crossword_solver.print_crossword(assignment)


    # crossword.print_input_files()
    # crossword.print_grids()
    # crossword.print_xword_and_words()
    # crossword.print_words_to_solve()
    # crossword.print_domains()
    # print(f'{crossword_solver.domains=}')
    # crossword.find_word_locations()

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