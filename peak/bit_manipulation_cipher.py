#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the cipher function below.
def cipher(n, k, s):
    
    s = list(map(int, s))
    cols = n + k - 1
    pad = cols - len(s)
    
    # create a matrix (kinda sparse) represented by a list of list
    cache = ''

    # iterate from the first encoded string
    running_sum = [0 for _ in range(n)]
    for i in range(n - pad):
        # put one or zero
        to_put = running_sum[i] ^ s[i]
        cache += str(to_put)
        # update running_sum
        for j in range(1, k):
            if i+j < n: # avoid overflow
                running_sum[i+j] ^= to_put
    
    # now take the first row of length n
    return cache

def cipher_fast(n, k, s):
    a = list(map(int, s))
    l = []

    accum = 0
    for i in range(n):
        l.append(accum ^ a[i])
        accum ^= l[-1]
        if i >= k-1:
            accum ^= l[i-k+1]
    
    return ''.join([str(l[i]) for i in range(0, len(a)+1-k)])
    



if __name__ == '__main__':

    nk = input().split()

    n = int(nk[0])

    k = int(nk[1])

    s = input()

    result = cipher(n, k, s)

    print(result)
