"""
https://codeforces.com/problemset/problem/2154/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) 和一棵 n 个节点的无向树的 n-1 条边。节点编号从 1 到 n。

有一只猫位于节点 1，你需要让猫移动到节点 n。
你可以执行两种操作，格式如下：
"1"：猫会随便移动一步，即移动到猫所处节点的随机邻居上。如果没有邻居，猫不会移动。
"2 u"：摧毁节点 u。如果猫恰好在节点 u，你会获得 WA。如果节点 u 已被摧毁，则不会发生任何事情。
要求：总操作次数 ≤ 3n，且不能连续执行第二种操作。

输出具体的操作序列，使得无论猫如何移动，在所有操作结束后，猫一定位于节点 n。可以证明，这样的操作序列一定存在。
输出格式：先输出总操作次数 k，然后输出 k 个操作。
"""
import sys, itertools
from functools import cache
from heapq import heappop, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

"""


如果没有限制 就一直删掉分支 最后1 走到正确方向，但不能连续用2

提示: 奇偶层
从0出发 每走一步跨越奇偶层 所以下次删除可以删掉对面层的点 删叶节点不影响连通性
因为点随机，不能枚举树 不知道当前是什么节点 


"""
def solve(n, g, indegree):

    q = deque([1])
    vis = [False]*(n+1)
    vis[1] = True
    level = [0]*(n+1)
    l = 0

    while q:
        size = len(q)
        for _ in range(size):
            x = q.popleft()
            level[x] = l
            for y in g[x]:
                if not vis[y]:
                    vis[y] = True
                    q.append(y)
        l ^= 1

    leaves = [deque(), deque()]
    for i in range(1, n+1):
        if indegree[i] == 1 and i != n:
            leaves[level[i]].append(i)

    res = []
    cnt = n

    # 不能按点模拟 因为不知道具体的点
    # 按剩余点数量推
    cur = 0
    while cnt > 1:

        # 有一次删点机会
        if leaves[cur^1]: # 不在同层的叶节点可以删一个 (n不会被加入待删除叶子)
            d = leaves[cur^1].pop()
            res.append(f"2 {d}")
            cnt -= 1
            for j in g[d]:
                indegree[j] -= 1
                if indegree[j] == 1 and j != n:
                    leaves[level[j]].append(j)
        cur ^= 1

        # else:
            # 只能删除同层 但是不知道是不是当前自己的点 那就先走一步到对面
        if cnt > 1:
            res.append("1")

    return str(len(res)) + "\n" + "\n".join(res)


for _ in range(RI()):
    n = RI()
    g = [[] for _ in range(n+1)]
    indegree = [0]*(n+1)
    for _ in range(n-1):
        a,b = RII()
        g[a].append(b)
        g[b].append(a)
        indegree[a] += 1
        indegree[b] += 1

    print(solve(n, g, indegree))
    print()

