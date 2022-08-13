import itertools
import random
import sys
import os
import re
from collections import OrderedDict, defaultdict
import networkx as nx
import matplotlib.pyplot as plt


class Variable_Node:
    def __init__(self, name: str, domain: list):
        self.name = name
        self.domains = domain
        self.parents = []
        self.children = []
        self.cond_prob_table = []
        self.verbose_cpt = []
        self.big_cpt = OrderedDict()
        self.final_cpt = OrderedDict()

    def add_parents(self, parents: list):
        self.parents = parents

    def add_children(self, children: list):
        self.children = children

    def update_cond_prob_table(self, table_line: list):
        self.cond_prob_table.append(table_line)

    def update_verbose_cpt(self, table: list):
        self.verbose_cpt = table


class Model:
    def __init__(self):
        # self.graph = nx.DiGraph()
        self.input_file = ''
        self.Variables = OrderedDict()

        self.parse_cli()
        self.parse_input_file()
        # self.build_verbose_cpt()
        self.create_acyclic_graph()

        self.create_big_cpt()

        if self.debug:
            # self.display_graph()
            # self.print_variable_dict()
            # self.print_verbose_cpt()
            # self.print_normal_cpt()
            pass

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


    # def parse_input_file(self):
    #     with open(self.input_file, 'r') as fi:
    #         section = "Variables"
    #         iter_length = 0; count = 0; node_name = ''
    #         line_count = 0
    #         for line in fi:
    #             line = line.strip()
    #             fields = line.split(' ')
    #
    #             if re.search(r'# Parents', line):
    #                 section = "Parents"
    #                 continue
    #
    #             elif re.search(r'# Tables', line):
    #                 section = "Tables"
    #                 continue
    #
    #             if section == "Variables":
    #                 """
    #                 Burglary T F
    #                 Earthquake T F
    #                 Alarm T F
    #                 JohnCalls T F
    #                 MaryCalls T F
    #                 """
    #
    #                 var = Variable_Node(name=fields[0], domain=fields[1:])
    #
    #                 self.Variables.update({var.name:var})
    #
    #             elif section == "Parents":  # parents
    #                 """
    #                 # Parents
    #                 Alarm Burglary Earthquake
    #                 JohnCalls Alarm
    #                 MaryCalls Alarm
    #                 """
    #
    #                 child = fields[0]
    #                 parents = fields[1:]
    #                 if child in self.Variables.keys():
    #                     child = self.Variables[child]
    #                     child.add_parents(parents)
    #                     self.Variables.update({child.name:child})
    #
    #             elif section == "Tables":  # tables
    #                 """
    #                 # Tables
    #                 Burglary
    #                 0.001
    #                 Earthquake
    #                 0.002
    #                 Alarm
    #                 T T 0.95
    #                 T F 0.94
    #                 F T 0.29
    #                 F F 0.001
    #                 JohnCalls
    #                 T 0.90
    #                 F 0.05
    #                 MaryCalls
    #                 T 0.70
    #                 F 0.01
    #                 """
    #
    #                 prob_list = []
    #                 if node_name == '' and re.search(r'[A-Za-z]{2,}', line):  # at least two letters for var
    #                     # Burglary
    #                     node_name = fields[0]
    #                     if node_name in self.Variables.keys():
    #                         node = self.Variables[node_name]  # should be    parent domain len * parent domain len * parent domain len
    #
    #                 elif node_name != '':
    #
    #                     end = len(node.parents)
    #
    #                     if len(fields) == 1:
    #                         print(f'{fields = }')
    #                         node.update_cond_prob_table(fields)
    #                         self.Variables.update({node.name:node})
    #                         node_name = ''
    #
    #                     elif len(fields) > 1:  # Quality -> 0.1 0.2 0.4 0.2
    #                         prob_list.append(fields)
    #
    #
    #
    #                     print(f'{node_name = } : {prob_list = }')
    #     sys.exit()



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
                            node = self.Variables[node_name]  # should be    parent domain len * parent domain len * parent domain len
                            # iter_length = pow(2, len(node.parents))  # table will have 2^n values with n being len of parent list
                            iter_length = 0

                            for node_parent_name in node.parents:

                                if iter_length == 0:
                                    iter_length = len(self.Variables[node_parent_name].domains)
                                else: # 2 * 5 * 5 for Honesty[2] * Quality[5] * Kindness[5] = 50 for Recommendation
                                    iter_length *= len(self.Variables[node_parent_name].domains)
                                print(f'ITER LENGTH {iter_length = }')

                            print(f'{fields = } : {iter_length = }')
                        continue

                    if node_name != '':  # not nothing
                        # print(f'{node_name} : {iter_length = } : {count = }')
                        if node_name in self.Variables.keys():
                            node = self.Variables[node_name]

                            print(f'{node.name = } : {node.cond_prob_table = }')

                            if len(fields) == 1:
                                print(f'{fields = }')
                                node.update_cond_prob_table(fields)
                                self.Variables.update({node.name:node})

                            elif len(fields) > 1:  # Quality -> 0.1 0.2 0.4 0.2

                                # print(f'{fields = } > 1 !!!!!!!!!!!!!!!!')
                                # T 1 1 0.0 0.0 0.0 0.0 = 7 fields
                                # H Q K = 3 parents
                                # 0.0 0.0 0.0 0.0 = 4 probs
                                # 1, 2, 3, 4, 5 = 5 domains
                                if (len(node.domains) > 2) and ((len(fields) - len(node.parents)) != len(node.domains)):
                                # if (len(fields) - len(node.parents)) != len(node.domains):
                                #     print(f'{fields = } > 1 UNEQUAL')

                                    len_fields = len(fields)
                                    len_par =    len(node.parents)
                                    len_dom =    len(node.domains)
                                    print(f'{len_fields = } : {len_par = } : {len_dom = }')
                                    probs_start = len(node.parents)
                                    probability = fields[probs_start:]

                                    summ = 0
                                    for i in probability:
                                        try:
                                            summ += float(i)
                                        except:
                                            print(f'ERROR {fields = }')
                                    final_field = str(round(1-summ, 3))
                                    fields.append(final_field)
                                    print(f'{fields = }')

                                node.update_cond_prob_table(fields)
                                self.Variables.update({node.name:node})

                            # node = self.Variables[node_name]
                            # node.update_cond_prob_table(fields)
                            # self.Variables.update({node.name:node})
                            """
                            for k,v in self.Variables.items():
                                print(f'\n{k = } : {v.domains = }')
                                for line in v.cond_prob_table:
                                    print(f'cpt {line = }')
                            """

                        #
                        #     print(f'{node.name = } : {node.cond_prob_table = }')
                        #
                        #
                        # print('PRINTTTTTTTTT')
                        # for k,v in self.Variables.items():
                        #     print(f'\n{k = } : {v.domains = }')
                        #     for line in v.cond_prob_table:
                        #         print(f'cpt {line = }')

                        if iter_length == 0:  # case for just value listed   0.001
                            node_name = ''; count = 0; iter_length = 0
                        elif count == iter_length - 1:  # done with current cond_prob_table
                            node_name = ''; count = 0; iter_length = 0
                        else:
                            count += 1

                line_count += 1

        for k,v in self.Variables.items():
            print(f'{k = }\n{v.cond_prob_table = }')

    def print_variable_dict(self):
        for k,v in self.Variables.items():
            # print(f'{k = } :\n{v = } : {v.name = } : {v.domains = } {v.parents = } : {v.cond_prob_table = }\n')
            print(f'{k = } :\n{v.name = } : {v.domains = } {v.parents = } : {v.cond_prob_table = }')
            print(f'{v.verbose_cpt = }\n')

    def print_normal_cpt(self):
        for k,v in self.Variables.items():
            print(f'\n{k = }')
            for line in v.cond_prob_table:
                print(line)
        print()

    def create_acyclic_graph(self):

        G = nx.DiGraph()

        for k,v in self.Variables.items():
            node_name = k
            node = v
            G.add_node(node_name)
            G.nodes[node_name]['object'] = node

        for k,v in self.Variables.items():
            node_name = k
            node = v
            if len(node.parents) > 0:
                for parent in node.parents:
                    G.add_edge(parent, node_name)

                    # if self.debug:
                    #     print(f'{parent = }: {node.name = }')
        self.graph = G

    def display_graph(self):

        nx.draw_networkx(self.graph)
        plt.show()

    def create_big_cpt(self):

        for node_name, node in self.Variables.items():
            print(f'\nbig cpt init on {node_name = }')
            new_cpt = OrderedDict()

            if len(node.domains) == 2:  # T, F

                for line in node.cond_prob_table:  # check node domain size to determine

                    print(f'{line = } : {node.domains = }')
                    key = ''
                    parents = line[:-1]   # not true for books.txt
                    prob = line[-1]       # fix for books.txt (last 5 values are prob)


                    # key = '__'.join(parents)
                    for i in parents:
                        key += f'{i}__'

                    count = 0
                    for d in node.domains:  # T, F
                        # new_key = key
                        # new_key = f'{key}__{d}'
                        new_key = f'{key}{d}'
                        if count == 0:
                            new_cpt[new_key] = float(prob)
                        else:
                            new_cpt[new_key] = round(1 - float(prob), 3)
                        count += 1



            # elif len(node.domains) > 2: # 5 for Quality, Kindness, Recommendation
            if len(node.domains) > 2: # 5 for Quality, Kindness, Recommendation
                print(f'domains > 2: {node.domains = }')

                if len(node.parents) == 0:

                    """
                    key = 'Honesty'
                    T : v = 0.8
                    F : v = 0.2
                    
                    key = 'Quality'
                    1 : v = 0.1
                    2 : v = 0.2
                    3 : v = 0.4
                    4 : v = 0.2
                    5 : v = 0.1
                    """

                    for line in node.cond_prob_table:  # check node domain size to determine
                        print(f'long {line = }')

                        # k = 'Kindness' :
                        # v.domains = ['1', '2', '3', '4', '5']
                        # cpt line = ['0.05', '0.1', '0.2', '0.5', '0.15']
                        for domain, prob in zip(node.domains, line):
                            new_cpt[domain] = float(prob)  # '1' = 0.05;  '2' = 0.1

                elif len(node.parents) > 0:

                    len_parents = len(node.parents)

                    for line in node.cond_prob_table:

                        prob_fields = line[len_parents:]

                        print(f'deep cpt {line = }')
                        key_str_common = '__'.join(line[0:len_parents])
                        # key_str_common = '__'.join(line[0:len_parents])

                        print(f'!!!!!!!!! {key_str_common = } : {prob_fields = } !!!!!!!!!!!!!!!!!!!!!!!!!')

                        for domain, prob in zip(node.domains, prob_fields):
                            key_str = f'{key_str_common}__{domain}'
                            new_cpt[key_str] = float(prob)

            node.big_cpt = new_cpt

            self.Variables.update({node_name:node})

    def print_big_cpt(self):
        print(f'\nformat:\tparents then child domain\texample: ')
        print(f'parent=Burglary, parent=Earthquake, child=Alarm')
        print(f'domains=T,F')
        print(f'''key = 'Alarm'
                    B E A : Probability
                    T.T.T : v = 0.95
                    T.T.F : v = 0.05
                    T.F.T : v = 0.94
                    T.F.F : v = 0.06
                    F.T.T : v = 0.29
                    F.T.F : v = 0.71
                    F.F.T : v = 0.001
                    F.F.F : v = 0.999\n''')
        for key,val in self.Variables.items():
            print(f'{key = }')
            for k,v in val.big_cpt.items():
                print(f'{k = } : {v = }')
            print()


