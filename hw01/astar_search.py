#!/usr/bin/python3
import heapq
import math
import os
import sys
import re
from collections import OrderedDict
from operator import itemgetter
from queue import PriorityQueue
import networkx as nx
from math import *
import matplotlib.pyplot as plt
import heapq
import scipy


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


def astar_search(graph, S: str, G: str):

    print(f'starting city: {S}\tgoal city: {G}\n')

    h = calc_direct_distance(graph, S, G)
    g = 0
    f = h + g

    # frontier = PriorityQueue()
    frontier = PriorityQueue()
    frontier.put(S, 0)


    visited_nodes = []
    total_distance = 0
    nodes_viewed = 1
    edges_count = 0

    while not frontier.empty():  # not empty

        node = frontier.get()  # smallest f value at front

        visited_nodes.append(node)

        print(f'node: {node}')
        visited = [node]

        if node == G:
            print(f'goal found: {G}\ntotal distance: {total_distance}')
            break

        curr_neighbors = []
        for node_neighbor in graph.edges(node):
            edges_count += 1

            parent_node =  node_neighbor[0]
            current_node = node_neighbor[1]

            if current_node not in visited_nodes:
                nodes_viewed += 1
                h = calc_direct_distance(graph, current_node, G)
                g = graph.edges[node_neighbor]["distance"]
                f = h + g

                print(f"parent node: '{parent_node}'\nchild node:  '{current_node}'\nh: {h}\ng: {g}\nf: {f}\n")

                frontier.put(current_node, block=f)  # only if shorter path
        print(f'frontier: {frontier.queue}')


    # find edge distance between each pair in visited nodes
    # sum up for total distance

    # for i
    # graph.edges()

    path = ' -> '.join(visited_nodes)
    node_count = len(visited_nodes)
    frontier_count = len(frontier.queue)
    print(f'edges viewed: {edges_count}')

    print(f'nodes calculated: {nodes_viewed}')

    print(f'\n{node_count} nodes visited\n\n{frontier_count} nodes left in the frontier\n\n'
          f'path:\t{path}\n\ntotal_distance: {total_distance} miles\n')
    return visited_nodes, total_distance


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
    def __init__(self, state, action=None, cost=0, parent_node=None):
        self.state = state
        self.action = action
        self.cost = cost
        self.parent_node = parent_node

    def __lt__(self, next_node):
        return self.cost < next_node.cost

    def __str__(self):
        return str(self.state)

    def isGoal(self, G):
        return str(self) == str(G)

    # def pathCost(self, next_node):
    def pathCost(self, next_node, g):
        if next_node.parent_node == self:
            return self.cost + g

        return math.inf

    '''
    In the basic version of the node class, actions all have the same cost (1 per step in search),
    leading search to always default to breadth-first, since the priority queue will be ordered
    by tree depth.  If some actions actually cost more than others, however, we could still order
    by path-cost, without it being equivalent to tree-depth.  In such cases the best-first search
    algorithm is then identical to Dijkstra's algorithm, searching for a shortest path according
    to total action-cost.  

    Here is an example in which going UP costs twice as much as other actions:
    
    def pathCost(self, next_node):
        if next_node.parent == self:
            if next_node.action == Action.UP:
                return self.cost + 2
            else:
                return self.cost + 1
        
        return math.inf
    '''



def astar_search_sat(graph, S: str, G: str):

    print(f'starting city: {S}\tgoal city: {G}\n')

    curr_node = TreeNode(state=S)

    frontier = [curr_node]
    heapq.heapify(frontier)

    visited_nodes = {str(curr_node): 0}
    city_paths_dict = {str(curr_node): 0}

    while frontier:
        curr_node = heapq.heappop(frontier)

        if curr_node.isGoal(G):
            print(curr_node.cost)
            return curr_node

        for children in graph.edges(curr_node.state):
            # parent_node = children[0]
            child_node =  children[1]

            h = calc_direct_distance(graph, S=child_node, G=G)
            g = graph.edges[children]["distance"]
            f = h + g

            if child_node not in visited_nodes:
                child = TreeNode(state=child_node, cost=0, parent_node=curr_node)

                # child.cost = node.pathCost(g)
                child.cost = curr_node.pathCost(child, g)
                city_paths_dict.update({child:child.cost})

                # print(f"parent node: '{curr_node}'\nchild node:  '{child_node}'\n")

                # print(f'child node: {child}')
                # if (child not in visited_nodes) and (child not in frontier):
                    # and child.cost < visited_nodes[child]):  # visited_nodes[child].cost
                if (child not in visited_nodes) or (child in visited_nodes and child.cost < visited_nodes[child].cost):  # visited_nodes[child].cost
                    # visited_nodes.update({child:f})  # {child:child.cost}
                    heapq.heappush(frontier, child)

        #
        # for k,v in city_paths_dict.items():
        #     print(k,v)
        #
        # print('\n')

    return None

