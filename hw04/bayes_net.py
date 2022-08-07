#!/usr/bin/python3
import os
import sys
import re
from collections import OrderedDict
import numpy as np
from functools import *
from utils import *

from classes import *


def prompt_user(bayes_net):
    # global args
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
        # bayes_net.calculate_probability(args)
        # print(args, args[0], args[1:])
        # Alarm | Burglary = T, Earthquake = T
        return args[0], args[1:]
    else:
        sys.exit(f'{user_input}\n')


class Bayes_Net:
    def __init__(self, Model):
        self.Model = Model

        # self.Model.convert_cpt_tuple()
        # self.Model.enumeration_ask()  # calls self.Model.enumeration_all() inside
        # enumeration_ask(X=, evidence=, net=Model)  # calls self.Model.enumeration_all() inside
        # self.Model.print_cpt()


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



class ProbDist:
    """A discrete probability distribution. You name the random variable
    in the constructor, then assign and query probability of values.
    # >>> P = ProbDist('Flip'); P['H'], P['T'] = 0.25, 0.75; P['H']
    0.25
    # >>> P = ProbDist('X', {'lo': 125, 'med': 375, 'hi': 500})
    # >>> P['lo'], P['med'], P['hi']
    (0.125, 0.375, 0.5)
    """

    def __init__(self, var_name='?', freq=None):
        """If freq is given, it is a dictionary of values - frequency pairs,
        then ProbDist is normalized."""
        self.prob = {}
        self.var_name = var_name
        self.values = []
        if freq:
            for (v, p) in freq.items():
                self[v] = p
            self.normalize()

    def __getitem__(self, val):
        """Given a value, return P(value)."""
        try:
            return self.prob[val]
        except KeyError:
            return 0

    def __setitem__(self, val, p):
        """Set P(val) = p."""
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        """Make sure the probabilities of all values sum to 1.
        Returns the normalized distribution.
        Raises a ZeroDivisionError if the sum of the values is 0."""
        total = sum(self.prob.values())
        if not np.isclose(total, 1.0):
            for val in self.prob:
                self.prob[val] /= total
        return self

    def show_approx(self, numfmt='{:.3g}'):
        """Show the probabilities rounded and sorted by key, for the
        sake of portable doctests."""
        return ', '.join([('{}: ' + numfmt).format(v, p) for (v, p) in sorted(self.prob.items())])

    def __repr__(self):
        return "P({})".format(self.var_name)


def normalize(dist):
    "Normalize a {key: value} distribution so values sum to 1.0. Mutates dist and returns it."
    total = sum(dist.values())
    for key in dist:
        dist[key] = dist[key] / total
        assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
    return dist


def enumeration_ask(X: str, e: list, bn):

    # check if both parents aren't there CPT
    # T.T.T
    # incomplete lookups

    # X = str(X[0])  # first and only elem of list
    vars = list(bn.Variables.keys())

    evidence_dict = OrderedDict()
    for i in e:
        j = i.split(' = ')[0]  # 'Earthquake = T' => 'Earthquake'
        evidence_dict[i.split(' = ')[0]] = i.split(' = ')[1]   # evidence_dict['Earthquake'] = 'T'

    assert X not in evidence_dict.keys(), "Query variable must be distinct from evidence"
    Q = OrderedDict()

    for xi in bn.Variables[X].domains:  # T, F

        evidence_dict[X] = xi  # 'Alarm' = 'T'  # add to dict
        Q[xi] = enumerate_all(vars=bn.Variables, evidence=evidence_dict, bayes_net=bn)  # Q['T'] = 0.001

    Q_normalized = normalize(Q)  # {Q['T'] = 0.001, Q['F'] = 0.999}

    return Q_normalized


def enumerate_all(vars: dict, evidence: dict, bayes_net):

    if len(vars) == 0: return 1.0

    var_names = list(vars.keys())
    V, rest = var_names[0], var_names[1:]

    rest_dict = OrderedDict()
    for elem in rest:
        if elem in vars.keys():
            rest_dict.update({elem:vars[elem]})

    Vnode = vars[V]
    # print(f'{V = } : {rest = } : {Vnode = }')

    if V in evidence.keys():  # only go here if full CPT lookup possible ***

        row = ''  # create the cpt row now
        if len(vars[V].parents) > 0:
            for parent in vars[V].parents:  # ['Burglary', 'Earthquake']
                row += f'{evidence[parent]}.'  # T.

        row += evidence[V]  # 0.99  # exact cpt row match expected like 'T.T.T' = 0.99
        # if row in vars[V].big_cpt.keys():
        cpt_prob =  vars[V].big_cpt[row]  # 'T.T.T' = 0.99

        return cpt_prob * enumerate_all(vars=rest_dict, evidence=evidence, bayes_net=bayes_net)

    else: # no exact match found in cpt
        total = 0
        evidenceV = evidence.copy()
        for domain_val in vars[V].domains:  # loop through parent unknowns too

            row = ''  # create the cpt row now
            if len(vars[V].parents) > 0:
                for parent in vars[V].parents:  # ['Burglary', 'Earthquake']
                    row += f'{evidenceV[parent]}.'  # T.

            row += domain_val  # 0.99  # exact cpt row match expected like 'T.T.T' = 0.99

            cpt_prob =  vars[V].big_cpt[row]  # 'T.T.T' = 0.99

            total += (cpt_prob * enumerate_all(vars=rest_dict, evidence=evidenceV, bayes_net=bayes_net))

        return total


# loop through parent domain unknowns


def print_output(Q_normalized):

    output = ''
    for k,v in Q_normalized.items():
        output += f'P({k}) = {round(v, 3)}\t\t'
    print(f'\n{output}\n')

if __name__ == "__main__":

    model = Model()

    bayes_net = Bayes_Net(model)

    while True:

        X, e = prompt_user(bayes_net)

        Q_normalized = enumeration_ask(X=X, e=e, bn=bayes_net.Model)

        print_output(Q_normalized)

    # query = args[0] # evidence = args[1:]

    # Q_normalized = enumeration_ask(X='Alarm', e=['Burglary = T', 'Earthquake = T'], bn=bayes_net.Model)  # P(T) = 0.95		P(F) = 0.05
    # Q_norm = enumeration_ask(X=['Alarm'], e=['Earthquake = F', 'Burglary = F'], bn=bayes_net.Model)  # P(T) = 0.001		P(F) = 0.999
    # Q_norm = enumeration_ask(X=['Burglary'], e=['Alarm = T', 'JohnCalls = F'], bn=bayes_net.Model)  # P(T) = 0.001		P(F) = 0.999

    # print_output(Q_normalized)




"""

P(alarm | burglary) = P(alarm | burglary, earthquake = false) + P(alarm | burglary, earthquake = true)

P(john) = 0.9 * P(alarm)
P(john) = 0.9  * P(alarm) = 0.9 * P(alarm| earthquake, burglarly)
P(john) = p(john| alarm =true) + P(john| alarm = false)
p(john) = 0.9 * p(alarm = true)_ + 0.05 * P(alarm=false)

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

