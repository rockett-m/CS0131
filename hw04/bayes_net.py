#!/usr/bin/python3
import os
import sys
import re
from collections import OrderedDict
from classes import *


class Bayes_Net:
    def __init__(self, Model):
        self.Model = Model

        self.domains = self.Model.Variables
        self.input_file = ''






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
