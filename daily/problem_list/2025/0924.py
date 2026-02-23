"""
https://codeforces.com/problemset/problem/2070/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤3e5。
每组数据先输入 n(2≤n≤3e5)，然后输入一棵有 n 个节点的树，节点编号从 1 到 n，根节点是 1。
输入格式为 p2,p3,...,pn，分别表示节点 2,3,...,n 的父节点。保证 1≤p[i]<i。

计算有多少个满足如下要求的非空节点序列 b。下标从 1 开始。
1. b[i] 是树的第 i 层的一个节点。（所以 b[1] 是根节点）
2. 当 i ≥ 2 时，b[i] 不是 b[i+1] 的父节点。

输出合法序列个数，模 998244353。

树形dp 补集法转移
"""
import sys
from bisect import bisect_left, bisect_right
from collections import deque

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
# MOD = 10 ** 9 + 7
MOD = 998244353

# sys.setrecursionlimit(1 << 25)
def solve(n, pa):

    g = [[] for _ in range(n)]
    for i,p in enumerate(pa, 1): # 节点 2..n 的父亲
        g[p-1].append(i)

    # 迭代 BFS 分层：levels[d] = 深度 d 的节点列表（节点用 0-index 存）
    levels = []
    q = deque([0])
    while q:
        size = len(q)
        cur = []
        for _ in range(size):
            u = q.popleft()
            cur.append(u)
            for v in g[u]:
                q.append(v)
        levels.append(cur)
    m = len(levels)

    # f[i] 必选i 子树的方案
    f = [0] * n
    # 只有深度 >= 1 的 f[u] 才有意义；叶子（深度>=1）初始为 1
    for u in levels[m-1]:
        if u != 0:
            f[u] = 1

    t = 0
    for l in range(m-2, 0, -1):

        total_next = 0
        for v in levels[l+1]:
            total_next = (total_next + f[v]) % MOD

        # t += sum(f[x] for x in levels[l+1]) % MOD  += 累计 允许跳层
        # 题目要求每层必须有一个人，b序列应该是前缀 而不是

        # 本层每个点：1 + (下一层总 - 子女和)
        for u in levels[l]:
            # 允许停在 u：+1
            val = 1
            # 加上跨到下一层非子女的续选
            sum_children = 0
            for v in g[u]:
                sum_children = (sum_children + f[v]) % MOD
            val = (val + (total_next - sum_children)) % MOD
            f[u] = val

    # 根层（深度 0）：首跳不受限制
    ans = 1  # 只选根
    if m >= 2:
        for v in levels[1]:
            ans = (ans + f[v]) % MOD
    return ans % MOD


for _ in range(RI()):
    n = RI()
    pa = RILIST()
    print(solve(n, pa))