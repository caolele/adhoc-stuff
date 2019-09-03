#!/bin/python3

import math
import os
import random
import re
import sys


def getSeaLevelIdx(n, s):
    result = [-1]
    running_sum = 0
    for i in range(n):
        if s[i] == "D":
            running_sum -= 1
        elif s[i] == "U":
            running_sum += 1
        else:
            raise RuntimeError("illegal character in input!")
        if running_sum == 0:
            result.append(i) 
    return result


# Complete the countingValleys function below.
def countingValleys(n, s):
    # obtain indeces that ends on sea level, range [0, n]
    sl_idx = getSeaLevelIdx(n, s)
    # calculate the number of vallies by selecting only the
    # pairs of idx representing a vally
    result = 0
    for i in range(len(sl_idx) - 1):
        _idx = sl_idx[i]
        idx_ = sl_idx[i+1]
        c_after = s[_idx + 1]
        c_before = s[idx_]
        if c_after == "D" and c_before == "U":
            result += 1
    return result



if __name__ == '__main__':

    n = int(input())

    s = input()

    result = countingValleys(n, s)

    print(result)
