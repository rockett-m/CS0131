#!/usr/bin/python3
import os
import sys
import re
from collections import OrderedDict
from classes import *


class Bayes_Net:
    def __init__(self, Model):
        self.Model = Model

        # self.domains = self.Model.Variables
        self.Model.parse_input_file()
        if self.Model.debug:
            self.Model.print_variable_dict()


    def calculate_probability(self, args: list):

        print(f'{args = }')
        var = args[0]

        if len(args) == 1:
            if var in self.Model.Variables.keys():
                node = self.Model.Variables[var]

                if len(node.parents) == 0:
                    prob_true = 0.0
                    for i in node.cond_prob_table:
                        prob_true = float(i[0])

                    print(f'P(T) = {prob_true}, P(F) = {1-prob_true}\n')

                else:
                    print(f'need to solve when parent len != 0')
            else:
                print(f'\n{var = } not found in conditional probability table\n')


        elif len(args) == 2:  # P(X | Y) = P(X and Y)/P(Y)
            cond = args[1]

            if [var, cond] in self.Model.Variables.keys():
                node = self.Model.Variables[var]

                cond_prob = 0.0
                for line in node.cond_prob_table:
                    t_or_f = cond.split(' = ')[-1]
                    if t_or_f == line[0]:
                        cond_prob = line[1]
                        continue

                # if direct match of conditional prob, can calc var
                location = 0
                if cond in node.parents:
                    location = node.parents.index(cond)


            else:
                print(f'\n{args = } not all found in conditional probability table\n')


        elif len(args) == 3:
            cond1 = args[1]; cond2 = args[2]

            if [var, cond1, cond2] in self.Model.Variables.keys():
                node = self.Model.Variables[var]

            else:
                print(f'\n{args = } not all found in conditional probability table\n')

        else:
            print(f'not found: {args = }\n')

#
    def prompt_user(self):
        # prompt user for symbol until 'end' is typed
        user_input = input()
        user_input.strip()  # remove newline
        cond = []; args = []

        fields = user_input.split(' | ')  # requires space between |
        if len(fields) == 2:
            cond = fields[-1].split(', ')

        args.insert(0, fields[0])
        args += cond

        if user_input != "quit":
            self.calculate_probability(args)
        else:
            sys.exit(f'{user_input}\n')


if __name__ == "__main__":

    model = Model()

    bayes_net = Bayes_Net(model)

    while True:
        bayes_net.prompt_user()
    # https://github.com/MaxHalford/sorobn

# recreate the network

# write own data structure

# create a graph

# make node class with prob and children and parents

"""
# Parents
Disabled Weapon NeuralDisruptor Overpower
^ child   ^ parents  ^          ^



P(alarm | burglary) = P(alarm | burglary, earthquake = false) + P(alarm | burglary, earthquake = true)



P(john) = 0.9 * P(alarm)
P(john) = 0.9  * P(alarm) = 0.9 * P(alarm| earthquake, burglarly)
P(john) = p(john| alarm =true) + P(john| alarm = false)
p(john) = 0.9 * p(alarm = true)_ + 0.05 * P(alarm=false)

"""
