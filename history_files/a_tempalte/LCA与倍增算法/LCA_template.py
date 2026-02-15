from typing import List

def LCA_template1(self, n: int, edges: List[List[int]]) -> List[int]:

    # 1. 初始化图，跳表深度为图的最大节点数取log 即bit_length
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 2. 深度表 st跳表 （有时还需跳表跳跃路径对应值）
    m = n.bit_length()
    depth = [0]*n
    st = [[-1]*m for _ in range(n)]

    # 2.1 dfs初始化 深度/parent
    def dfs(i, p, d):
        depth[i] = d
        for j in g[i]:
            if j == p: continue
            st[j][0] = i
            dfs(j, i, d+1)
    dfs(0, -1, 0)

    # 2.2 初始化st表
    for j in range(1, m):
        for i in range(n):
            if st[i][j - 1] != -1: #必须要有-1检查 否则越界造成错乱
                st[i][j] = st[st[i][j - 1]][j - 1]

    # 3. 简单LCA模板 - 只求lca （扩展可以维护求lca路径上的信息）
    def getLCA(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        # 3.1 先让ab同深度
        k = depth[a] - depth[b] # 将所有非空二进制bit对应的跳跃都作用上去
        for i in range(m):
            if k >> i & 1 == 1:
                a = st[a][i]

        # 3.2 如果a是b的祖先 则ab会想同。否则两者同时向上跳，直到lca的两个直连子节点为止
        if a != b:
            for i in range(m - 1, -1, -1): #从大到小bit尝试，如果没有跳过就作用上
                if st[a][i] != st[b][i]:
                    a, b = st[a][i], st[b][i]
            a = st[a][0]
        lca = a
        return lca
    # 这个过程实质上就是
    # ab同深度到lca(a,b) 需要一起跳跃k个祖先，k=0b10110 上面从高到低位实为尝试这个k
    # 证明：最后一定停在lca的直接子节点
    # 反证，如果不是 则ab各差了距离d （1<d<=k) ... 待证明

    def dist(a,b): #树上路径长度
        ancestor = getLCA(a,b)
        return depth[a] + depth[b] - 2*depth[ancestor]


"""
• 1483. 树节点的第 K 个祖先 -- 简单倍增模板
• 2836. 在传球游戏中最大化函数值 -- 除了跳表 再维护倍增路径的权重
• 2846. 边权重均等查询 --  LCA + 如何维护更复杂的树上路径信息
• 2277. 树中最接近路径的节点 -- 几组节点的lca
5.救灾【算法赛】 - 蓝桥云课 (lanqiao.cn)  lca求树上距离 + 博弈dp 
"""