#!/bin/python3

import math
import os
import random
import re
import sys

def countInversions(arr):
    result = 0

    def merge(_arr, first, mid, last):
        nonlocal result
        left = _arr[first:mid]
        right = _arr[mid:last + 1]
        left.append(float('inf'))
        right.append(float('inf'))
        i = j = 0
        thres = mid - first
        for k in range(first, last + 1):
            if left[i] <= right[j]:
                _arr[k] = left[i]
                i += 1
            else:
                _arr[k] = right[j]
                j += 1
                if i < thres:
                    result += (thres - i)

    def merge_sort(_arr, first, last):
        if first < last:
            mid = (first + last) // 2
            merge_sort(_arr, first, mid)
            merge_sort(_arr, mid + 1, last)
            merge(_arr, first, mid + 1, last)

    merge_sort(arr, 0, len(arr) - 1)
    
    return result

if __name__ == '__main__':

    t = int(input())

    for t_itr in range(t):
        n = int(input())

        arr = list(map(int, input().rstrip().split()))

        result = countInversions(arr)

        print(result)

