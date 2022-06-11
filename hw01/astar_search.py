#!/usr/bin/python3

from genericpath import isfile
import imp
import os
import sys


def parse_file():
    file = sys.argv[1]
    if not os.path.isfile(file):
        print(f'file not found: {file}\n')
        sys.exit()
    return file


def main():
    pass


if __name__ == "__main__":

    file = parse_file()

    main(file)