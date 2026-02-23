"""
https://codeforces.com/problemset/problem/1141/C

输入 n(2≤n≤2e5) 和长为 n-1 的数组 d(-n<d[i]<n)。

这个长为 n-1 的 d 数组，是某个 1~n 的排列 p 的差分数组。

输出 p 数组。
如果不存在 p，输出 -1。

假设开头是x 则可以根据差分还原数组，根据数组和可求x
x, x+d[:1], x+d[:2], x+d[:3]... x+d[:n] = [1..n]
- x*n + sum(list(itertools.accumulate(a))) = (1+n)*n//2

不合法情况，x非整数，后续构建超出范围/重复 => 不能恰好构成1-n排列
"""

import sys, itertools
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n = RI()
a = RILIST()
def solve(n, a):
    t = (n+1) * n // 2 - sum(list(itertools.accumulate(a)))
    if t % n or not (1 <= t//n <= n):
        print("-1")
        return

    x = t // n
    res = [0]*n
    res[0] = x
    vis = [False]*n
    vis[x-1] = True
    for i,d in enumerate(a, 1):
        res[i] = res[i-1] + d
        cur = res[i]
        if not (1 <= cur <= n) or vis[cur-1]:
            print("-1")
            return
        vis[cur - 1] = True
    print(" ".join(map(str, res)))
solve(n, a)