"""
H Q K      Prob
T 1 1 1.0 0.0 0.0 0.0
T 1 2 0.9 0.1 0.0 0.0
T 1 3 0.8 0.1 0.1 0.0
T 1 4 0.7 0.1 0.1 0.1
T 1 5 0.6 0.125 0.125 0.125

Honesty
0.8
Quality
0.1 0.2 0.4 0.2
Kindness
0.05 0.1 0.2 0.5

H Q K R      Prob
T 1 1 1 1.0 0.0 0.0 0.0
T 1 1 2 1.0 0.0 0.0 0.0
T 1 1 3 1.0 0.0 0.0 0.0
T 1 1 4 1.0 0.0 0.0 0.0
T 1 1 5 0.0 1.0 1.0 1.0



T 1 5 0.6 0.125 0.125 0.125

\/

T 1 5 1 0.6
T 1 5 2 0.125
T 1 5 3 0.125
T 1 5 4 0.125
T 1 5 5 = 1 - sum(1:4)


"""


"""
def build_verbose_cpt(self):

    for k, v in self.Variables.items():

        node_name = k
        node = v

        len_line = len(node.cond_prob_table[0])
        num_lines = len(node.cond_prob_table)
        # print(f'{len_line = }\t{num_lines = }')
        # print(node.cond_prob_table.shape())
        new_table = []
        if num_lines == 1 and len_line == 1:

            newline = []
            field = f'{node_name} = T'
            newline.append(field)

            prob = v.cond_prob_table[0][0]
            newline.append(prob)
            new_table.append(newline)

        else:
            # print(f'{len_line = } : {num_lines = }')
            for line in node.cond_prob_table:
                newline = []
                # print(f'{line = }')
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

def print_verbose_cpt(self):
    for k,v in self.Variables.items():
        print(f'\n{k = }')
        for line in v.verbose_cpt:
            print(line)
    print()
"""