"""
https://codeforces.com/problemset/problem/1333/A

输入 T(≤20) 表示 T 组数据。
每组数据输入 n m(2≤n,m≤100)。

构造一个 n 行 m 列的网格图，只包含大写字母 B 和 W。
设 cntB 为网格图中与至少一个 W 相邻的 B 的数量。
设 cntW 为网格图中与至少一个 B 相邻的 W 的数量。
要求 cntB = cntW + 1。

注：相邻指共用一条边。

wb - 当一个相邻wb彼此计入1.
b  - 多一个b相邻到同一个w 才会多个1

为了保持这个结构 放在左上角 剩余就算全放b 他们不和w相邻都是0

wb ...
b ....

"""
import sys, itertools
from functools import cache, lru_cache
from heapq import heappop, heapify, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left, bisect_right
from collections import deque, defaultdict, Counter

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())

MOD = 10 ** 9 + 7


def solve(m, n):
    res = [None]*m
    res[0] = "W" + "B"*(n-1)
    res[1] = "B"*n
    for i in range(2, m):
        res[i] = "B"*n

    return res

for _ in range(RI()):
    m, n = RII()
    print("\n".join(solve(m, n)))