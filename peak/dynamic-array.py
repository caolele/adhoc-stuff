#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'dynamicArray' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER n
#  2. 2D_INTEGER_ARRAY queries
#

def dynamicArray(n, queries):
    
    # Write your code here
    q = len(queries)
    last_answer = 0
    S = []
    for i in range(n):
        S.append([])
    
    # iterate each query
    result = []
    for query in queries:
        query_type = query[0]
        _seq = (query[1] ^ last_answer) % n
        if query_type == 1:
            S[_seq].append(query[2])
        elif query_type == 2:
            _seq_len = len(S[_seq])
            _ele = query[2] % _seq_len
            last_answer = S[_seq][_ele]
            result.append(last_answer)
    
    return result

if __name__ == '__main__':

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    q = int(first_multiple_input[1])

    queries = []

    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    result = dynamicArray(n, queries)

    print(*result, sep="\n")
