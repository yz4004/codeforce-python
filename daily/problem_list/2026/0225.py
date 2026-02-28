"""
https://codeforces.com/problemset/problem/2085/C

输入 T(≤1e4) 表示 T 组数据。
每组数据输入 x y (1≤x,y≤1e9)。

找到一个在 [0,1e18] 中的整数 k，使得如下等式成立
(x+k) + (y+k) = (x+k) XOR (y+k)

如果无解，输出 -1。
否则输出任意符合要求的 k。

"""

import sys, itertools
from functools import cache
from heapq import heappop, heappush
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

"""
位运算 xor 构造

将大的数最高位进一 其余都是0. 则会有 1000...0 形式 
对于较小的那个数 最高位不进位 低位随便怎么排 都不影响和0的xor

只有两数相等时不可以
"""

def solve(x, y):

    if x == y:
        return -1

    if x < y: x, y = y, x

    # x > y
    u = x.bit_length()

    # x加上一个k 使得最高位进位 变成 1<<u = 10000..0
    k = (1<<u) - x

    return k

    # u = max_(x,y).bit_length()
    # k = 0
    # for i in range(u):
    #     a = x >> i & 1
    #     b = y >> i & 1
    #
    #     if a == b == 1:
    #         mask = (1 << (i+1)) - 1
    #         lx = x & mask
    #         ly = y & mask
    #
    #         hx = x - lx
    #         hy = y - ly
    #
    #         if hx == hy:
    #             return -1
    #
    #         h = hx ^ hy
    #
    #         lb = h ^ -h
    #
    #         d = lb - lx
    #
    #         k += d
    #
    #         x += d
    #         y += d



for _ in range(RI()):
    x, y = RII()
    print(solve(x,y))