import sys
from math import inf
from typing import List
from collections import defaultdict, deque


"""
0210
https://atcoder.jp/contests/abc218/tasks/abc218_f

输入 n(2≤n≤400) m(1≤m≤n*(n-1))，表示一个 n 点 m 边的有向图。保证图中无自环和重边。
然后输入 m 条边，每条边输入 x y，表示一条 x 到 y 的有向边，边权为 1。节点编号从 1 开始。

输出 m 个数，其中第 i 个数表示删除输入的第 i 条边后，从 1 到 n 的最短路长度。如果无法从 1 到达 n，输出 -1。

- 移除边后，影响最短路吗？
- 先随便bfs计算一个最短路实例 - O(n+m) 一般由m主导
- 如果该边不在最短路上，则不影响；如果这边确在最短路上，可以移除后再求一次 bfs 最短路, 最短路最长为n-1 所以至多 n*m 次重新计算 
"""
def solve(n, s,t, edges):
    g = [[] for _ in range(n)]

    for a,b in edges:
        g[a].append(b)
        g[b].append(a)

    # bfs最短路 找一个实例
    def bfs(dele, need_instance):
        q = deque([s])
        dist = [inf]*n
        dist[s] = 0
        while q:
            x = q.popleft()
            for y in g[x]:
                if dist[x] + 1 < dist[y]:
                    dist[y] = dist[x] + 1
                    q.append(y)
        if need_instance:
            path = set([t]) # 只记录点即可
            y = t
            while y != s:
                for x in g[y]:
                    if dist[x] == dist[y] - 1:
                        path.add(x)
                        y = x
            return dist[t], path
        return dist[t], None

    d0, instance = bfs(-1, True)


    subtree_size = [0]*n
    def dfs(i, p):
        subtree_size[i] = 1
        for j in g[i]:
            if j == p: continue
            dfs(j, i)
            subtree_size[i] += subtree_size[j]
    dfs(0, -1)

    res = [0]*n
    size = [[n] for _ in range(n)]
    def dfs(i, p):
        # 考虑不含颜色c的连通块尺寸
        # 当前color[i] = c 往下看当前不包含c的连通块应该是 子树size - 子树中以c为颜色的root
        c = colors[i]
        for j in g[i]:
            if j == p: continue
            size[c].append(subtree_size[j])
            dfs(j, i)
            component = size[c].pop() # 当前不含c的连通块，所有路径 c(m,2) + m = m * (m-1) // 2 + m
            res[c] += component * (component + 1) // 2

        size[c][-1] -= subtree_size[i]
        # print(i,p, c, subtree_size[i], "--", size, res, res[c])
    dfs(0, -1)
    total = n * (n + 1) // 2

    for i in range(n):
        component = size[i][0]
        res[i] += component * (component + 1) // 2

    return [total - x for x in res]




Test = False
if Test:
    ########################## 本地调试部分 读取同目录下的 input.txt 数据
    # 输入部分
    with open("../input.txt", "r") as file:
        sys.stdin = file
        input = sys.stdin.read
        data = input().splitlines()

        ###############################################
        n = int(data[0])
        colors = list(map(lambda x: int(x)-1, data[1].split())) # 也转换为0-base
        edges = []
        for i in range(n - 1):
            a, b = map(int, data[2 + i].split())
            edges.append((a - 1, b - 1))

        result = solve(n, colors, edges)
        for x in result:
            sys.stdout.write(str(x) + "\n")
        ###############################################

        sys.exit()

sys.setrecursionlimit(10**7)
input = sys.stdin.read
data = input().splitlines()

###############################################
n = int(data[0])
colors = list(map(lambda x: int(x) - 1, data[1].split()))  # 也转换为0-base
edges = []
for i in range(n - 1):
    a, b = map(int, data[2 + i].split())
    edges.append((a - 1, b - 1))

result = solve(n, colors, edges)
for x in result:
    sys.stdout.write(str(x) + "\n")
###############################################