"""

    curr_neighbors = []
    for node_neighbor in graph.edges(node):
        edges_count += 1

        parent_node =  node_neighbor[0]
        current_node = node_neighbor[1]

        if current_node not in visited_nodes:
            nodes_viewed += 1
            h = calc_direct_distance(graph, current_node, G)
            g = graph.edges[node_neighbor]["distance"]
            f = h + g

            print(f"parent node: '{parent_node}'\nchild node:  '{current_node}'\nh: {h}\ng: {g}\nf: {f}\n")

            frontier.put(current_node, block=f)  # only if shorter path
    print(f'frontier: {frontier.queue}')
"""

def printSolution(solution_node):
    '''Prints out solution path from start-to-finish, after best-first-search.
       Back-tracks from solution to start and prints the states and actions of
       a solution path, in (start -> solution) order.

       Args
       ----
       solution_node: a TreeNode returned by best_first_search()
    '''
    solution_path = [solution_node]
    parent_node = solution_node.parent_node
    while parent_node != None:
        solution_path.insert(0, parent_node)
        parent_node = parent_node.parent_node

    path = solution_path[0]
    for i in range(1, len(solution_path)):
        path = f'{path} -> {solution_path[i]}'
    print(path)

# def a_star_search(graph, start, goal):
#     # frontier = PriorityQueue()
#     # frontier.put(start, 0)
#     came_from = {start: None}
#     cost_so_far = {start: 0}
#
#     while not frontier.empty():
#         current = frontier.get()
#
#         if current == goal:
#             break
#
#         for next in graph.neighbors(current):
#             new_cost = cost_so_far[current] + graph.cost(current, next)
#             if next not in cost_so_far or new_cost < cost_so_far[next]:
#                 cost_so_far[next] = new_cost
#                 priority = new_cost + heuristic(goal, next)
#                 frontier.put(next, priority)
#                 came_from[next] = current
#
#     return came_from, cost_so_far


"""
def astar_search(graph, S: str, G: str):

    # nx.draw(graph)
    nx.draw_networkx(graph, arrows=True, with_labels=True)
    plt.show()

    
    graph.nodes[k]

    
    edge = ''
    h = graph.edges[edge]['distance']
    
    current_nodes = [S]
    visited_nodes = []



    while len(current_nodes) > 0:
        node = None

        for c in current_nodes:
            if node == None


    C = current city
    for neighbor_node in graph.neighbors():
        gC = calc_direct_distance(graph, S, C)
        hC = calc_direct_distance(graph, C, G)
        fC = gC + hC


"""

# class Node:
#     def __init__(self):
#         self.h = h
#         self.g = g
#         self.f = f





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

if __name__ == "__main__":

    file = parse_file()

    city_dict, dist_dict = read_file(file)

    graph = create_graph(city_dict, dist_dict, debug=True)

    # astar_search(graph, S='La Crosse', G='Minneapolis')
    # solution_node = astar_search_sat(graph, S='La Crosse', G='Minneapolis')
    solution_node = astar_search_sat(graph, S='La Crosse', G='New York')
    # solution_node = astar_search_sat(graph, S='New York', G='London')

    printSolution(solution_node)

    sys.exit()
    # S, G = prompt_user(graph)

    # astar_search(graph, S='La Crosse', G='Minneapolis')
    # update_edge_weights(graph, debug=True)

    S, G = prompt_user(graph)

    calc_direct_distance(graph, S, G, debug=True)

    # heuristic is straight line distance S -> G    # underestimate unless straight path somehow

    # g is actual drive distance    # real cost

    # f combining the h and the g

        # start has g=0
        # end has h=0

    # edges are g values


