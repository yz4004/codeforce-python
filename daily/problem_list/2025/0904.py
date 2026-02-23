"""
https://codeforces.com/problemset/problem/628/E

输入 n m(1≤n,m≤3000) 和一个 n 行 m 列的网格图，只包含 '.' 和 'z'。

定义「Z 图案」为网格图中的子正方形，它的第一行、最后一行和反对角线都是 'z'。
注意：对于 Z 图案的其余单元格，没有限制，可以是 '.' 或者 'z'。
特别地，Z 图案的大小可以是 1，即只有一个 'z'。

输出这个网格图有多少个 Z 图案。

k  k-1          1
i-k i-(k-1) ... i-1 i

i, k
- f[i-k] >= k
- f[i-k+1] >= k-1
...
- f[i-1] >= 1

x in [i-k,i-1] f[x] >= i-x

f[x] + x >= i

a = [f[x1] ... f[xn]]
b = [f[xi] + xi ...]


"""
import sys
from bisect import bisect_left
from collections import defaultdict, deque
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, m = map(int, sys.stdin.readline().split())
g = [RS().strip() for _ in range(n)]

# 预处理水平连续 z
L = [[0]*m for _ in range(n)]
R = [[0]*m for _ in range(n)]
for i in range(n):
    run = 0
    for j in range(m):
        run = run + 1 if g[i][j] == 'z' else 0
        L[i][j] = run
    run = 0
    for j in range(m-1, -1, -1):
        run = run + 1 if g[i][j] == 'z' else 0
        R[i][j] = run



class BIT:
    def __init__(self, n):
        self.a = [0]*(n+1)
    def add(self, i, v):
        i += 1
        while i < len(self.a):
            self.a[i] += v
            i += i & -i
    def sum(self, i):  # sum of [0..i]
        i += 1
        s = 0
        while i > 0:
            s += self.a[i]
            i -= i & -i
        return s
    def range_sum(self, l, r):  # [l..r]
        if l > r: return 0
        return self.sum(r) - (self.sum(l-1) if l > 0 else 0)


ans = 0
# 枚举所有反对角线 r + c = s，从“右上到左下”（r++，c--）方向走
# 沿反对角线 枚举到i，右侧 r[i] 最大z只能看反对角线前面长为 [i-r[i]+1, i] 的区域
# [i-r[i]+1, i]
# 这里每个j的左侧是 l[j] 希望l[j] >= i-j 统计这样j的数量
# l[j]+j >= i for j in [i-r[i]+1, i]


for s in range(n + m - 1):
    r = 0 if s < m else s - (m - 1)
    c = s - r
    zs_L, zs_R = [], []

    while r < n and c >= 0:
        if g[r][c] == 'z':
            zs_L.append(L[r][c])
            zs_R.append(R[r][c])
        else:
            # 处理一个全 'z' 块
            if zs_L:
                length = len(zs_L)
                buckets = [[] for _ in range(length + 1)]
                for j in range(length):
                    T = zs_L[j] + j
                    if T > length: T = length
                    buckets[T].append(j)
                bit = BIT(length)
                # 阈值从 length 到 1
                for T in range(length, 0, -1):
                    for j in buckets[T]:
                        bit.add(j, 1)
                    i = T - 1
                    Lbound = i - zs_R[i] + 1
                    if Lbound < 0: Lbound = 0
                    ans += bit.range_sum(Lbound, i)
                zs_L.clear(); zs_R.clear()
        r += 1; c -= 1

    # 收尾：末尾块
    if zs_L:
        length = len(zs_L)
        buckets = [[] for _ in range(length + 1)]
        for j in range(length):
            T = zs_L[j] + j
            if T > length: T = length
            buckets[T].append(j)
        bit = BIT(length)
        for T in range(length, 0, -1):
            for j in buckets[T]:
                bit.add(j, 1)
            i = T - 1
            Lbound = i - zs_R[i] + 1
            if Lbound < 0: Lbound = 0
            ans += bit.range_sum(Lbound, i)
            
print(ans)       
