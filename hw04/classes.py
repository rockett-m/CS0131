import sys
import os
import re
from collections import OrderedDict

class Variable:
    def __init__(self, name: str, domain: list, probability: float):
        self.name = name
        self.domains = domain
        self.probability = probability

class Model:
    def __init__(self):
        self.input_file = ''
        self.my_dict = OrderedDict()
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
            count = 0
            key = ''
            for line in fi:
                line = line.strip()
                fields = line.split(' ')

                if re.search(r'# Parents', line):  # count == 1
                    count += 1
                    continue

                elif re.search(r'# Tables', line):  # count == 2
                    count += 1
                    continue

                if count == 0:
                    result = re.match(r'^(.+)\s(.+)\s(.+)\s*', line)
                    if result:
                        key = result.group(1)
                        val1 = result.group(2)
                        val2 = result.group(3)

                        var = Variable(name=key, domain=[val1, val2], probability=0)
                        self.my_dict.update({var.name:var})

                        # self.Variables.add(name=key, domain=[val1, val2], probability=0)

                elif count == 1:  # parents
                    pass

                elif count == 2:  # tables
                    if (len(fields) == 1) and (key == '') and re.search(r'[A-Za-z]+', line):  # variable
                        key = fields[0]
                        continue

                    elif (len(fields) == 1) and (key != '') and re.search(r'([\d.]+)', line):  # variable
                        var = Variable(name=key, domain=[val1, val2], probability=float(fields[0]))
                        self.my_dict.update({var.name:var})
                        key = ''



