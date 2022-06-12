#!/usr/bin/python3

import os
import sys
import re
from collections import OrderedDict
import networkx as nx
from math import *


def parse_file():
    file = sys.argv[1]
    if not os.path.isfile(file):
        print(f'file not found: {file}\n')
        sys.exit()
    else:
        with open(file, 'r') as fi:
            for line in fi:
                print(line)
    return file


def read_file(file):

    city_dict = OrderedDict()
    dist_dict = OrderedDict()

    with open(file, 'r') as fi:

        coords = False; distances = False

        for line in fi:

            if re.search("# name latitude longitude", line):
                coords = True
                distances = False
                continue
            elif re.search("# distances", line):
                distances = True
                coords = False
                continue

            if coords and not distances:
                # result = re.match(r'([A-Za-z\s]+)\s+(-*[\d.]+)\s+(-*[\d.]+)', line)
                result = re.match(r'(.+)\s+(-*[\d.]+)\s+(-*[\d.]+)', line)
                if result:
                    city = result.group(1)
                    lat = result.group(2)
                    long = result.group(3)
                    # print(f'\tcity: {city}; lat: {lat}; long: {long}\n')
                    if city not in city_dict.keys():
                        city_dict[city] = [lat, long]
                else:
                    print(f'error: [coords] result not found:\n\t{line}\n')

            elif distances and not coords:
                result = re.match(r'(.+),\s(.+):\s+(-*[\d.]+)', line)
                if result:
                    city1 = result.group(1)
                    city2 = result.group(2)
                    dist = result.group(3)
                    # print(f'\tcity1: {city1}; city2: {city2}; dist: {dist}\n')
                    if city1 not in dist_dict.keys():
                        dist_dict[city1] = []
                    dist_dict[city1].append([city2, dist])

                else:
                    print(f'error: [distances] result not found:\n\t{line}')

    return city_dict, dist_dict


def create_graph(city_dict: dict, dist_dict: dict):
    graph = nx.Graph()

    for k, v in city_dict.items():
        graph.add_node(k)

    for keys, values in dist_dict.items():
        for elem in values:

            city1 = keys
            city2 = elem[0]
            dist = elem[1]

            graph.add_edge(city1, city2, length=dist)

    # print(f'{G}\n{G.nodes}\n{G.edges}\n')

    return graph


def input_handling(graph, src_or_dst, var): # input_handling(graph, 'Starting', 'S')
    city = input(f"Please enter a {src_or_dst} city, '{var}', and press 'Enter' when done\n")
    # city = input("Please enter a starting city, 'S', and press 'Enter' when done\n")
    if city == '0':
        sys.stdout.write("Program terminated; '0' was entered. Exiting...\n")
        sys.exit()

    while city not in graph.nodes:
        if city == '0':
            sys.stdout.write("Program terminated; '0' was entered. Exiting...\n")
            sys.exit()
        city = input(f"City: '{city}' not found\n\nPlease enter a {src_or_dst} city, '{var}', and press 'Enter' when done\n")

    print(f"{src_or_dst} city, '{var}': '{city}' found in graph\n")
    return city


def prompt_user(graph): # 'S' = starting city; 'G' = goal city

    print('[MSG] cities are parsed and graph is created\n')

    S = input_handling(graph, 'Starting', 'S')

    G = input_handling(graph, 'Goal', 'G')

    return S, G


def astar_search(S, G, graph, city_dict):

    lon2 = float(city_dict[G][1])
    lon1 = float(city_dict[S][1])

    lat2 = float(city_dict[G][0])
    lat1 = float(city_dict[S][0])

    lon1, lon2, lat1, lat2 = map(radians, [lon1, lon2, lat1, lat2]) # convert from degrees to radians

    lon_dist = lon2 - lon1
    lat_dist = lat2 - lat1

    a = pow(sin(lat_dist/2), 2) + cos(lat1) * cos(lat2) * pow(sin(lon_dist/2), 2)

    c = 2 * atan2(sqrt(a), sqrt(1-a))
    dist = c * 3958.8  # radius of the earth in miles (6371 km)



if __name__ == "__main__":

    file = parse_file()

    city_dict, dist_dict = read_file(file)

    graph = create_graph(city_dict, dist_dict)

    S, G = prompt_user(graph)

    astar_search(S, G, graph, city_dict)


# References
#     http://andrew.hedges.name/experiments/haversine/
#     https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97