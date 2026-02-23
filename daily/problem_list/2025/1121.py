"""
https://codeforces.com/problemset/problem/1245/F

输入 T(≤100) 表示 T 组数据。
每组数据输入 L R(0≤L≤R≤1e9)。

输出有多少对整数 (a,b) 满足如下条件：
L ≤ a ≤ R
L ≤ b ≤ R
a + b = a XOR b

"""

import itertools
import sys
from bisect import bisect_left
from collections import defaultdict
from functools import cache
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(L,R):
    # a+b = a xor b
    if L > R: L, R = R, L

    def check(L, R):
        if L < 0 or R < 0:
            return 0

        if L > R: L, R = R,L
        sa, sb = [int(c) for c in str(bin(L)[2:])], [int(c) for c in str(bin(R)[2:])]
        m = len(sb)

        sa = (m - len(sa)) * [0] + sa


        @cache
        def f(i, is_limit_a, is_limit_b):
            if i == m:
                return 1

            res = 0
            hi_a = 1 if not is_limit_a else sa[i]
            hi_b = 1 if not is_limit_b else sb[i]

            # 如果要引入 is_num 必须改 lo 的逻辑

            for ca in range(0, hi_a+1):
                for cb in range(0, hi_b + 1):
                    if ca + cb == ca ^ cb:
                        res += f(i+1, is_limit_a and ca==sa[i], is_limit_b and cb==sb[i])
            return res
        return f(0,True, True)

    # [L,R]
    return check(R,R) - check(L-1,R) * 2 + check(L-1,L-1)


for _ in range(RI()):
    L, R = RII()
    print(solve(L,R))

