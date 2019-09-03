#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the repeatedString function below.
def repeatedString(s, n):
    # number of complete repetitions and tails
    s_len = len(s)
    n_rep = int(n / s_len) # floor
    n_tail = n % s_len

    # a occurances in s
    result = s.count("a")

    # calc head a occurances
    result *= n_rep

    # add tail a's
    result += s[:n_tail].count("a")

    return result


if __name__ == '__main__':

    s = input()

    n = int(input())

    result = repeatedString(s, n)

    print(result)
