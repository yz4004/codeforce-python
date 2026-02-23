

"""
笛卡尔树 （支持 O(logN) -> O(1) 静态数组 rmq)

ex:
    0 1 2 3 4 5  6  7  8  9  10
    9 3 7 1 8 12 10 20 15 18 5
          1
        /   \
      3       5
     / \       \
    9   7       8
                 \
                 10
                /  \
              12    15
                    / \
                  20  18
https://oi-wiki.org/ds/cartesian-tree/ （有构建图）
- 最小值是根，随后划分成两个子数组，问题递归
- 构建：
 如果用每次决定根节点的递归方式 需要查找 min [l,r] 的坐标 （但我们希望这是用法）
 单调栈维护右链
    上面9越到3就不需要9了, 但是遇到7则要先保留 （因为不确定右侧，直到1将它弹出） 提示我们入栈要更新pa
    1遇到8但不确定他就是右孩子，先保留知道5将他弹出。而且5只会更新8的pa, 提示我们只对最后一个出栈的人更新pa

- rmq (range minimum query) 操作
    min nums[l,r] 即为 lca(l,r) 最近公共祖先

https://chatgpt.com/c/6839ff78-e278-800a-ace3-72b2a94cc5b7
"""
def build_min_cartesian_tree(nums):
    n = len(nums)
    pa = [-1] * n
    s = [] # 栈内维护右链/右分支
    for i,x in enumerate(nums):
        d = -1
        while s and nums[s[-1]] > x:
            d = s.pop()
        if d > -1: pa[d] = i # 如果发生弹栈，则最后出栈的人更新pa 上图的8最后会被5弹出
        if s:
            pa[i] = s[-1] # 7入栈，pa是3，8入栈 pa暂定是1. 栈内都存的右链.
        s.append(i)
    return pa
# nums = list(map(int, "9 3 7 1 8 12 10 20 15 18 5".split()))
# print(build_min_cartesian_tree(nums))

def support_rmq_cartesian_tree(nums):
    n = len(nums)
    # 1. cartesian tree
    pa = build_min_cartesian_tree(nums)

    # 2. lca O(n*logU) 构建 + logU 单次查询 (如果用tarjan就可以O(1))
    g = [[] for _ in range(n)]
    root = -1
    for i,p in enumerate(pa):
        if p == -1:
            root = i
            continue
        g[p].append(i)

    LOG = (n-1).bit_length()
    up = [[-1]*n for _ in range(LOG)] # up[i][j] 维护树节点j的 2^i祖先，i=0即为父节点
    depth = [0]*n

    def dfs(u):
        for v in g[u]:
            depth[v] = depth[u] + 1
            up[0][v] = u
            dfs(v)
    dfs(root)

    for k in range(1, LOG):
        for v in range(n):
            if up[k-1][v] != -1:
                up[k][v] = up[k-1][ up[k-1][v] ]

    # 3. lca查询
    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        # 把 u 提到跟 v 同一深度
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != -1 and depth[up[k][u]] >= depth[v]:
                u = up[k][u]
        if u == v:
            return u
        # 一起往上跳
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]
        return up[0][u]

    # 4. range minimum query
    def range_min_query(l, r):
        # 返回 nums[l..r] 中的最小值的位置
        return lca(l, r)