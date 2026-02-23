"""
https://codeforces.com/problemset/problem/212/E

输入 n(3≤n≤5000) 和一棵 n 个节点的无向树的 n-1 条边。节点编号从 1 开始。

一开始每个节点都是白色。
你需要把某些（不是全部）节点染色红色或者蓝色。
要求：
1. 至少有一个点是红色，至少有一个点是蓝色。
2. 红色节点不能和蓝色节点相邻。

设 (a,b) = (红色节点数,蓝色节点数)。
你需要最大化 a+b。

输出有多少种不同的 (a,b)，记作 k。
然后输出这 k 种 (a,b)，按照 a 升序。

"""

import sys
from math import inf
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
# sys.setrecursionlimit(50000)

n = RI()
g = [[] for _ in range(n)]
for _ in range(n-1):
    a,b = RII()
    g[a-1].append(b-1)
    g[b-1].append(a-1)

f = [0]*n

target = n-1

reds = [False]*n
def dfs(i,p):
    cnt = 0
    f = 1
    for j in g[i]:
        if j == p: continue
        sub_cnt = dfs(j, i)
        cnt += sub_cnt
        f |= f << sub_cnt
    f |= f << (n - 1 - cnt)
    for i in range(1, n-1): # 1 <= i < n-1
        if f >> i & 1 == 1:
            reds[i] = True
    return cnt+1
dfs(0, -1)
reds = [r for r in range(n) if reds[r]]
# print(reds)
print(len(reds))
for x in reds:
    print(" ".join((str(x), str(n-1-x))))




