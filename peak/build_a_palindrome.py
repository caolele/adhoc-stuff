#!/bin/python3

import os
import sys

#
# Complete the buildPalindrome function below.
#
def buildPalindrome(a, b):
    
    alen = len(a)
    blen = len(b)
    
    def longest_palindrome_from_start(s):
        res = s[0]
        idx = len(s) - 1
        while idx > 0:
            if s[0] == s[idx]:
                offset = 1
                while offset <= idx - offset:
                    right = s[offset]
                    left = s[idx - offset]
                    if right != left:
                        break
                    offset += 1
                if offset > idx - offset:
                    res = s[:idx+1]
                    break
            idx -= 1
        return res       
    
    def beam_search(a_start, b_start):
        a_sub = a[a_start]
        b_sub = b[b_start]
        offset = 1
        while True:
            i = a_start + offset
            j = b_start - offset
            if i < alen and j >= 0:
                if a[i] == b[j]:
                    a_sub += a[i]
                    b_sub = b[j] + b_sub
                    offset += 1
                    continue
                else:
                    pd_a = longest_palindrome_from_start(b[j::-1])
                    pd_b = longest_palindrome_from_start(a[i:])
                    if len(pd_a) > len(pd_b):
                        a_sub += pd_a
                    elif len(pd_b) > len(pd_a):
                        b_sub = pd_b + b_sub
                    else:
                        if pd_a < pd_b:
                            a_sub += pd_a
                        else:
                            b_sub = pd_b + b_sub
                    break
            elif j >= 0:
                b_sub = longest_palindrome_from_start(b[j::-1]) + b_sub
                break
            elif i < alen:
                a_sub += longest_palindrome_from_start(a[i:])
                break
            else:
                break
        return a_sub + b_sub
    
    
    result = []
    max_len = 0
    for i in range(alen):
        a_i = a[i]
        for j in range(blen):
            b_j = b[j]
            if a_i == b_j:
                hit = beam_search(i, j)
                if len(hit) > max_len:
                    result = [hit]
                    max_len = len(hit)
                elif len(hit) == max_len:
                    result.append(hit)
    result_sorted = sorted(result)
    print(result_sorted)
    return result_sorted[0] if len(result_sorted) > 0 else '-1'
                
        

if __name__ == '__main__':

    t = int(input())

    for t_itr in range(t):
        a = input()

        b = input()

        result = buildPalindrome(a, b)

        print(result)
