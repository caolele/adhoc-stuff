#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the checkMagazine function below.
def checkMagazine(magazine, note):
    # build dict for magzine
    magazine_dict = {}
    for entry in magazine:
        if entry in magazine_dict:
            magazine_dict[entry] += 1
        else:
            magazine_dict[entry] = 1
    
    # check towards dict
    result = "Yes"
    for entry in note:
        if entry in magazine_dict:
            if magazine_dict[entry] > 0:
                magazine_dict[entry] -= 1
            else:
                result = "No"
                break
        else:
            result = "No"
            break
    
    print(result)


if __name__ == '__main__':
    mn = input().split()

    m = int(mn[0])

    n = int(mn[1])

    magazine = input().rstrip().split()

    note = input().rstrip().split()

    checkMagazine(magazine, note)
