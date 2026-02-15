"""
tarjan 求割点与桥 （无向图）

割点
"""


def tarjan_bridge(n, edges):  # 输入n节点的无向图
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
        
    dfn = [0] * n  # 我们的时间戳从1开始，所以初始值为0代表没有更新
    low = [0] * n
    time = 1
    stack = []
    in_stack = [False] * n
    fa = [-1]*n #父节点
    # scc = []  # strong connected component
    points = [] #分割点
    edges = [] #分割边

    def dfs(i):
        nonlocal time
        dfn[i] = low[i] = time
        time += 1
        # stack.append(i)
        # in_stack[i] = True
        # child = len(g[i]) #对于case 2 判断子节点数量

        for j in g[i]:
            if dfn[j] == 0:  # 未被访问过 时间戳为0 其应为i为根的搜索子树的子节点
                fa[j] = i #不能在外部 是dfs搜索生成树的父节点，在外部会被图破坏树性质
                dfs(j)
                ############## 新增部分
                if fa[i] == -1 and len(g[i]) >= 2: #case 2
                    points.append(i)
                if fa[i] != -1 and low[j] >= dfn[i]: #case 1
                    points.append(i)
                if low[j] > dfn[i]:
                    edges.append((i,j))
                ##############
                low[i] = min(low[i], low[j])
            elif j != fa[i]: #in_stack[j]:  # 可到达的祖先 只更新low
                low[i] = min(low[i], low[j])
            # else 此时j可由i到达，但已不在栈中？

        # if dfn[i] == low[i]:  # 连通块的根节点
        #     new_scc = []
        #     while stack[-1] != i:
        #         new_scc.append(stack.pop())
        #     new_scc.append(stack.pop())  # i 栈顶
        #     scc.append(new_scc)

    for i in range(n):
        if dfn[i] == 0:
            dfs(i)
    return points, edges
