"""
https://codeforces.com/problemset/problem/2114/E

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。
然后输入一棵 n 个节点的无向树的 n-1 条边。节点编号从 1 开始。

树根为 1。节点点权记录在数组 a 中。
对于节点 v=1,2,3,...,n，输出从 v 往上的最大交替子段和，即 a[v] - a[parent[v]] + a[parent[parent[v]]] - ... 的最大值。

- 当前 a[v] 贡献来自 a[v] - 父节点的某个交替子段和 (应为最小)
- 这要求维护每个 a[v] 向上的最小交替子段和
- 当a[v]向下传递最小子段和 应来源为 a[v] - 父节点的某个交替子段和 (应为最大)
- 所以同时维护最大最小交替子段和
"""
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


T = RI()
for _ in range(T):
    n = RI()
    nums = RILIST()
    g = [[] for _ in range(n)]
    for _ in range(n-1):
        a, b = RII()
        a, b = a-1, b-1
        g[a].append(b)
        g[b].append(a)

    res = [0]*n
    def dfs(i, p, mx_v, mn_v):

        res[i] = nums[i] - mn(mn_v, 0)
        new_mx_v = nums[i] - mn(mn_v, 0)
        new_mn_v = nums[i] - mx(mx_v, 0)
        for j in g[i]:
            if j == p: continue
            dfs(j, i, new_mx_v, new_mn_v)
    dfs(0, -1, 0, 0)
    print(" ".join(map(str, res)))
