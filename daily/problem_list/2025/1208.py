"""
https://codeforces.com/problemset/problem/2169/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 a(0≤a[i]≤2n)。

你可以执行如下操作至多一次：
选择 a（下标从 1 开始）的一个连续子数组 [L,R]，把子数组内的数都变成 L+R。

输出 sum(a) 的最大值。

"""
import itertools
from heapq import heappush, heappop
import sys
from math import inf
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, a = RI(), RILIST()

    # 前缀和 式子变形 枚举右维护左
    # [L,R]
    #-> L+R
    # sum

    # j],  i]
    # [j+1,i] --

    # (i-j) * (i+j+1) - (ps[i]-ps[j])
    # i*(i+1) - ps[i] - (j*(j+1) - ps[j])

    ps = list(itertools.accumulate(a, initial=0))

    res = 0
    mj = 0
    for i in range(n):
        t = (i+2)*(i+1) - ps[i+1]
        # L,R - 1 based
        if t - mj > res:
            res = t - mj
        mj = mn(mj, t)
    print(res + sum(a))
