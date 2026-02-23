"""
https://atcoder.jp/contests/abc286/tasks/abc286_e

输入 n(2≤n≤300) 和长为 n 的数组 a(1≤a[i]≤1e9)，表示一个 n 个点的图，每个点的点权为 a[i]。
然后输入一个 n*n 的 YN 矩阵 g，其中 g[i][j]=Y 表示有一条从 i 到 j 的有向边，边权为 1；g[i][j]=N 表示没有 i 到 j 的有向边。保证 g[i][i]=N。
然后输入 q(1≤q≤n*(n-1)) 和 q 个询问，每个询问输入两个数 x 和 y，保证 x≠y，范围在 [1,n]。

对于每个询问，输出两个数：
1. 从 x 到 y 的最短路长度 d。
2. 在所有从 x 到 y 的长为 d 的路径中，路径点权之和的最大值。
如果无法从 x 到 y，改为输出 Impossible。

- 支持n^3 floyd
- 两种维度 - 点权、边权
"""

import sys
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n = RI()
a = RILIST()
g = [RS() for _ in range(n)]

# floyd (但是点权非边权）
f = [[[inf]*2 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        if g[i][j] == "Y":
            f[i][j][0] = 1
            f[i][j][1] = a[i] + a[j]

for k in range(n): # 过前k个点，i-j最短路
    for i in range(n):
        for j in range(n):
            d1 = f[i][k][0] + f[k][j][0]
            d2 = f[i][k][1] + f[k][j][1] - a[k]
            if d1 < f[i][j][0]:
                f[i][j][0] = d1
                f[i][j][1] = d2
            elif d1 == f[i][j][0] and d2 > f[i][j][1]:
                f[i][j][1] = d2


for _ in range(RI()):
    i, j = RII()
    i, j = i-1, j-1
    if f[i][j][0] < inf:
        print(str(f[i][j][0]) + " " + str(f[i][j][1]))
    else:
        print("Impossible")






