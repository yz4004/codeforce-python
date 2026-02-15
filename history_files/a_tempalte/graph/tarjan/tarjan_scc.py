"""
tarjan 强联通分量（有向图） strong connected component
两个数组保存点的两个信息：
    dfn: dfs过程中的访问时间戳 (前序到达时更新）
    low: 能回溯到的最早时间戳 （前序到达时更新，后续动态更新）

stack: 用来保存强连通块中的点，随着查找当前分块的过程增长，在找到根节点时弹出
"""
def tarjan_scc(n, edges): #输入n节点的有向图
    g = [[] for _ in range(n)]
    for a,b in edges:
        g[a].append(b)

    dfn = [0]*n #我们的时间戳从1开始，所以初始值为0代表没有更新
    low = [0]*n
    time = 1
    stack = []
    in_stack = [False]*n
    scc = [] # strong connected component
    def dfs(i):
        nonlocal time
        dfn[i] = low[i] = time
        time += 1
        stack.append(i)
        in_stack[i] = True

        for j in g[i]:
            if dfn[j] == 0: #未被访问过 时间戳为0 其应为i为根的搜索子树的子节点
                dfs(j)
                low[i] = min(low[i], low[j])
            elif in_stack[j]: #可到达的祖先 只更新low 其实多余 但是说明示意
                low[i] = min(low[i], low[j])
            # else 不存在dfn非0即初始化过时间戳，而初始化时间戳的点一定in_stack

        if dfn[i] == low[i]: #连通块的根节点
            new_scc = []
            while stack[-1] != i:
                new_scc.append(stack.pop())
            new_scc.append(stack.pop()) # i 栈顶
            scc.append(new_scc)

    for i in range(n):
        if dfn[i] == 0:
            dfs(i)
    return scc


"""
核心 - dfs生成树，时间戳

ref:
BV19J411J7AZ - scc  
BV1Q7411e7bM - cut vertices & bridge
"""

