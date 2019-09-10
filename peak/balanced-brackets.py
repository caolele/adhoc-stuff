#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the isBalanced function below.
def isBalanced(s):
    brackets = {
        ")": "(",
        "]": "[",
        "}": "{"
    }
    opening_brackets = set(brackets.values())
    closing_brackets = set(brackets.keys())
    cache = []
    for c in s:
        if c in opening_brackets:
            cache.append(c)
        else:
            if len(cache) > 0:
                _c = cache.pop()
                if _c != brackets[c]:
                    return "NO"
            else:
                return "NO"
    if len(cache) == 0:
        return "YES"
    else:
        return "NO"

if __name__ == '__main__':

    t = int(input())

    for t_itr in range(t):
        s = input()

        result = isBalanced(s)

        print(result)
