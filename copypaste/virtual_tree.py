from collections import defaultdict
from itertools import pairwise
from typing import List



def interactionCosts( n: int, edges: List[List[int]], group: List[int]) -> int:
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 组内元素跨度大 - u很大时 - 虚树

    # dfn 部分
    time = 0
    tin = [-1] * n
    tout = [-1] * n
    def dfs(i, p):
        nonlocal time
        tin[i] = time
        time += 1
        for j in g[i]:
            if j == p: continue
            dfs(j, i)
        tout[i] = time
    dfs(0, -1)

    def is_ancestor(u, v):
        # v -> u
        return tin[u] <= tin[v] <= tout[v] <= tout[u]

    ########################################## lca
    # 1. 初始化图，跳表深度为图的最大节点数取log 即bit_length
    # 2. 深度表 st跳表 （有时还需跳表跳跃路径对应值）
    m = n.bit_length()
    depth = [0] * n
    st = [[-1] * m for _ in range(n)]

    # 2.1 dfs初始化 深度/parent
    def dfs(i, p, d):
        depth[i] = d
        for j in g[i]:
            if j == p: continue
            st[j][0] = i
            dfs(j, i, d + 1)

    dfs(0, -1, 0)

    # 2.2 初始化st表
    for j in range(1, m):
        for i in range(n):
            if st[i][j - 1] != -1:  # 必须要有-1检查 否则越界造成错乱
                st[i][j] = st[st[i][j - 1]][j - 1]

    # 3. 简单LCA模板 - 只求lca （扩展可以维护求lca路径上的信息）
    def getLCA(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        # 3.1 先让ab同深度
        k = depth[a] - depth[b]  # 将所有非空二进制bit对应的跳跃都作用上去
        for i in range(m):
            if k >> i & 1 == 1:
                a = st[a][i]

        # 3.2 如果a是b的祖先 则ab会想同。否则两者同时向上跳，直到lca的两个直连子节点为止
        if a != b:
            for i in range(m - 1, -1, -1):  # 从大到小bit尝试，如果没有跳过就作用上
                if st[a][i] != st[b][i]:
                    a, b = st[a][i], st[b][i]
            a = st[a][0]
        lca = a
        return lca

    def dist(a, b):  # 树上路径长度
        ancestor = getLCA(a, b)
        return depth[a] + depth[b] - 2 * depth[ancestor]
    ########################################## lca

    # 分组构造虚树
    ans = 0
    grps = defaultdict(list)
    for i, x in enumerate(group):
        grps[x].append(i)

    for group_x, nodes in grps.items():
        if len(nodes) == 1: continue

        # 1. 将该组内点按dfn序排序
        nodes.sort(key=lambda i: tin[i])


        # 枚举dfn序临近的点 两两求lca 作为虚拟节点 然后去重
        # x-y-z 得到的 虚拟节点 a,b 其中a b 都是y的ancestor
        all_nodes = nodes[:]
        for i in range(1, len(nodes)):
            # x,y 的ancestor不一定是虚树 y 的直接父节点，可能他和右侧一个z有更矮的祖先
            all_nodes.append(getLCA(nodes[i - 1], nodes[i]))
            
        all_nodes = sorted(set(all_nodes), key=lambda i: tin[i]) 
        rt = all_nodes[0]

        # 对虚拟节点去重后 按dfn序排序. 然后连边
        # 单调栈构造法: https://oi-wiki.org/graph/virtual-tree/
        # vg = defaultdict(list)
        # for i in range(1, len(all_nodes)):
        #     x, y = all_nodes[i - 1], all_nodes[i]
        #     lca = getLCA(x, y)
        #
        #     # 为什么这里不对 x 操作 - 因为上轮 当前x作为y被加过了 首轮x是最早的lca即根节点
        #     # 因为按dfn排序 y是后出现的子节点
        #     dy = dist(y, lca)
        #     vg[lca].append((y, dy))
            

        # stack build virtual tree (directed parent -> child)
        vg = defaultdict(list)
        st_stack = []
        st_stack.append(all_nodes[0])
        rt = all_nodes[0]
        for v in all_nodes[1:]:
            # pop until stack top is ancestor of v
            while st_stack and not is_ancestor(st_stack[-1], v):
                st_stack.pop()

            # now stack top is parent in virtual tree
            p = st_stack[-1]
            vg[p].append((v, dist(p, v)))

            st_stack.append(v)


        # 自定义逻辑 在虚树上求解
        k = len(nodes)
        res = 0
        def dfs(i) -> int:  # 返回子树“原组”节点数量
            nonlocal res

            total = 1 if group[i] == group_x else 0
            for j, d in vg[i]:
                cnt = dfs(j)
                res += cnt * (k - cnt) * d
                total += cnt
            return total
        dfs(rt)
        ans += res

    return ans
"""
3786. 树组的交互代价总和 -  边贡献法 + 树形dp 虚树

"""




