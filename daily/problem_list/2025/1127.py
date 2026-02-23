"""
https://codeforces.com/problemset/problem/1073/E

输入 L R(1≤L≤R<1e18) 和 k(1≤k≤10)。

如果一个整数至多包含 k 种数字，那么称其为好整数。
例如 112 包含两种数字 1 和 2。

输出 [L,R] 中的好整数之和。
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
MOD = 998244353


def check(R,k):
    s = [int(c) for c in str(R)]
    m = len(s)

    tens = [1]*(m+1)
    for i in range(1,m+1):
        tens[i] = tens[i-1]*10

    @cache
    def f(i, is_num, is_limit, mask):
        if i == m:
            return [1,0] if mask.bit_count() <= k else [0,0] # 注意是至多k个

        res = [0,0]
        if not is_num:
            res = f(i+1, False, False, 0)

        lo = 1 if not is_num else 0
        hi = 9 if not is_limit else s[i]

        for j in range(lo, hi+1):
            cnt, sm = f(i+1, True, is_limit and j == hi, mask | (1<<j))
            res[0] += cnt
            res[1] = (res[1] + sm + cnt * j * tens[m-1-i]) % MOD
        return res

    cnt, sm = f(0, False, True, 0)
    return sm

L, R, k = RII()
print((check(R,k) - check(L-1,k))%MOD)

