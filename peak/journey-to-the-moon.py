#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the journeyToMoon function below.
def journeyToMoon(n, astronaut):
    # build a graph representation
    graph = {}
    for pair in astronaut:
        n0, n1 = pair[0], pair[1]
        if n0 in graph:
            graph[n0].append(n1)
        else:
            graph[n0] = [n1]
        if n1 in graph:
            graph[n1].append(n0)
        else:
            graph[n1] = [n0]

    # find all sub graphs
    running_sum = 0
    result = 0
    to_visit = set(range(n))
    while len(to_visit) > 0:
        cache = 0
        # DFS for current sub-graph
        queue = [to_visit.pop()]
        while len(queue) > 0:
            _node = queue.pop(0)
            cache += 1
            if _node not in graph:
                break
            for adj_node in graph[_node]:
                if adj_node in to_visit:
                    to_visit.remove(adj_node)
                    queue.append(adj_node)
        # formula: new answer = old answer + sum of old values * new value
        if running_sum != 0:
            result = result + running_sum * cache
            running_sum += cache
        else:
            running_sum = cache
    return result

if __name__ == '__main__':

    np = input().split()

    n = int(np[0])

    p = int(np[1])

    astronaut = []

    for _ in range(p):
        astronaut.append(list(map(int, input().rstrip().split())))

    result = journeyToMoon(n, astronaut)

    print(result)
