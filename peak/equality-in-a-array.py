#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the equalizeArray function below.
def equalizeArray(arr):
    n = len(arr)
    cache = {}
    for num in arr:
        if num in cache:
            cache[num] += 1
        else:
            cache[num] = 1
    result = n
    for key in cache:
        to_remove = n - cache[key]
        if to_remove < result:
            result = to_remove
    return result

if __name__ == '__main__':

    n = int(input())

    arr = list(map(int, input().rstrip().split()))

    result = equalizeArray(arr)

    print(result)
