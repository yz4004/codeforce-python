"""
https://codeforces.com/problemset/problem/2071/B

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤1e6。
每组数据输入 n(1≤n≤5e5)。

构造一个 1~n 的排列 p，满足 p 的前缀和不含完全平方数。
具体地，若 p 的下标从 1 开始，那么 p[1], p[1]+p[2], p[1]+p[2]+p[3], ..., sum(p) 都不是完全平方数。

如果无解，输出 -1。
否则输出任意满足要求的 p。

"""
import sys, itertools
from functools import cache
from heapq import heappop, heapify, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(n):
    # 构造1-n排列 前缀和不含完全平方数
    # 1 4 9 16 25 36 49...

    # 3 5 7 9 11 13

    # n^2, (n+1)^2 -- gap = 2n + 1

    # 整体是平方和 则没办法摆脱

    # 按1234顺序排 如果发现完全平方 交换 x,x+1 则肯定能规避 sum(1-x)=t^2 因为加了1后必然不是完全平方 至少差3

    # 1...x x+1

    # 1... x+1 x

    # 如果交换后到x 也是完全平方?

    # sum(1..x) = (1+x)*x//2 = n^2
    # 根据连续完全平方的规律 下一个至少是 (n+1)^2 = n^2 + 2n+1
    # 即 x+1 至少是 2n+1 （2nk+k^2 更大了)
    # x=2n 带回 （1+x)*x//2 = (1+2n)*n >> n^2 不对
    # 所以 1--x+1必然不是平方数

    # https://chatgpt.com/c/6992e9e4-ace0-832a-ae15-a0e510cc1ccd

    s = (n+1) * n // 2
    if s == isqrt(s) ** 2:
        return "-1"

    res = [0]*n
    s = 0
    for i in range(1, n+1):
        s += i
        if res[i-1]: continue # 填过了

        if s == isqrt(s) ** 2:
            res[i-1], res[i] = i+1, i
        else:
            res[i-1] = i
    return " ".join(map(str, res))


for _ in range(RI()):
    print(solve(RI()))