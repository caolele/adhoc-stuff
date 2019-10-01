#!/bin/python3

import math
import os
import random
import re
import sys

def halo(M, r, c, i, j):
    d = 1
    while True:
        if j+d >= c or M[i][j+d] == -1:
            break
        if i+d >= r or M[i+d][j] == -1:
            break
        if j-d < 0 or M[i][j-d] == -1:
            break
        if i-d < 0 or M[i-d][j] == -1:
            break
        d += 1
    return d

def get_product(a, b):
    bx, by = b[0][0], b[0][1]
    result = 0
    for k in range(1, b[1] + 1):
        first = 4 * k - 3
        b_set = {b[0]}
        for i in range(1, k):
            b_set.add((bx+i, by))
            b_set.add((bx-i, by))
            b_set.add((bx, by+i))
            b_set.add((bx, by-i))
        ax, ay = a[0][0], a[0][1]
        ar = a[1]
        for i in range(1, a[1]):
            if (ax+i, ay) in b_set or (ax-i, ay) in b_set or (ax, ay+i) in b_set or (ax, ay-i) in b_set:
                ar = i
                break
        fs = first * (4 * ar - 3)
        if fs > result:
            result = fs
    return result

# Complete the twoPluses function below.
def twoPluses(grid):
    # construct a data structure which is good for this task
    M = []
    for line in grid:
        M.append([])
        for x in line:
            if x=='B':
                M[-1].append(-1)
            elif x=='G':
                M[-1].append(0)
            else:
                continue

    # first sweep
    row = len(M)
    col = len(M[0])
    cache = {}
    for i in range(row):
        for j in range(col):
            if M[i][j] >= 0:
                M[i][j] = halo(M, row, col, i, j)
                if M[i][j] > 1:
                    cache[(i, j)] = M[i][j]

    # return the result
    result = sorted(cache.items(), key=lambda kv: kv[1])
    #first = 4 * result[0][1] - 3
    #second = 4 * result[1][1] - 3 if len(result)>1 else 1
    #return first * second
    product = 0
    rlen = len(result)
    for i in range(rlen):
        first = 4 * result[i][1] - 3
        for j in range(i+1, rlen):
            fs = get_product(result[j], result[i])
            if fs > product:
                product = fs
        if i == rlen - 1:
            if first > product:
                product = first
    return product


if __name__ == '__main__':

    nm = input().split()

    n = int(nm[0])

    m = int(nm[1])

    grid = []

    for _ in range(n):
        grid_item = input()
        grid.append(grid_item)

    result = twoPluses(grid)

    print(result)
