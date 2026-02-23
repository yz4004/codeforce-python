"""
https://codeforces.com/problemset/problem/1954/D

输入 n(1≤n≤5000) 和长为 n 的数组 a(1≤a[i]≤5000)，保证 sum(a)≤5000。
a[i] 表示颜色为 i 的小球的个数。

定义 f(b) 表示一共有 sum(b) 个小球，每次操作可以移除一个球，或者两个颜色不同的球，问：至少要操作多少次才能把所有球移除完。
例如 f([3,1,7]) = 7。

a 有 2^n 个子序列 b，每个独立计算 f(b)。
输出这 2^n 个 f(b) 之和，模 998244353。
"""
import itertools
import sys
from functools import cache
from math import inf
from operator import add, xor
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 998244353

def solve(n, a):
    # 挡板贪心 - 两两移除不同值 + 背包 + 贡献法

    # 对每个a的子序列b 考虑 f(b)
    # f(b) 给定球计数序列 b 每次移除两个不同值的球 至少操作次数
    # 根据两两移除不同值的挡板贪心 对单个子序列b 由b的max和b的和决定
    # - max(max(b), (sum(b)+1)//2)

    # 提示 sum(a) < 5000 - 按子序列和背包

    # 对a排序后每次引入的x就是max 由x参与的子序列和 以及x可以决定该子序列贡献

    a.sort()
    u = sum(a)
    f = [0]*(u+1)
    f[0] = 1
    res = 0
    for x in a:
        for i in range(u, x-1, -1):
            f[i] += f[i-x]
            res += max_((i + 1) // 2, x) * f[i-x]  # 引入x后 sum=i 的子序列新增数量 f[i-x] 以及对应的最少移除次数 max_((i + 1) // 2, x)

            f[i] %= MOD
            res %= MOD

        # 分开计算会重复计入之前x没参与的那些子数组
        # for i in range(x, u+1):
        #     res += max_((i+1)//2, x) * f[i]
    return res

n, a = RI(), RILIST()
print(solve(n, a))



