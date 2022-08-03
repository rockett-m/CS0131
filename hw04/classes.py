import itertools
import random
import sys
import os
import re
from collections import OrderedDict, defaultdict
import networkx as nx
import matplotlib.pyplot as plt


def P(var, evidence={}):
    "The probability distribution for P(variable | evidence), when all parent variables are known (in evidence)."
    row = tuple(evidence[parent] for parent in var.parents)
    return var.cpt[row]

def normalize(dist):
    "Normalize a {key: value} distribution so values sum to 1.0. Mutates dist and returns it."
    total = sum(dist.values())
    for key in dist:
        dist[key] = dist[key] / total
        assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
    return dist

def sample(probdist):
    "Randomly sample an outcome from a probability distribution."
    r = random.random() # r is a random point in the probability distribution
    c = 0.0             # c is the cumulative probability of outcomes seen so far
    for outcome in probdist:
        c += probdist[outcome]
        if r <= c:
            return outcome

def globalize(mapping):
    "Given a {name: value} mapping, export all the names to the `globals()` namespace."
    globals().update(mapping)

def joint_distribution(net):
    "Given a Bayes net, create the joint distribution over all variables."
    return ProbDist({row: prod(P_xi_given_parents(var, row, net)
                               for var in net.variables)
                     for row in all_rows(net)})

def all_rows(self, net):
    return itertools.product(*[var.domain for var in net.variables])

def P_xi_given_parents(var, row, net):
    "The probability that var = xi, given the values in this row."
    dist = P(var, Evidence(zip(net.variables, row)))
    xi = row[net.variables.index(var)]
    return dist[xi]

def prod(numbers):
    "The product of numbers: prod([2, 3, 5]) == 30. Analogous to `sum([2, 3, 5]) == 10`."
    result = 1
    for x in numbers:
        result *= x
    return result


class Factor(dict): "An {outcome: frequency} mapping."

class ProbDist(Factor):
    """A Probability Distribution is an {outcome: probability} mapping.
    The values are normalized to sum to 1.
    ProbDist(0.75) is an abbreviation for ProbDist({T: 0.75, F: 0.25})."""
    def __init__(self, mapping=(), **kwargs):
        if isinstance(mapping, float):
            mapping = {T: mapping, F: 1 - mapping}
        self.update(mapping, **kwargs)
        normalize(self)

class Evidence(dict):
    "A {variable: value} mapping, describing what we know for sure."

class CPTable(dict):
    "A mapping of {row: ProbDist, ...} where each row is a tuple of values of the parent variables."

    def __init__(self, mapping, parents=()):
        """Provides two shortcuts for writing a Conditional Probability Table.
        With no parents, CPTable(dist) means CPTable({(): dist}).
        With one parent, CPTable({val: dist,...}) means CPTable({(val,): dist,...})."""
        if len(parents) == 0 and not (isinstance(mapping, dict) and set(mapping.keys()) == {()}):
            mapping = {(): mapping}
        for (row, dist) in mapping.items():
            if len(parents) == 1 and not isinstance(row, tuple):
                row = (row,)
            self[row] = ProbDist(dist)

class Bool(int):
    "Just like `bool`, except values display as 'T' and 'F' instead of 'True' and 'False'"
    __str__ = __repr__ = lambda self: 'T' if self else 'F'

T = Bool(True)
F = Bool(False)


def enumeration_ask(X, evidence, net):
    "The probability distribution for query variable X in a belief net, given evidence."
    i = net.variables.index(X)    # The index of the query variable X in the row
    dist = defaultdict(float)     # The resulting probability distribution over X
    for (row, p) in joint_distribution(net).items():
        if matches_evidence(row, evidence, net):
            dist[row[i]] += p
    return ProbDist(dist)

def matches_evidence(row, evidence, net):
    "Does the tuple of values for this row agree with the evidence?"
    return all(evidence[v] == row[net.variables.index(v)]
               for v in evidence)



class Variable_Node:
    def __init__(self, name: str, domain: list):
        self.name = name
        self.domains = domain
        self.parents = []
        self.children = []
        self.cond_prob_table = []
        self.verbose_cpt = []
        self.base_case = False

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
        self.build_verbose_cpt()
        self.create_acyclic_graph()

        if self.debug:
            self.display_graph()
            self.print_variable_dict()

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

                    if self.debug:
                        print(f'{parent = }: {node.name = }')

        self.graph = G

    def display_graph(self):

        nx.draw_networkx(self.graph)
        plt.show()

# create BST of vars
# adjacency lists
#     https://www.pythonpool.com/adjacency-list-python/
# for each node, which nodes are direct path

    # def enumeration_ask(self, X, e, bn):
    # def enumeration_ask(self, X, e):
    #     # bn = self.
    #     for parent, child in self.graph.edges:
    #         print(f'{parent = } : {child = }')
    #         # print(f'{edge = }')
    #         #
            # parent = edge[0]
            # child =  edge[1]


        #     number = self.enumeration_all(vars, e)
        #
        # normalized_qx = normalize_qx()
        # return normalized_qx

        """
        for node in self.graph:
            print(f'{node = }') #: {node['object'] = }")        
        """








    # # def enumeration_all(self, vars, e):
    # def enumerate_all(self, e):
    #     vars = self.Variables
    #     number = 0
    #
    #     if len(vars) == 0:
    #         return 1.0
    #
    #     for V in vars:
    #         # if V is an evidence variable with value v in e
    #         if V:  # an evidence variable with value v in e
    #             # return P(v | parents(V )) × enumerate_all(REST(vars),e))
    #             probability = 0
    #             return probability
    #
    #         else:
    #             sum_v = 0
    #             # !v P(v | parents(V)) × enumerate_all(REST(vars), ev)
    #             # where ev is e extended with V = v
    #             return sum_v
    #
    #     return number

    # def normalize_qX(self, X):
    #
    #     normalized_qx = 0
    #
    #     for i in X:
    #         pass
    #
    #     return normalized_qx