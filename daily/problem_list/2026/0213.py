"""
https://codeforces.com/problemset/problem/1715/E

输入 n(2≤n≤1e5) m(1≤m≤1e5) 和 k(1≤k≤20)，表示一个 n 点 m 边的无向图。无自环，可能有重边。
然后输入 m 条边，每条边输入 x y w(1≤w≤1e9)，表示一条边权为 w 的无向边连接 x 和 y。节点编号从 1 到 n。

有 n 座城市，m 条道路连接这些城市。
此外，每对城市之间都有一条航班。从城市 x 到城市 y 的用时为 (x-y)²。

输出 n 个数。
第 i 个数表示在至多乘坐 k 次航班的约束下，从 1 到 i 的最短路长度。

整体凸壳 CHT +  多源 Dijkstra / 带初始势能的 Dijkstra

1. 整体凸壳 vs 动态凸壳
    当转移信息只来源于前缀 - 动态凸壳 边加点边查询
    这题依赖上一行所有状态 - 整体凸壳合适 （否则要前后缀各算一次）

2. 更新一次航班后 得重新跑一次最短路
    带初始势能的dijkstra 初始必须所有点入队

参考
https://chatgpt.com/c/698edde8-a3e4-832f-a58b-7ebc7e9fa999

"""
import sys, itertools
from functools import cache
from heapq import heappop, heapify, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

"""
没有飞机就是最短路，考虑第一次飞机 x-y - (x-y)^2

更新当前站点i的 只能是最短路更早的 j.  

g[i] = min(f[j] + (i-j)^2 for j in range(n) where f[j] < f[i])  


    不能可以按距离重排序 然后考虑左侧 - 虽然得到了数组的前缀部分 但打乱下标i 斜率不保证单调
    维护凸壳 + deque 斜率优化 斜率单调是 [必须的] 

gi = fj + j^2 - 2ij + i^2 

整体维护上一行的下凸壳 
    x=j 
    y=fj + j^2 
    a=2i

    fj + j*2 - 2ij 
    y - a*x = b - 最小截距b (递增?)正斜率a - 下凸包 向右延展 
    y = ax + b 
"""
def solve(n,m,k,graph):

    def dijkstra(dist):
        """
        多源 Dijkstra / 带初始势能的 Dijkstra （已经算得的dist[i] 0-i 的一个距离
        不能只传原点
        """
        # q = [(0,0)]
        q = [(dx,x) for x,dx in enumerate(dist)]
        heapify(q)
        while q:
            dx, x = heappop(q)
            if dx > dist[x]: continue
            for y, w in graph[x]:
                if dx + w < dist[y]:
                    dist[y] = dy = dx + w
                    heappush(q, (dy, y))
        return dist
    # f = sorted((dx,x) for x,dx in enumerate(dist))

    dist = [inf]*n
    dist[0] = 0
    f = dijkstra(dist)
    g = [inf]*n
    g[0] = 0

    def cross_product(v1, v2):
        # v1 x v2 向量叉乘
        # v1 旋转到 v2. <0顺时针 >0 逆时针   ( 01 -> 10 = 0*0-1*1 = -1 )
        x1, y1 = v1
        x2, y2 = v2
        return x1 * y2 - x2 * y1

    def cross(a, b, c): # (a,b) x (a,c)
        vab = b[0] - a[0], b[1] - a[1]
        vac = c[0] - a[0], c[1] - a[1]
        return cross_product(vab, vac)

    # gi = fj + j^2 - 2ij + i^2
    # 维护左侧 fj + j*2 - 2ij
    for _ in range(k):

        # 已经计算得了 k-1 次转机的最短路. 引入第k次转机
        # gi = fj + j^2 - 2ij + i^2
        # 维护min fj + j^2 - 2ij
        # y=fj+j^2, x=j, a=2i
        # y - ax = b
        # a=2i 递增 x=j 递增
        # y = ax + b - 找min b
        # 维护下凸壳
        # 因为j可以在i左右 先统一计算下凸壳. 然后对每个i (斜率a增大 最优解在下凸壳往右移动切线)

        q = deque()
        for j,dj in enumerate(f):
            xj, yj = j, dj + j*j

            while len(q) > 1 and cross(q[-2], q[-1], (xj, yj)) <= 0:
                q.pop()
            q.append((xj,yj))

        for i in range(1, n):
            ai = 2*i
            # 1. 先计算当前值. 弹出队列左侧. 当前f值计算结束后再更新凸壳
            get_b = lambda x,y,a: y - a*x
            while len(q) > 1 and get_b(q[0][0], q[0][1], ai) >= get_b(q[1][0], q[1][1], ai):
                q.popleft()

            if q:
                b = get_b(q[0][0], q[0][1], ai)
                b += i * i
                g[i] = min_(g[i], b)

        #### 增加一次航班 - 后面还要跑最短路 - 再已有dist上更新一次最短路
        g = dijkstra(g)
        f, g = g, f

        # 从左往右 再从右往左 其实是多余的
        # q = deque()
        # for i,di in enumerate(f):
        #     xi, yi = i, di + i*i
        #     ai = 2*i
        #
        #     # 1. 先计算当前值. 弹出队列左侧. 当前f值计算结束后再更新凸壳
        #     get_b = lambda x,y,a: y - a*x
        #     while len(q) > 1 and get_b(q[0][0], q[0][1], ai) >= get_b(q[1][0], q[1][1], ai):
        #         q.popleft()
        #
        #     if q:
        #         b = get_b(q[0][0], q[0][1], ai)
        #         b += i * i
        #         g[i] = min_(g[i], b)
        #
        #     # 2. (xi,yi) 更新凸壳
        #     while len(q) > 1 and cross(q[-2], q[-1], (xi, yi)) <= 0:
        #         q.pop()
        #     q.append((xi,yi))
    return f




n, m, k = RII()
g = [[] for _ in range(n)]
for _ in range(m):
    a, b, w = RII()
    a, b = a-1, b-1
    g[a].append((b,w))
    g[b].append((a,w))
print(" ".join(map(str, solve(n,m,k,g))))
