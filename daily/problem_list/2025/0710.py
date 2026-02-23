"""
https://codeforces.com/problemset/problem/2117/G

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5，m 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) m(n-1≤m≤2e5)，表示一个 n 点 m 边的无向图。保证图是连通的，无自环，无重边。
然后输入 m 条边，每条边输入 x y w(1≤w≤1e9)，表示一条边权为 w 的无向边连接 x 和 y。节点编号从 1 开始。

输出从 1 到 n 的路径中，「最小边权+最大边权」的最小值。
注意：路径不一定是简单路径，可以重复经过点和边。

"""
import sys
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, m = RII()

    # DAG
    # min(最小边权 + 最大边权 for path from 1-n)
    # 可以绕路，但总归要找1-n的通路，尝试dijkstra 路径距离定义为所有路径的最大边权，然后找最小路径的通路
    # 在通过1出发找附近的最小边权，在经过边不大于max边权的情况，找能够到的最小
    # 但这并不一定是最优

    # 提示：并查集
    # 结果肯定是 wi + wj for i,j 尝试从小到大合并边权，直到联通为止

    pa = list(range(n))
    block_min_edge = [inf]*n

    def find(x):
        # if pa[x] == x:
        #     return x
        # pa[x] = find(pa[x])
        # return pa[x]

        # 先顺着pa找到代表元
        rt = pa[x]
        while rt != pa[rt]:
            rt = pa[rt]

        # 路径压缩
        while x != rt:
            x, pa[x] = pa[x], rt
        return rt

    def merge(x,y):
        x,y = find(x), find(y)
        if x == y: return 0
        pa[x] = y
        return 1

    edges = []
    for _ in range(m):
        a,b,w = RII()
        edges.append((a-1,b-1,w))

    res = inf
    edges.sort(key=lambda e:e[2])
    for a,b,w in edges:
        a,b = find(a), find(b)
        if a == b: continue

        pa[a] = b
        block_min_edge[b] = min(block_min_edge[b], block_min_edge[a], w)

        if find(0) == find(n-1):
            # print(edges[0][-1] + w)
            # w一定是最大的，因为他是瓶颈条件，但是edges[0]不一定与他们联通 需要手动找一下最小边

            # 这也没完，也许后面的最大边稍大一点，确联通了更小的edge 让总复杂度变小
            res = mn(res, w + block_min_edge[find(0)])
    print(res)

