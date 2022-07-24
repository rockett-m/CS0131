import sys
import os
import re
from collections import OrderedDict

class Variable_Node:
    def __init__(self, name: str, domain: list):
        self.name = name
        self.domains = domain
        self.parents = []
        self.truth_table = []

    def add_parents(self, parents: list):
        self.parents = parents

    def update_truth_table(self, table_line: list):
        self.truth_table.append(table_line)


class Model:
    def __init__(self):
        self.input_file = ''
        self.Variables = OrderedDict()
        self.parse_cli()

    def parse_cli(self):
        # read user input on what knowledge base to use
        self.input_file = sys.argv[1]

        if len(sys.argv) > 2:
            self.debug = True
        else:
            self.debug = False

        if not os.path.isfile(self.input_file):
            print(f'file not found: {self.input_file = }\n')
            sys.exit("run: python bayes_net.py burglary.txt ")

    def parse_input_file(self):
        with open(self.input_file, 'r') as fi:
            key = ''
            section = "Variables"

            iter_length = 0
            count = 0
            node_name = ''

            for line in fi:
                line = line.strip()
                fields = line.split(' ')

                if re.search(r'# Parents', line):
                    section = "Parents"
                    continue

                elif re.search(r'# Tables', line):
                    section = "Tables"
                    continue

                if section == "Variables":
                    """
                    Burglary T F
                    Earthquake T F
                    Alarm T F
                    JohnCalls T F
                    MaryCalls T F
                    """

                    var = Variable_Node(name=fields[0], domain=fields[1:])
                    self.Variables.update({var.name:var})

                elif section == "Parents":  # parents
                    """
                    # Parents
                    Alarm Burglary Earthquake
                    JohnCalls Alarm
                    MaryCalls Alarm
                    """

                    child = fields[0]
                    parents = fields[1:]
                    if child in self.Variables.keys():
                        child = self.Variables[child]
                        child.add_parents(parents)
                        self.Variables.update({child.name:child})

                elif section == "Tables":  # tables
                    """
                    # Tables
                    Burglary
                    0.001
                    Earthquake
                    0.002
                    Alarm
                    T T 0.95
                    T F 0.94
                    F T 0.29
                    F F 0.001
                    JohnCalls
                    T 0.90
                    F 0.05
                    MaryCalls
                    T 0.70
                    F 0.01
                    """

                    if node_name == '' and re.search(r'[A-Za-z]{2,}', line):  # at least two letters for var
                        # Burglary
                        node_name = fields[0]
                        if node_name in self.Variables.keys():
                            node = self.Variables[node_name]
                            iter_length = pow(2, len(node.parents))  # table will have 2^n values with n being len of parent list
                        continue

                    if node_name != '':  # not nothing
                        # print(f'{node_name} : {iter_length = } : {count = }')
                        if node_name in self.Variables.keys():
                            node = self.Variables[node_name]
                            node.update_truth_table(fields)
                            self.Variables.update({node.name:node})

                        if iter_length == 0:  # case for just value listed   0.001
                            node_name = ''; count = 0; iter_length = 0
                        elif count == iter_length - 1:  # done with current truth table
                            node_name = ''; count = 0; iter_length = 0
                        else:
                            count += 1



    def print_variable_dict(self):
        for k,v in self.Variables.items():
            print(f'{k = } : {v = } : {v.name = } : {v.domains = } {v.parents = } : {v.truth_table = }\n')
