"""
https://codeforces.com/problemset/problem/1554/B

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤3e5。
每组数据输入 n(2≤n≤1e5) k(1≤k≤min(n,100)) 和长为 n 的数组 a(0≤a[i]≤n)。

输出 i * j - k * (a[i] OR a[j]) 的最大值，其中 i < j。

进阶：做到与 k 无关的时间复杂度。

提示
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

def solve(n,k,a):
    m = n.bit_length()

    # i*j - k*(ai |aj)
    f = [None]*(1<<m)
    f[0] = (-1, -1)
    for i,x in enumerate(a):
        if not f[x]:
            f[x] = (i,-1)
        else:
            f[x] = (i, f[x][0])


    for i in range(0, m):
        for s in range(1<<m):
            if s >> i & 1 and f[s ^ (1<<i)]:
                if not f[s]:
                    f[s] = f[s ^ (1<<i)]
                else:
                    i1, j1 = f[s]
                    i2, j2 = f[s ^ (1<<i)]

                    tmp = sorted((i1, j1, i2, j2), reverse=True)
                    f[s] = (tmp[0], tmp[1])


    res = -inf
    for s in range(1<<m):
        if f[s] and f[s][1] != -1:
            i, j = f[s]
            t = (i+1) * (j+1) - k * s # (i | j)
            if t > res:
                res = t
    return res





for _ in range(RI()):
    n, k = RII()
    a = RILIST()
    print(solve(n,k, a))
