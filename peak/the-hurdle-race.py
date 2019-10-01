#!/bin/python3

import math
import os
import random
import re
import sys


def maxheap_insert(heap, v):
    heap.append(v)
    idx = len(heap) - 1
    while idx != 0:
        parent_idx = (idx - 1) // 2
        if heap[parent_idx] < heap[idx]:
            heap[parent_idx], heap[idx] = heap[idx], heap[parent_idx]
        else:
            return
        idx = parent_idx  

# Complete the hurdleRace function below.
def hurdleRace(k, height):
    # construct a max heap
    maxheap = []
    for h in height:
        maxheap_insert(maxheap, h)
    # calculate the final result
    max_height = maxheap[0]
    if k >= max_height:
        return 0
    else:
        return max_height - k
    

if __name__ == '__main__':

    nk = input().split()

    n = int(nk[0])

    k = int(nk[1])

    height = list(map(int, input().rstrip().split()))

    result = hurdleRace(k, height)

    print(result)
