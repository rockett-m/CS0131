import sys
import os
import re
from collections import OrderedDict

class Variable_Node:
    def __init__(self, name: str, domain: list):
        self.name = name
        self.domains = domain
        self.parents = []
        self.cond_prob_table = []
        self.verbose_cpt = []
        self.base_case = False

    def add_parents(self, parents: list):
        self.parents = parents

    def update_cond_prob_table(self, table_line: list):
        self.cond_prob_table.append(table_line)

    def update_verbose_cpt(self, table: list):
        self.verbose_cpt = table


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
            print(f'\nfile not found: {self.input_file = }\n')
            sys.exit("\nrun: python bayes_net.py burglary.txt\n")
        else:
            print(f'\nLoading file "{self.input_file}"\n')

    def parse_input_file(self):
        with open(self.input_file, 'r') as fi:
            section = "Variables"
            iter_length = 0; count = 0; node_name = ''

            line_count = 0
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

                    if line_count == 0: var.base_case = True

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
                            node.update_cond_prob_table(fields)
                            self.Variables.update({node.name:node})

                        if iter_length == 0:  # case for just value listed   0.001
                            node_name = ''; count = 0; iter_length = 0
                        elif count == iter_length - 1:  # done with current cond_prob_table
                            node_name = ''; count = 0; iter_length = 0
                        else:
                            count += 1

                line_count += 1

    def build_verbose_cpt(self):

        for k, v in self.Variables.items():

            node_name = k
            node = v

            len_line = len(node.cond_prob_table[0])
            num_lines = len(node.cond_prob_table)

            # print(f'{len_line = }\t{num_lines = }')

            new_table = []

            if num_lines == 1 and len_line == 1:

                newline = []
                field = f'{node_name} = T'
                newline.append(field)

                prob = v.cond_prob_table[0][0]
                newline.append(prob)
                new_table.append(newline)

            else:

                for line in node.cond_prob_table:
                    newline = []

                    for iter in range(len(line)):
                        if iter != len_line - 1:
                            field = f'{node.parents[iter]} = {line[iter]}'  # "Earthquake = T"
                            newline.append(field)
                        else:
                            field = f'{line[iter]}'
                            newline.append(field)

                    new_table.append(newline)

            node.update_verbose_cpt(new_table)
            self.Variables.update({node_name:node})


    def print_variable_dict(self):
        for k,v in self.Variables.items():
            # print(f'{k = } :\n{v = } : {v.name = } : {v.domains = } {v.parents = } : {v.cond_prob_table = }\n')
            print(f'{k = } :\n{v.name = } : {v.domains = } {v.parents = } : {v.cond_prob_table = }')
            print(f'{v.base_case = }')
            print(f'{v.verbose_cpt = }\n')
