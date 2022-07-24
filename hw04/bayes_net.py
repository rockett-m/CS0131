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
        self.Model.print_variable_dict()






#
# def prompt_user(self):
#     # prompt user for symbol until 'end' is typed
#     user_input = input('Query symbol (or end): ')
#     user_input.strip()  # remove newline
#     if user_input != "end":
#         self.check_entailment(user_input)
#     else:
#         sys.exit(f'{user_input}\n')
#



if __name__ == "__main__":

    model = Model()

    bayes_net = Bayes_Net(model)

    sys.exit()


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
