#!/usr/bin/python3
import os
import sys
import re
from collections import OrderedDict
import numpy as np

from classes import *


def parse_args(input_args):

    cond = []; args = []

    fields = input_args.strip()
    fields = input_args.split(' | ')  # requires space between |
    if len(fields) == 2:
        cond = fields[-1].split(', ')

    args.insert(0, fields[0])
    args += cond

    X, e = args[0], args[1:]

    if input_args != "quit":
        return X, e
    else:
        sys.exit(f'{input_args}\n')


class Bayes_Net:
    def __init__(self, Model):
        self.Model = Model

        # self.Model.convert_cpt_tuple()
        # self.Model.enumeration_ask()  # calls self.Model.enumeration_all() inside
        # enumeration_ask(X=, evidence=, net=Model)  # calls self.Model.enumeration_all() inside
        # self.Model.print_cpt()

def normalize(dist):
    "Normalize a {key: value} distribution so values sum to 1.0. Mutates dist and returns it."
    total = sum(dist.values())
    for key in dist:
        dist[key] = dist[key] / total
        assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
    return dist


def print_output(Q_normalized):

    output = ''
    for k,v in Q_normalized.items():
        output += f'P({k}) = {round(v, 3)}\t\t'
    print(f'\n{output}\n')


def enumeration_ask(X: str, e: list, bn):
    # check if both parents aren't there CPT   # T.T.T   # incomplete lookups
    # vars = list(bn.Variables.keys())
    evidence_dict = OrderedDict()
    for i in e:  # 'Earthquake = T' => 'Earthquake'
        evidence_dict[i.split(' = ')[0]] = i.split(' = ')[1]   # evidence_dict['Earthquake'] = 'T'
    assert X not in evidence_dict.keys(), "Query variable must be distinct from evidence"

    Q = OrderedDict()
    for xi in bn.Variables[X].domains:  # T, F

        evidence_dict[X] = xi  # 'Alarm' = 'T'  # add to dict
        Q[xi] = enumerate_all(vars=bn.Variables, evidence=evidence_dict, bayes_net=bn)  # Q['T'] = 0.001

    return normalize(Q)  # {Q['T'] = 0.001, Q['F'] = 0.999}


def enumerate_all(vars: dict, evidence: dict, bayes_net):

    if len(vars) == 0: return 1.0

    var_names = list(vars.keys())
    V, rest = var_names[0], var_names[1:]
    Vnode = vars[V]

    rest_dict = OrderedDict()  # n-1 length vs prior run
    for elem in rest:
        if elem in vars.keys():
            rest_dict.update({elem:vars[elem]})
    # print(f'{V = } : {rest = }')

    if V in evidence.keys():  # only go here if full CPT lookup possible ***

        row = ''  # create the cpt row now
        if len(Vnode.parents) > 0:
            for parent in Vnode.parents:  # ['Burglary', 'Earthquake']  # has to be added to ev set first
                row += f'{evidence[parent]}__'  # T.

        row += evidence[V]  # 0.99  # exact cpt row match expected like 'T.T.T' = 0.99
        # print(f'if row {row}')
        # if row in vars[V].big_cpt.keys():
        cpt_prob = Vnode.big_cpt[row]  # 'T.T.T' = 0.99

        return cpt_prob * enumerate_all(vars=rest_dict, evidence=evidence, bayes_net=bayes_net)

    else: # no exact match found in cpt
        total = 0
        evidenceV = evidence.copy()
        for domain_val in Vnode.domains:  # loop through parent unknowns too

            evidenceV.update({V:domain_val})  # extend to add possible values
            row = ''  # create the cpt row now
            if len(Vnode.parents) > 0:
                for parent in Vnode.parents:  # ['Burglary', 'Earthquake']
                    row += f'{evidenceV[parent]}__'  # T.

            row += domain_val  # 0.99  # exact cpt row match expected like 'T.T.T' = 0.99
            # print(f'else row {row} : {V = } : {domain_val = }')

            cpt_prob = Vnode.big_cpt[row]  # 'T.T.T' = 0.99

            total += (cpt_prob * enumerate_all(vars=rest_dict, evidence=evidenceV, bayes_net=bayes_net))

        return total


if __name__ == "__main__":

    model = Model()

    bayes_net = Bayes_Net(model)

    # print(f'\nPRINTING big cpts:\n')

    bayes_net.Model.print_big_cpt()
    """ testing
    burglary_test = [
        "Burglary",
        "JohnCalls | Alarm = T",
        'Burglary | JohnCalls = T, MaryCalls = T',
        'Alarm | Burglary = T',
        'Alarm | Burglary = T, Earthquake = T',
        'Alarm | Earthquake = F, Burglary = F',
        'MaryCalls | Alarm = T',
        'MaryCalls | Alarm = F',
        'Burglary | Earthquake = T',
        'Burglary | Earthquake = F',
        'Burglary | Alarm = T',
        'Burglary | Alarm = T, JohnCalls = F',
        'JohnCalls | Burglary = T, Alarm = T',
        'JohnCalls | Burglary = T, Earthquake = T, Alarm = T',
    ]
    for test in burglary_test:
        X, e = parse_args(test)
        Q_normalized = enumeration_ask(X=X, e=e, bn=bayes_net.Model)
        print(test)
        print_output(Q_normalized)
    """

    while True:

        user_input = input()

        X, e = parse_args(user_input)

        Q_normalized = enumeration_ask(X=X, e=e, bn=bayes_net.Model)

        print_output(Q_normalized)

""" Test code
Alarm | Burglary = T, Earthquake = T
"""
