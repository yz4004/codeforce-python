



"""
tarjan 求割点与桥 无向图

在一次dfs中额外维护
    dfn 第一次访问时间戳;
    low u为根dfs子树 遍历子树+找一条返祖边 能到达的最早祖先

为什么引入返祖边和low可以判断割点/桥
    u->v 如果v子树有返祖边回到比u早的点 说明u->v 不是唯一进入v子树的边
    low[v] > dfn[u] - uv桥
    low[v] >=dfn[v] - v割点

        等号差异来自“能否回到 u 本身”：
        桥要更严格：连回到 u 都不行（>）
        割点只要求回不到 u 的祖先即可（>=），回到 u 本身也无法绕过删除 u 这个事实

"""

def tarjan_undirected_graph(n, edges): # 输入n节点的无向图
    # n 节点数
    # edges 无向边，可含重边
    # 返回
    #   cutpoints: [u...]
    #   bridges [(u,v)...]
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    is_cut = [False]*n
    bridges = []
    cutpoints = []

    dfn = [0] * n  # 节点 u 第一次被 DFS 访问到的时间戳（1..）
    low = [0] * n  # dfs树中 从u出发

    time = 1
    def dfs(i, p):
        nonlocal time
        dfn[i] = dfn[i] = time
        time += 1

        for j in g[i]:
            if j == p: continue

            if dfn[j] == 0: # 对未访问的子分支搜索
                dfs(j, i)

                # 桥 i -> j 成立的条件是j返回不到比i早的点
                if low[j] > low[i]:
                    bridges.append((i,j))

                # i是割点.
                if low[j] >= low[i]:

            # 更新low[i]
            if low[j] < low[i]:
                low[i] = low[j]

"""
https://chatgpt.com/c/696f17b9-0914-8331-a4e0-3d8b24f02bad

从已经联通的部分拆出不联通 - 割点/桥

LC1568. 使陆地分离的最少天数 (涨水淹没陆地 创造出不联通 无向图)
    https://leetcode.cn/problems/minimum-number-of-days-to-disconnect-island/
    
LC1192. 查找集群内的关键连接 (有向图)
    https://leetcode.cn/problems/critical-connections-in-a-network/description/

其他见 图论题单:
https://leetcode.cn/discuss/post/3581143/fen-xiang-gun-ti-dan-tu-lun-suan-fa-dfsb-qyux/
"""