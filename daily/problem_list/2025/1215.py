"""
https://www.luogu.com.cn/problem/P3903

输入 n(1≤n≤1e3) 和长为 n 的数组 a(1≤a[i]≤1e9)。

从 a 中选一个震荡子序列 b，满足 b[0] > b[1] < b[2] > b[3] < ...
输出 b 的最大长度。

注：子序列不一定连续。

"""
import sys
from functools import cache
from math import inf
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve_p3903(n, a):

    # 1e3 - n^2
    # f[i][0/1] - ending with i, decrease/increase

    # 转移本质是在满足condition的集合里找max 提出两个bit即可 n*logn

    f0 = [0]*n # decrease to i
    f1 = [1]*n

    res = 1
    for i,x in enumerate(a):
        # 第一个应该是高到低 所以f0不能从1开始
        f0[i] = max((f1[j] for j in range(i) if a[j] > x), default=-inf) + 1
        f1[i] = mx(max((f0[j] for j in range(i) if a[j] < x), default=0) + 1, 1)

        # for j in range(i):
        #     if a[j] < x:
        #         f1[i] = mx(f0[j]+1, f1[i])
        #     elif a[j] > x:
        #         f0[i] = mx(f1[j]+1, f0[i])

        res = mx(res, mx(f0[i], f1[i]))
    return res

n, a = RI(), RILIST()
print(solve_p3903(n, a))

