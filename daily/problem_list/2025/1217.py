"""
https://codeforces.com/problemset/problem/1850/H

输入 T(≤100) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) m(1≤m≤n)。一维坐标轴上有 n 个点，第 i 个点的位置记作 x[i]。
然后输入 m 条信息，每条输入 a b(1≤a,b≤n, a≠b) d(-1e9≤d≤1e9)，表示 x[a]-x[b]=d。

这 m 条信息是否无矛盾？
如果无矛盾，输出 YES，否则输出 NO。

"""
import sys
from functools import cache
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


def solve_1850h(n, m, a):
    # a: [(i,j,d) ... xi - xj = d
    # 给定数组和其数值差，问有无矛盾 (只有差 初始值自由度可设0)
    # 并查集
    # 合并两个自洽连通块 不会有冲突 调整代表员即可
    # 冲突发生在一个块内 一个连边推导出和代表元差值不同
    # x,y,d - e
    # e-x != e-y + d

    pa = list(range(n))
    g = [0]*n # gap between x & pa[x].  val[root] - val[x]

    def find(x):
        if pa[x] == x:
            return x

        old_pa = pa[x]
        pa[x] = find(pa[x])

        g[x] += g[old_pa] # x - old_pa - root

        # 更新前
        # g[x]   = val[old] - val[x]
        # g[old] = val[root] - val[old]

        # 更新后should be
        # val[root] - val[x]  --- g[x] + g[old]
        return pa[x]


    for i,j,d in a:
        i,j = i-1, j-1

        x, y = find(i), find(j)
        if x != y:
            pa[y] = x
            g[y] = g[i]-g[j] + d
            # x-i y-j

            # g[i] = val[x]-val[i]
            # g[j] = val[y]-val[j]

            # val[i] - val[j] = d

            # =>
            # g[y] = val[x] - val[y] = gi-gj + vi-vj

        else:
            # vi - vj = d?
            # gi - gj = ve - vi - (ve - vj) = vj - ve = -d
            if g[i] - g[j] != -d:
                return "NO"
    return "YES"



for _ in range(RI()):
    n, m = RII()
    a = [tuple(RII()) for _ in range(m)]
    print(solve_1850h(n, m, a))
