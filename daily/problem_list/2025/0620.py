"""
https://codeforces.com/problemset/problem/176/E

输入 n(1≤n≤1e5) 和一棵无向树的 n-1 条边（节点编号从 1 开始），每条边包含 3 个数 x y z(1≤z≤1e9)，表示有一条边权为 z 的边连接 x 和 y。
一开始有一个集合 S，初始为空。
然后输入 q(1≤q≤1e5) 和 q 个询问，格式如下：
"+ v"：把点 v 加到集合 S 中，保证 v 不在 S 中。
"- v"：把点 v 从集合 S 中删除，保证 v 在 S 中。
"?"：输出包含 S 所有点的最小连通块（用最少的边连通 S 中所有点）的边权之和。

n, q <= 1e5
树上集合，包含他们的最小联通块也是个子树，根节点就是所有人的最近公共祖先
- 遍历s 维持一个公共祖先节点，和下一个人再取lca. 最后算子树边权之和 -- q*n*logn

"""

import sys
from bisect import bisect_left

from sortedcontainers import SortedList
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


n = RI()
# 1. 初始化图，跳表深度为图的最大节点数取log 即bit_length
m = n.bit_length()
g = [[] for _ in range(n)]
for _ in range(n-1):
    a,b,w = RII()
    a,b = a-1, b-1
    g[a].append((b,w))
    g[b].append((a,w))

# 2. 深度表 st跳表 （有时还需跳表跳跃路径对应值）
depth = [0]*n
depth2 = [0]*n
st = [[-1]*m for _ in range(n)]

# 2.1 dfs初始化 深度/parent
def dfs(i, p, d1, d2):
    depth[i] = d1
    depth2[i] = d2
    for j, w in g[i]:
        if j == p: continue
        st[j][0] = i
        dfs(j, i, d1+1, d2+w)
dfs(0, -1, 0, 0)

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
    anc = getLCA(a,b)
    return depth2[a] + depth2[b] - 2*depth2[anc]

# 前序遍历
idx = [0]
dfn = [-1]*n
prefix_order = [-1]*n
def dfs(i, p):
    dfn[i] = idx[0]
    prefix_order[idx[0]] = i

    idx[0] += 1
    for j, _ in g[i]:
        if j == p: continue
        dfs(j, i)
dfs(0, -1)
# print(dfn)
# print(prefix_order)

sl = SortedList()
res = 0
for _ in range(RI()):
    q = RS().split()
    # print(q, sl, res)
    # print()
    if q[0] == "+":
        v = int(q[1])-1
        v_time = dfn[v]
        j = bisect_left(sl, v_time) # 大于等于
        if not sl:
            sl.add(v_time)
            continue

        sz = len(sl)
        pre_idx = (j - 1 + sz) % sz
        nxt_idx = j % sz


        pre_dfn, nxt_dfn = sl[pre_idx], sl[nxt_idx]

        pre_node = prefix_order[pre_dfn]
        nxt_node = prefix_order[nxt_dfn]

        res += (dist(pre_node, v) + dist(v, nxt_node) - dist(pre_node, nxt_node)) // 2
        sl.add(v_time)

    elif q[0] == "-":
        v = int(q[1])-1
        v_time = dfn[v]
        j = bisect_left(sl, v_time) # 大于等于

        sz = len(sl)
        pre_idx = (j - 1 + sz) % sz
        nxt_idx = (j+1) % sz

        pre_dfn, nxt_dfn = sl[pre_idx], sl[nxt_idx]

        pre_node = prefix_order[pre_dfn]
        nxt_node = prefix_order[nxt_dfn]

        res -= (dist(pre_node, v) + dist(v, nxt_node) - dist(pre_node, nxt_node)) // 2
        sl.remove(v_time)

    else:
        # ? 最小连通块
        print(res)
