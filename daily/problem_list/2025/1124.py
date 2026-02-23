"""
https://codeforces.com/problemset/problem/1921/D

输入 T(≤100) 表示 T 组数据。所有数据的 m 之和 ≤2e5。
每组数据输入 n m(1≤n≤m≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)，长为 m 的数组 b(1≤b[i]≤1e9)。

从 b 中选出 n 个数（子序列），你可以对其重新排列，得到数组 c。
输出 sum(|a[i]-c[i]|) 的最大值。
"""
import itertools
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


def solve(a,b):
    a.sort()
    b.sort()
    n, m = len(a), len(b)


    #     a1...an
    # b1...bm

    # a1-b1 + a2-b2
    # vs
    # a1-b2 + a2-b1

    # a1...an
    #     b1...bm
    res = 0

    ps_b = list(itertools.accumulate(b, initial=0))
    sa = sum(a)
    pre_a = 0
    for i,x in enumerate(a):
        # [:i]

        cnt_l = i
        cnt_r = n-i

        right_b = ps_b[m] - ps_b[m-i]
        left_b = ps_b[cnt_r]


        t = right_b - pre_a + (sa - pre_a - left_b)
        if t > res:
            res = t
        pre_a += x

    # a
    #   b
    t = ps_b[m] - ps_b[m-n] - sa
    if t > res:
        res = t

    #   a
    # b

    return res




for _ in range(RI()):
    n,m = RII()
    a = RILIST()
    b = RILIST()
    print(solve(a,b))
