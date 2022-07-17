#!/usr/bin/python3
import os
import sys
import re
from collections import OrderedDict

class Knowledge_Base:

    def __init__(self):
        self.symbols_list = []; self.final_symbols_list = []
        self.clauses_list = []; self.final_clauses_list = []
        self.symbols_count = 0; self.condional_count = 0
        self.parse_cli()
        self.create_kb()

    def parse_cli(self):
        # read user input on what knowledge base to use
        self.kbase_file = sys.argv[1]
        if len(sys.argv) > 1:
            self.debug = True
        else:
            self.debug = False

        if not os.path.isfile(self.kbase_file):
            print(f'file not found: {self.kbase_file = }\n')
            sys.exit("run: python forward_chain.py kb_00.txt ")

    def create_kb(self):
        with open(self.kbase_file, 'r') as fi:

            for line in fi:
                line = line.strip()       # strip newline
                fields = line.split(' ')  # separate fields by spaces

                if len(fields) == 1:      # symbol if only one field per line
                    self.symbols_count += 1
                    self.symbols_list.append(fields[0])
                else:
                    self.condional_count += 1
                    self.clauses_list.append(line)

        # will want copies before updating KB
        self.final_symbols_list = self.symbols_list.copy()
        self.final_clauses_list = self.clauses_list.copy()

    def update_kb(self):
        # loop through all clauses to check entailment
        prev_symbols_list = self.final_symbols_list.copy()

        line_count = 0
        for line in self.final_clauses_list:
            line = line.strip()
            # len line always odd 3, 5, 7, ... fields
            # THEN always second-to-last element  line[-2]
            # p# that is last element is always compared   line[-1]
            fields = line.split(' ')
            last_elem = fields[-1]
            # simple case with no AND's
            if len(fields) == 3:  # line == p7 THEN p1
                if (fields[0] in self.final_symbols_list) and (last_elem not in self.final_symbols_list):  # line[0] == p7,  line[-1] == p1
                    self.final_symbols_list.append(last_elem)
                    self.final_clauses_list.pop(line_count)  # work is done here

            # one or more AND's and 5+ fields
            else:
                # line == p1 AND p2 AND p3 THEN p4
                # and_subsection == p1 AND p2 AND p3
                # conditionals == p1, p2, p3

                and_subsection = fields[:-2]  # remove last 2 elem
                conditionals = []
                for elem in and_subsection:
                    if not re.search('AND', elem):
                        conditionals.append(elem)  # only update if symbol, not an AND

                # need all conditionals to be in symbol list for a potential update
                # check = all(item in conditionals for item in self.final_symbols_list)
                check = True
                for item in conditionals:
                    if item not in self.final_symbols_list:
                        check = False; break

                # list not set so we don't want to add any duplicate items to symbols_list
                if self.debug:
                    print(f'{fields = }\n{and_subsection = }\n{conditionals = }\n{check = }\n')

                if check and (last_elem not in self.final_symbols_list):
                    self.final_symbols_list.append(last_elem)
                    self.final_clauses_list.pop(line_count)  # work is done here

            line_count += 1

        if len(self.final_symbols_list) == len(prev_symbols_list):
            # no more changes after running through all KB clauses
            return False

        # or keep going and start again from the top
        return True  # default is True - keep looping

    def print_kb_info(self):
        print(f'\nKB has {knowledge_base.condional_count} conditional clauses and {knowledge_base.symbols_count} propositional symbols.')
        print(f'\nClauses:\n'); [print(x) for x in knowledge_base.clauses_list]
        print(f'\nSymbols:\n'); [print(x) for x in knowledge_base.symbols_list]; print('\n')

    def prompt_user(self):
        # prompt user for symbol until 'end' is typed
        user_input = input('Query symbol (or end): ')
        user_input.strip()  # remove newline
        if user_input != "end":
            self.check_entailment(user_input)
        else:
            sys.exit(f'{user_input}\n')

    def check_entailment(self, user_input: str) -> None:

        if user_input not in self.final_symbols_list:
            print(f'No! {user_input} is not entailed by out knowledge-base\n')
        else:
            print(f'Yes! {user_input} is entailed by out knowledge-base\n')


if __name__ == "__main__":
    # RUN
    # ./forward_chain.py inputData/kb_00.txt [debug]
    knowledge_base = Knowledge_Base()

    knowledge_base.print_kb_info()

    if len(knowledge_base.final_clauses_list) == 0:  # even though seemingly pointless...
        # check_entailment() inside prompt_user() relies on self.final_symbols_list
        # which is generated by update_kb() # so running once for data structures
        knowledge_base.update_kb()

    update = True
    while (len(knowledge_base.final_clauses_list) > 0) and update:
        # continuously run until no more elem in clause list
        # elems get popped from list once the logic is satisfied and symbol list is updated
        update = knowledge_base.update_kb()
        if knowledge_base.debug:
            print(f'{knowledge_base.final_clauses_list = }')
            print(f'{knowledge_base.final_symbols_list = }\n\n')

    while True:
        knowledge_base.prompt_user()
