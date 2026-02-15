from math import inf
from typing import List
from collections import deque
"""
1. bellman_ford 松弛dp 模板检测负环
2. spfa 队列/拓扑序 松弛模板 检测负环
3. 例题 lc787 有边数限制的最短路 （dijkstra也会导向这里）
"""

def bellman_ford(n, src, edges):
    # edges[ [0,1,100] ... ] n点m边
    INF = 0x3F3F3F3F
    dis = [INF] * (n + 1)
    dis[src] = 0
    for i in range(1, n + 1): # n个点 至多n轮松弛
        flag = False
        for u,v,w in edges:
            if dis[u] == INF: continue # 到u最短路长度为 INF 的点引出的边不可能发生松弛操作
            if dis[v] > dis[u] + w:
                dis[v] = dis[u] + w
                flag = True
        # 没有可以松弛的边时就停止算法
        if not flag:
            break
    # 第 n 轮循环仍然可以松弛时说明 s 点可以抵达一个负环
    return flag

"""
1. Bellman-Ford 核心是松弛dp
    n轮松弛，每轮松弛遍历所有m条边
    每轮循环尝试对图上所有点进行一次松弛，直到没有更新位置 O(mn)
2. 检测负环，因为最短路至多长为n-1，一次松弛会使最短路边长+1 如果发现第n轮松弛仍能发生边松弛，说明出现负环
3. 上轮被松弛到的点，下轮才有可能继续松弛到新的点，队列优化 SPFA (最坏仍然mn)
    参考 https://oi-wiki.org/graph/shortest-path/#bellmanford-%E7%AE%97%E6%B3%95
"""

def spfa_find_negative_circle(n, src, edges):
    INF = 0x3F3F3F3F

    g = [[] for _ in range(n)]
    for a,b,w in edges:
        g[a].append((b,w))
        g[b].append((a,w))

    dis = [INF] * (n + 1)
    cnt = [0] * (n + 1)
    vis = [False] * (n + 1)
    q = deque([src])
    dis[src] = 0
    vis[src] = True

    while q:
        u = q.popleft()
        vis[u] = False
        for v,w in g[u]:
            if dis[v] > dis[u] + w:
                dis[v] = dis[u] + w
                cnt[v] = cnt[u] + 1  # 记录最短路经过的边数
                if cnt[v] >= n:
                    return False
                # 在不经过负环的情况下，最短路至多经过 n - 1 条边
                # 因此如果经过了多于 n 条边，一定说明经过了负环
                if not vis[v]:
                    q.append(v)
                    vis[v] = True


"""
有边数限制的最短路
就算一开始想dijkstra最终也会通向这个版本
"""
def lc_787_findCheapestPrice(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    # 要求中间点数量不超过k 即最大边长为k+1
    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)] #反图 一种非松弛写法用到
    for a, b, w in flights:
        g[a].append((b, w))
        rg[b].append((a, w))

    # 1. bellman-ford 松弛dp 非空间优化 超内存限制
    # 虽然d+1只依赖d层，但因为拓扑序更新顺序不按层更新，并不方便改成滚动空间优化
    f = [[inf] * (n) for _ in range(k + 2)]  # f[i][j] 从src出发经过i站中转到达j
    f[0][src] = 0
    q = deque([(0, src)])
    while q:
        d, i = q.popleft()
        for j, w in g[i]:
            if d + 1 <= k + 1 and f[d][i] + w <= f[d + 1][j]:
                f[d + 1][j] = f[d][i] + w  # 易见d+1只依赖d层，所以可以定义d层在前
                q.append((d + 1, j))
    res = min(f[t][dst] for t in range(k + 2))

    # 2. 按层更新，虽然有上轮没有被松弛更新的点 本轮仍从他们出发进行了无用松弛 但按层做到空间优化 147ms通过本题
    f = [inf]*n # f[i][j] 从src出发经过i站中转到达j
    f[src] = 0
    for d in range(1, k+2):
        old_f = f[:]
        for j in range(n): #通过反图倒退谁能更新到j
            for i,w in rg[j]:
                f[j] = min(f[j], old_f[i] + w)
    res = f[dst]

    # 2.1 按层写法的刷表松弛正推
    f = [inf] * n  # f[i][j] 从src出发经过i站中转到达j
    f[src] = 0
    for d in range(0, k + 1):  # 通过刷表正推 松弛到谁
        old_f = f[:]
        for i in range(n):
            for j, w in g[i]:
                f[j] = min(f[j], old_f[i] + w)
    res = f[dst]

    # 3. spfa空间优化的混合写法 最快46ms - (最坏q内仍可能堆积n*m个状态，但是一般不卡）
    # 如果一开始想的是dijkstra+边数限制，其实就是这个版本，但是heap替代deque意义不大
    f = [[inf, 0] for _ in range(n)]  # f[i] 从src出发经过到达j 距离,中转
    f[src][0] = 0
    q = deque([(0, src, 0)]) #维持状态 使用边数，点，距离。不再通过dist里固定查询，而是拓扑序带着所有状态
    res = inf
    while q:
        d, i, dist = q.popleft()
        for j, w in g[i]:
            if d + 1 <= k + 1 and dist + w <= f[j][0]: #如果距离更小 就直接更新到f 无视耗边
                f[j] = [dist + w, d + 1]
                q.append((d + 1, j, dist + w)) #使用d的数据 覆盖边数
                if j == dst:
                    res = min(res, dist + w)

            elif d + 1 < f[j][1]: # 如果没有更新最短距，但是节约了边数，暂存到q 也是未来可期的状态
                q.append((d + 1, j, dist + w))
                # if j == dst: res = min(res, dist + w) 这里反而不需要 因为没有更新到最短边 只是节约边数假如到枚举状态里
    return res if res < inf else -1
