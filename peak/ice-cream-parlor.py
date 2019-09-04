#!/bin/python3

import math
import os
import random
import re
import sys

"""
It is actually a problem that is similar to the two-sum problem
except that it allows duplicated elements in the costs array
https://leetcode.com/articles/two-sum/
"""

# Complete the whatFlavors function below.
def whatFlavors(cost, money):
    n = len(cost)
    # iterate the cost
    cache = {}
    for i in range(n):
        _cost = cost[i]
        _diff = money - _cost
        if _diff in cache:
            print("{} {}".format(cache[_diff], i + 1))
            return
        if _cost not in cache:
            cache[_cost] = i + 1
        

if __name__ == '__main__':
    t = int(input())

    for t_itr in range(t):
        money = int(input())

        n = int(input())

        cost = list(map(int, input().rstrip().split()))

        whatFlavors(cost, money)
