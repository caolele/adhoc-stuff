#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the makeAnagram function below.
def makeAnagram(a, b):
    len_a = len(a)
    len_b = len(b)
    # iterate the first array
    ref_dict = {}
    for i in range(len_a):
        _char = a[i]
        if _char in ref_dict:
            ref_dict[_char] += 1
        else:
            ref_dict[_char] = 1
    # iterate the second array
    result = 0
    for i in range(len_b):
        _char = b[i]
        if _char in ref_dict:
            ref_dict[_char] -= 1
            if ref_dict[_char] <= 0:
                del ref_dict[_char]
        else:
            result += 1
    # handle the residual
    for key in ref_dict:
        result += ref_dict[key]
    return result


if __name__ == '__main__':

    a = input()

    b = input()

    res = makeAnagram(a, b)

    print(res)
