

"""
https://codeforces.com/problemset/problem/2125/C

输入 T(≤1e3) 表示 T 组数据。
每组数据输入 L R(1≤L≤R≤1e18)。

输出 [L,R] 中有多少个整数 x，满足 x 的所有质因子都至少是两位数。

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




def include_exclusion_prime_factor_template(n):
    # 1...n 中所有被下面质因子整除的数 容斥排除
    # 2,3,5,7
    vals = (2,3,5,7)

    # - (所有被至少一个素数整除的数) + (所有至少被两个素数整除的数) - ...

    res = n
    for s in range(1, 1<<4):
        sign = -1 if s.bit_count() % 2 == 1 else 1
        t = 1
        for i,v in enumerate(vals):
            if s >> i & 1:
                t *= v

        res += sign * (n // t) # 所有被t整除的数的个数
    return res

    # 移除拥有某些素因子的数
    # https://codeforces.com/problemset/problem/2125/C



