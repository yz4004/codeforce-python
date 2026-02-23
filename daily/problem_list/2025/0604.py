"""
https://codeforces.com/problemset/problem/2000/F

输入 T(≤100) 表示 T 组数据。所有数据的 n 之和 ≤1e3。
每组数据输入 n(1≤n≤1e3) k(1≤k≤100) 和长为 n 个矩形的长和宽，范围 [1,100]。

每个大小为 a×b 的矩形，有 a×b 个单元格。
每次操作，你可以选择一个矩形的一个单元格，将其涂色。
如果一个矩形的一行被涂满颜色，你获得一分。
如果一个矩形的一列被涂满颜色，你获得一分。

至少获得 k 分，最少要执行多少次操作？
如果无法做到，输出 -1。

"""
from collections import defaultdict
from functools import cache
from math import comb, factorial, inf
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(n,k, mat):

    # 前i个矩阵提供k分
    # 某个矩阵提供的分数 1 2 ... a*b 的分别对应最小花费

    costs = []
    for x,y in mat: # 100 * n
        cost = []
        t = mn(x+y, k)
        for i in range(1, t+1):
            tmp = inf
            # i = r + i-r
            # (r,i-r)
            # r<x, i-r<y
            for r in range(mx(0,i-y), mn(i, x)+1):
                c = i-r
                tmp = mn(tmp, r*y + c*x - r*c)
            cost.append(tmp)
        costs.append(cost)

    # f[i] 凑够分数i的最小花费 （前i个矩阵）
    f = [inf]*(k+1)
    f[0] = 0

    for cost in costs:
        # g = [0] + [inf] * k
        g = f[:]

        for j,c in enumerate(cost, 1):
            # for i in range(j, k+1):
            # for i in range(k, j-1, -1):
            #     f[i] = mn(f[i-j] + c, f[i])

            for i in range(j, k + 1):
                g[i] = mn(f[i - j] + c, g[i])
        f = g
    return f[k] if f[k] < inf else -1

T = RI()
for _ in range(T):
    n,k = RII()
    mat = [RII() for _ in range(n)]
    print(solve(n, k, mat))
