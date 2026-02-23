
"""
https://codeforces.com/problemset/problem/1900/C

输入 T(≤5e4) 表示 T 组数据。所有数据的 n 之和 ≤3e5。
每组数据输入 n(2≤n≤3e5) 和一个长为 n 的字符串 s，只包含 U L R 三种字母。
然后输入 n 对整数 L[i] 和 R[i]，表示一棵 n 个节点的二叉树，第 i 个节点的左儿子和右儿子的节点编号分别为 L[i] 和 R[i]。
节点编号从 1 到 n。如果 L[i] = 0 表示 i 没有左儿子，如果 R[i] = 0 表示 i 没有右儿子。

每个节点 i 都有一个指令 s[i]，表示往父节点（U），左儿子（L），右儿子（R）方向移动。如果指令对应的节点不存在，则原地不动。
你可以修改 s 中的字母。
至少要修改多少次，使得我们能从根节点 1 出发，遵循节点上的指令，在移动过程中遇到叶子节点？
注意：不要求最终停留在叶子上，只要在移动过程中能遇到叶子就行。
"""

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


# import itertools
from math import inf
import sys
# sys.setrecursionlimit(300000+1)


N = RI()
for _ in range(N):
    n = RI()
    s = RS()
    g = [[-1, -1] for _ in range(n)]
    for i in range(n):
        a,b = RII()
        g[i][0] = a-1
        g[i][1] = b-1

    def dfs(i):
        if i == -1:
            return inf
        if g[i][0] == g[i][1] == -1:
            return 0
        # o0 = dfs(pa[i]) + ("U" != s[i])
        o1 = dfs(g[i][0]) + ("L" != s[i])
        o2 = dfs(g[i][1]) + ("R" != s[i])
        return min(o1, o2)
    print(dfs(0))

