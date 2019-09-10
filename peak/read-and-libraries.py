#!/bin/python3

import math
import os
import random
import re
import sys

# here is a somewhat okay explanation: https://fizzbuzzer.com/roads-and-libraries-challenge/
# it is more interesting prove the validity of the method using recursive approach
def roadsAndLibraries(n, c_lib, c_road, cities):

    # when c_lib <= c_road, just build a lib for each city
    # otherwise, build one lib for each connected subgraph
    if c_lib < c_road:
        return n*c_lib

    # constract graph representation
    graph = [set() for _ in range(n)]
    for path in cities:
        graph[path[0]-1].add(path[1]-1)
        graph[path[1]-1].add(path[0]-1)

    # not visited set
    to_visit = set(range(n))

    # find sub-graphs
    sub_graphs = []
    while len(to_visit) > 0:
        cache = set()
        # bfs
        _queue = [to_visit.pop()] # IMPORTANT!!! using  "_queue = [list(to_visit)[0]]" will not be able to pass all test due to performance issues
        while len(_queue) > 0:
            _node = _queue.pop(0)
            to_visit.discard(_node)
            cache.add(_node)
            for conn_node in graph[_node]:
                if conn_node in to_visit:
                    _queue.append(conn_node)
                    to_visit.discard(conn_node)
        # append the current subgraph
        if len(cache) > 0:
            sub_graphs.append(cache)

    # for the case of c_lib > c_road
    # can be merged to the previous loop
    result = 0
    for sub_graph in sub_graphs:
        result += c_lib
        result += (len(sub_graph) - 1) * c_road
    return result
            

if __name__ == '__main__':

    q = int(input())

    for q_itr in range(q):
        nmC_libC_road = input().split()

        n = int(nmC_libC_road[0])

        m = int(nmC_libC_road[1])

        c_lib = int(nmC_libC_road[2])

        c_road = int(nmC_libC_road[3])

        cities = []

        for _ in range(m):
            cities.append(list(map(int, input().rstrip().split())))

        result = roadsAndLibraries(n, c_lib, c_road, cities)

        print(result)
