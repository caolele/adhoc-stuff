#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the jumpingOnClouds function below.
def jumpingOnClouds(c):
    # init cache array
    # -1: not processed
    # 0: processed, yet no need to stand on
    # 1: process, and will be stand on
    n = len(c)
    cache = [-1] * n
    # process thunder and their neighbors
    for idx, var in enumerate(c):
        if var == 1:
            cache[idx] = 0
            cache[idx - 1] = 1
            cache[idx + 1] = 1
    # traverse from the first cache element 
    # using a greedy strategy to calculate result
    idx = 0
    result = 0
    while(True):
        if idx >= n - 1:
            break
        result += 1
        if idx + 2 <= n - 1 and cache[idx + 2] != 0:
            idx = idx + 2
        else:
            idx += 1
    return result
        
            

if __name__ == '__main__':

    n = int(input())

    c = list(map(int, input().rstrip().split()))

    result = jumpingOnClouds(c)

    print(result)
