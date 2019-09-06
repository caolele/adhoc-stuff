#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the maximumToys function below.
def maximumToys(prices, k):
    n = len(prices)
    prices = sorted(prices)
    running_sum = 0
    for i in range(n):
        running_sum += prices[i]
        if running_sum > k:
            return i 

if __name__ == '__main__':

    nk = input().split()

    n = int(nk[0])

    k = int(nk[1])

    prices = list(map(int, input().rstrip().split()))

    result = maximumToys(prices, k)

    print(result)
