#!/usr/bin/python3
import math
import os
import sys
import re
import time
from collections import OrderedDict
from functools import wraps
import networkx as nx
from math import *
import heapq

# run as ./astar_search.py ./inputData/cities02.txt
# > La Crosse
# > New York

def timeit(func):
    @wraps(func)
    def measure_time(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("@timefn: {} took {} seconds.\n".format(func.__name__, round(end_time - start_time, 2)))
        return result
    return measure_time


def parse_file():
    file = sys.argv[1]
    if not os.path.isfile(file):
        print(f'file not found: {file}\n')
        sys.exit()
    # else:
    #     with open(file, 'r') as fi:
    #         for line in fi:
    #             print(line)
    return file


def read_file(file):

    city_dict = OrderedDict()
    dist_dict = OrderedDict()

    with open(file, 'r') as fi:

        coords = False
        distances = False

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
                    lat = float(result.group(2))
                    long = float(result.group(3))
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
                    dist = float(result.group(3))
                    # print(f'\tcity1: {city1}; city2: {city2}; dist: {dist}\n')
                    if city1 not in dist_dict.keys():
                        dist_dict[city1] = []
                    dist_dict[city1].append([city2, dist])

                else:
                    print(f'error: [distances] result not found:\n\t{line}')

    return city_dict, dist_dict


def create_graph(city_dict: dict, dist_dict: dict, debug=False):

    graph = nx.Graph()

    for k, v in city_dict.items():
        graph.add_node(k)
        graph.nodes[k]['pos'] = (v[0], v[1])  # city lat lon

    # print(f"{graph}\n{graph.nodes}\n{graph.nodes['Winona']['pos'][0]}")

    for keys, values in dist_dict.items():
        for elem in values:

            city1 = keys
            city2 = elem[0]
            dist = float(elem[1])

            graph.add_edge(city1, city2, distance=dist)

    # print(f"{graph}\n{graph.nodes}\n{graph.edges}\n")
    if debug:
        print(graph.edges(data=True))
        # print(graph.nodes(data=True))
    return graph


def calc_direct_distance(graph, S: str, G: str, debug=False):

    lon2 = graph.nodes[G]['pos'][1]
    lon1 = graph.nodes[S]['pos'][1]

    lat2 = graph.nodes[G]['pos'][0]
    lat1 = graph.nodes[S]['pos'][0]

    lon1, lon2, lat1, lat2 = map(radians, [lon1, lon2, lat1, lat2])  # convert from degrees to radians

    lon_dist = lon2 - lon1
    lat_dist = lat2 - lat1

    a = pow(sin(lat_dist/2), 2) + cos(lat1) * cos(lat2) * pow(sin(lon_dist/2), 2)

    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d_total = round(c * 3958.8, 2)  # radius of the earth in miles (6371 km)

    if debug:
        print(f"Distance between starting city: '{S}' and goal city: '{G}' is {d_total} miles.")
    return d_total


def input_handling(graph, src_or_dst: str, var: str): # input_handling(graph, 'Starting', 'S')
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


def prompt_user(graph):  # 'S' = starting city; 'G' = goal city

    print('[MSG] cities are parsed and graph is created\n')

    S = input_handling(graph, 'Starting', 'S')

    G = input_handling(graph, 'Goal', 'G')

    return S, G


class TreeNode:
    '''Object for storing search-tree node data.

       Members:
       --------
       state: 8-puzzle configuration as 2-dimensional array
       action: Action item that led to this state in search
           Note: will be None if and only if this is starting state
       cost: depth of node in search-tree
       parent: TreeNode that led to this node in search
           Note: will be None if and only if this is starting state

        Implicits
        ---------
        String conversion: defined based upon state.
        Comparison: lt (<) operator compares cost.

        Methods
        -------
        isGoal: returns true if and only if this node's state is identical to GOAL_STATE

        pathCost: returns (cost + 1) if supplied with node that has self as parent
            Note: will return arbitrarily large value if node has a different parent
    '''
    def __init__(self, state, cost=0, parent_node=None):
        self.state = state
        self.cost = cost
        self.parent_node = parent_node

    def __lt__(self, next_node):
        return self.cost < next_node.cost

    def __str__(self):
        return str(self.state)

    def isGoal(self, G):
        return str(self) == str(G)

    def pathCost(self, next_node, g):
        if next_node.parent_node == self:
            return self.cost + g
        return math.inf


@timeit

def astar_search_unopt(graph, S: str, G: str):

    curr_node = TreeNode(state=S)

    frontier = [curr_node]
    heapq.heapify(frontier)

    visited_nodes = OrderedDict()
    visited_nodes = {str(curr_node): 0}

    while frontier:
        curr_node = heapq.heappop(frontier)

        if curr_node.isGoal(G):
            nodes_left = len(frontier)
            total_nodes = len(visited_nodes) + nodes_left
            print(f'Total nodes generated: {total_nodes}\nNodes left in frontier: {nodes_left}\n')
            return curr_node

        for child_node in graph.neighbors(curr_node.state):

            if child_node not in visited_nodes:

                h = calc_direct_distance(graph, S=child_node, G=G)
                g = graph.edges[(curr_node.state, child_node)]['distance']
                f = h + g

                child = TreeNode(state=child_node, cost=0, parent_node=curr_node)
                child.cost = curr_node.pathCost(child, g)

                if (child.state not in visited_nodes.keys()) or (child.state in visited_nodes.keys() and g < visited_nodes[child.state].cost):

                    visited_nodes.update({child:g})  # g or f
                    heapq.heappush(frontier, child)

    return -1


@timeit
def astar_search_opt(graph, S: str, G: str):

    curr_node = TreeNode(state=S)

    frontier = [curr_node]
    heapq.heapify(frontier)

    visited_nodes = {str(curr_node): 0}

    while frontier:
        curr_node = heapq.heappop(frontier)

        if curr_node.isGoal(G):
            nodes_left = len(frontier)
            total_nodes = len(visited_nodes) + nodes_left
            print(f'Total nodes generated: {total_nodes}\nNodes left in frontier: {nodes_left}\n')
            return curr_node

        for children in graph.edges(curr_node.state):
            child_node = children[1]  # parent_node = children[0]

            if child_node not in visited_nodes:

                h = calc_direct_distance(graph, S=child_node, G=G)
                g = graph.edges[children]["distance"]
                f = h + g

                child = TreeNode(state=child_node, cost=0, parent_node=curr_node)
                child.cost = curr_node.pathCost(child, g)

                if (child not in visited_nodes) or (child in visited_nodes and g < visited_nodes[child].cost):
                    # if (child not in visited_nodes) or (child in visited_nodes and g < visited_nodes[child]):
                    visited_nodes.update({child:g})
                    heapq.heappush(frontier, child)

    return -1  # path not found


def printSolution(solution_node):
    '''Prints out solution path from start-to-finish, after best-first-search.
       Back-tracks from solution to start and prints the states and actions of
       a solution path, in (start -> solution) order.

       Args
       ----
       solution_node: a TreeNode returned by best_first_search()
    '''
    if solution_node == -1:
        print(f'no path found. Exiting...')
        sys.exit()
    solution_path = [solution_node]
    parent_node = solution_node.parent_node
    while parent_node is not None:
        solution_path.insert(0, parent_node)
        parent_node = parent_node.parent_node

    path = solution_path[0]
    for i in range(1, len(solution_path)):
        path = f'{path} -> {solution_path[i]}'
    print(f'optimal path:\n\n{path}\n\ndistance traveled:\t{solution_node.cost} miles\n')


if __name__ == "__main__":

    file = parse_file()

    city_dict, dist_dict = read_file(file)

    graph = create_graph(city_dict, dist_dict, debug=False)

    # """ prompt version
    S, G = prompt_user(graph)

    solution_node_unopt = astar_search_unopt(graph, S, G)
    printSolution(solution_node_unopt)

    solution_node_opt = astar_search_opt(graph, S, G)
    printSolution(solution_node_opt)
    # """

    """ manual bypass input run
    solution_node_unopt = astar_search_unopt(graph, S='La Crosse', G='New York')
    printSolution(solution_node_unopt)

    solution_node_opt = astar_search_opt(graph, S='La Crosse', G='New York')
    printSolution(solution_node_opt)
    # """

    sys.exit()



# implement best first search
# current path cost and heuristic value

# dictionary to keep track of what is seen
# store g the

# f = g + h
# f - decide who to choose next - lowest values
# h = straight line
# g = cost to get there from the start

# start has g=0
# end has h=0

# keep track of current dist taken so far
# g+h = f - decide which to

# shortest f value
# sum actual dist   g
# heuristic dist

# frontier ordered by f value from smallest to largest
# check heapify

# for each child, what is the f and what is the g value

# heuristic is straight line distance S -> G    # underestimate unless straight path somehow

# g is actual drive distance    # real cost

# f combining the h and the g

    # start has g=0
    # end has h=0

# edges are g values

