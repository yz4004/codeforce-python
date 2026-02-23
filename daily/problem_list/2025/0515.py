"""
https://codeforces.com/problemset/problem/645/D

输入 n(2≤n≤1e5) m(1≤m≤1e5)，表示一个 n 点 m 边的有向无环图（DAG）。保证图中无自环和重边。
然后输入 m 条边，每条边输入 x y，表示一条 x 到 y 的有向边。节点编号从 1 开始。

输出最小的 k，满足：
只考虑输入的前 k 条边，所形成的图的拓扑序是唯一的。

如果不存在这样的 k，输出 -1。

你能做到 O(n) 吗？

1. 二分+check唯一拓扑序 （任何时候队列元素都为1） -- nlogn
2. Hamilton路径的性质 利用唯一拓扑序           -- n
- 因为有唯一拓扑序 只关心哈密顿路径的主干
"""
import sys, random
from collections import defaultdict, deque

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, m = RII()
g = [[] for _ in range(n)]
edges = {}
ind = [0]*n
for i in range(m):
    a,b = RII()
    a,b = a-1,b-1
    edges[(a,b)] = i+1
    g[a].append(b)
    ind[b] += 1

def solve():
    q = deque([i for i in range(n) if ind[i] == 0])
    res = 1
    while q:
        if len(q) > 1:
            return -1

        x = q.popleft()
        for y in g[x]:
            # x-y 是否决定了 xy 的序，才需要考虑必须纳入前k个 (但是拓扑定序 是在入队时候发生）
            ind[y] -= 1
            if ind[y] == 0:
                # x-y 定唯一拓扑序
                res = mx(res, edges[(x,y)])
                q.append(y)
    return res
print(solve())






