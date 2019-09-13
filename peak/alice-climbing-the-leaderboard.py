#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the climbingLeaderboard function below.
def climbingLeaderboard(scores, alice):
    # cache is an array, which contains triplets [a, b, c]
    # a is the actual score from either rank or alice
    # b is the counter indicating how many times it showed up in rank scores
    # c is the same as b except that it counts in alice scores
    n_score = len(scores)
    n_alice = len(alice)
    p_score = 0
    p_alice = n_alice - 1
    cache = []
    while p_score < n_score or p_alice >= 0:
        # health check for append tails
        if p_score < n_score:
            _score = scores[p_score]
        else:
            _score = -1
        if p_alice >= 0:
            _alice = alice[p_alice]
        else:
            _alice = -1
        # build cache
        if _score >= _alice:
            if len(cache) == 0 or cache[-1][0] != _score:
                cache.append([_score, 1, 0])
            else:
                cache[-1][1] += 1
            p_score += 1
        else:
            if len(cache) == 0 or cache[-1][0] != _alice:
                cache.append([_alice, 0, 1])
            else:
                cache[-1][2] += 1
            p_alice -= 1
    # Traverse the cache array to calculate the final 
    result = []
    running_minus = 0
    for i in range(len(cache)):
        entry = cache[i]
        _score, c1, c2 = entry[0], entry[1], entry[2]
        if c2 > 0:
            _dup_rank = (i + 1) - running_minus
            for _ in range(c2):
                result.insert(0, _dup_rank)
            if c1 == 0:
                running_minus += 1
    return result


if __name__ == '__main__':

    scores_count = int(input())

    scores = list(map(int, input().rstrip().split()))

    alice_count = int(input())

    alice = list(map(int, input().rstrip().split()))

    result = climbingLeaderboard(scores, alice)

    print('\n'.join(map(str, result)))
