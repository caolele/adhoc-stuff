#!/bin/python3

import math
import os
import random
import re
import sys


# use dp[i][i] to represent reachability (i.e. broadcasted from the first pair
# of element, wether they need to be compared in order to obtain the final result)
def abbreviation(a, b):
    n, m = len(a), len(b)
    dp = [[False for i in range(m+1)] for j in range(n+1)]
    dp[0][0] = True
    
    for i in range(n):
        for j in range(m+1):
            if not dp[i][j]: 
                continue
            if j<m and a[i].upper() == b[j]:
                dp[i+1][j+1] = True
            if a[i].islower():
                dp[i+1][j] = True
    return "YES" if dp[n][m] else "NO"
        


def abbreviation_recursive(a, b):
    result = False
    memo = set()
    
    def rec_func(_a, _b):
        nonlocal result
        nonlocal memo
        len_a = len(_a)
        len_b = len(_b)
        if result or len_b > len_a:
            return
        if len_b < 1:
            if all(c.islower() for c in _a):
                result = True
            return
        
        _pair = "{}-{}".format(_a, _b)
        if _pair in memo:
            return
        else:
            memo.add(_pair)
        
        a_head = _a[0]
        # remove lower case letter
        if a_head.islower():
            rec_func(_a[1:], _b)
        # try to match: fail
        if a_head.upper() != _b[0]:
            return
        # try to match: success
        rec_func(_a[1:], _b[1:])
        
    rec_func(a, b)
    
    return ("YES" if result else "NO")
        
            

if __name__ == '__main__':

    q = int(input())

    for q_itr in range(q):
        a = input()

        b = input()

        result = abbreviation(a, b)

        print(result)
