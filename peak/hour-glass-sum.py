#!/bin/python3

import math
import os
import random
import re
import sys
# import numpy as np
# from scipy import signal

def my_conv(a, b, x, y):
    result = 0
    dim = len(b)
    for i in range(dim):
        for j in range(dim):
            result += a[i+x][j+y] * b[i][j]
    return result

# Complete the hourglassSum function below.
def hourglassSum(arr):
    # np_arr = np.array(arr)
    # conv_patch = np.array([[1,1,1],[0,1,0],[1,1,1]])
    # conv_res = signal.convolve2d(np_arr, conv_patch, mode="valid")
    # return conv_res.max()

    conv_patch = [[1,1,1],[0,1,0],[1,1,1]]

    # anchor the top left corner
    dim = len(arr) - 2
    result = 0
    for i in range(dim):
        for j in range(dim):
            curr = my_conv(arr, conv_patch, i, j)
            if i == 0 and j == 0:
                result = curr
            elif result < curr:
                result = curr
    return result


if __name__ == '__main__':

    arr = []

    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))

    result = hourglassSum(arr)

    print(result)
