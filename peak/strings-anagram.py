#!/bin/python3

import math
import os
import random
import re
import sys


def is_ana(a, b):
    # build a cache using a
    cache = {}
    for c in a:
        if c in cache:
            cache[c] += 1
        else:
            cache[c] = 1
    # remove common letters while iterating b
    for c in b:
        if c in cache and cache[c] > 0:
            cache[c] -= 1
        else:
            continue
    # sum in cache dict
    result = 0
    for v in cache.values():
        result += v
    return result


# Complete the anagram function below.
def anagram(s):
    n_s = len(s)
    # odd length will not be possible
    if n_s % 2 != 0:
        return -1
    else: # possible case
        _mid = int(n_s / 2)
        return is_ana(s[:_mid], s[_mid:])


if __name__ == '__main__':

    q = int(input())

    for q_itr in range(q):
        s = input()

        result = anagram(s)

        print(result)
