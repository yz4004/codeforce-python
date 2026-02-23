"""
https://codeforces.com/problemset/problem/2069/B

输入 T(≤1e4) 表示 T 组数据。所有数据的 n*m 之和 ≤5e5。
每组数据输入 n m(1≤n≤m≤700) 和 n 行 m 列的网格图，元素范围 [1,n*m]。
单元格的值表示其颜色。

每次操作，选择一些颜色相同的，但两两不相邻的单元格，把所选单元格都涂成其他颜色。
注：相邻指共用一条边。

要使所有格子的颜色都相同，至少要操作多少次？

观察到任意颜色分布至多只需要操作两次 -- 一坨整块也是2次 二分图
所以操作不是1次就是两次，求和再减去最大的一个操作
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, m = RII()
    mat = [RILIST() for _ in range(n)]

    colors = [0]*(n*m+1)
    for i in range(n):
        for j in range(m):
            c = mat[i][j]
            if colors[c] == 2: continue

            if colors[c] == 0:
                colors[c] = 1

            for (p,q) in ((i-1,j), (i,j-1), (i,j+1),(i+1,j)):
                if 0 <= p < n and 0 <= q < m and mat[p][q] == c:
                    colors[c] = 2
                    break
    remove = max(colors) # 1/2
    operations = sum(colors) - remove

    print(operations)
