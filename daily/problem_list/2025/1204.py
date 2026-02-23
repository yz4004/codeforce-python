"""
https://codeforces.com/problemset/problem/893/F

输入 n(1≤n≤1e5) root(1≤root≤n) 和长为 n 的数组 a(1≤a[i]≤1e9)。
然后输入一棵 n 个节点的树的 n-1 条边。节点编号从 1 到 n。
树根为 root，点权为 a。

然后输入 m(1≤m≤1e6) 和 m 个询问。强制在线。
第 i 个询问输入两个数 p q(1≤p,q≤n)，用于计算 x = (p + lastAns) % n + 1 以及 k = (q + lastAns) % n。
其中 lastAns 为上一个询问的答案，初始值为 0。

对于每个询问：
找到在子树 x 中的，到 x 的最短路（边的个数）不超过 k 的点，输出这些点中的最小点权。

"""
from heapq import heappush, heappop
import sys
from math import inf
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7
class Node:
    __slots__ = "l", "r", "lo", "ro", "m",

    # [l,r] lo/ro + 该线段维护内容 - [l,r] 的子区间 cnt, sum
    def __init__(self, l, r, lo=None, ro=None, m=inf):
        self.l = l
        self.r = r
        self.lo = lo
        self.ro = ro
        self.m = m

    @staticmethod
    def build(l, r) -> "Node":
        o = Node(l, r)
        if l == r:
            return o
        mid = (l + r) // 2
        o.lo = Node.build(l, mid)
        o.ro = Node.build(mid + 1, r)
        return o

    def merge(self):  # 当前节点维护值
        # self.cnt = self.lo.cnt + self.ro.cnt
        self.m = mn(self.lo.m, self.ro.m)

    def add(self, i, x) -> "Node":
        o = Node(self.l, self.r, self.lo, self.ro, self.m)
        # 自根节点下 新增一条path 对应着更新版本后的树 -- 在i处增加x后的版本
        if self.l == self.r:
            if x < o.m:
                o.m = x
            return o

        mid = (self.l + self.r) // 2
        if i <= mid:
            o.lo = self.lo.add(i, x)
        if mid + 1 <= i:
            o.ro = self.ro.add(i, x)
        # self.merge()
        o.merge()  # 要对新版本的节点维护，旧版本不动
        return o

    def apply(self, i, x) -> None:
        # 自根节点下 新增一条path 对应着更新版本后的树 -- 在i处增加x后的版本
        if self.l == self.r:
            if x < self.m:
                self.m = x
            return

        mid = (self.l + self.r) // 2
        if i <= mid:
            self.lo.apply(i, x)
        if mid + 1 <= i:
            self.ro.apply(i, x)
        self.merge()  # 对当前版本的节点维护

    def query(self,  L, R) -> int:
        if L <= self.l and self.r <= R:
            return self.m  #

        res = inf
        mid = (self.l + self.r) // 2
        if L <= mid:
            m = self.lo.query( L, R)
            if m < res:
                res = m
        if mid + 1 <= R:
            m = self.ro.query(L, R)
            if m < res:
                res = m
        return res

    # def kth(self, old: "Node", k) -> int:
    #     if self.l == self.r:
    #         return self.l
    #     cnt_l = self.lo.cnt - old.lo.cnt
    #     if k <= cnt_l:
    #         return self.lo.kth(old.lo, k)
    #     else:
    #         return self.ro.kth(old.ro, k - cnt_l)



def solve(n, root, a):
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        i, j = RII()
        g[i].append(j)
        g[j].append(i)

    tin = [0] * (n + 1)
    tou = [0] * (n + 1)
    depth = [0] * (n + 1)

    t = 0
    def dfs(i, p, d):
        nonlocal t
        depth[i] = d

        t += 1
        tin[i] = t
        for j in g[i]:
            if j == p: continue
            dfs(j, i, d + 1)
        tou[i] = t

    dfs(root, -1, 1)
    # t = 0
    # stack = [(root, 0, 0)]  # (当前节点, 父节点, 状态 0=入栈, 1=回栈)
    # depth[root] = 1
    #
    # while stack:
    #     u, p, state = stack.pop()
    #     if state == 0:
    #         t += 1
    #         tin[u] = t
    #         stack.append((u, p, 1))
    #         # 注意倒序压栈，保证遍历顺序和递归一致（可有可无）
    #         for v in reversed(g[u]):
    #             if v == p:
    #                 continue
    #             depth[v] = depth[u] + 1
    #             stack.append((v, u, 0))
    #     else:
    #         tou[u] = t

    levels = [[] for _ in range(n+1)]
    for i,d in enumerate(depth):
        if i == 0: continue
        levels[d].append(i)

    # 给定子树节点i 查询这个范围的j 里最小的 a[j]
    # i - [tin[i], tou[i]], depth[j] < di + k -- a[j]
    # [l,r], d < depth

    # trees[i] - 深度为i的版本
    trees: List["Node"] = [None] * (n + 1)
    trees[0] = Node.build(0, n+1)

    # for d, tin_i, tou_i, i, v in tmp:
    #     # d, [tin_i, tou_i], i, (v)
    #     # 在dfn数组上，在 dfn[tin_i]=v 影响范围是 [tin_i, tou_i]
    #
    #     if trees[d] is None:
    #         trees[d] = trees[d - 1].add(tin_i, v)  # 记录入时
    #     else:
    #         trees[d].apply(tin_i, v)  #

    for d in range(1, n+1):

        trees[d] = trees[d - 1]
        if levels[d]:
            for i in levels[d]:
                tin_i = tin[i]
                v = a[i-1]
                trees[d] = trees[d].add(tin_i, v)  #


    res = []
    last_ans = 0
    for _ in range(RI()):
        p, q = RII()

        # (p + last_ans) % n + 1 -- x
        # (q + last_ans) % n     -- k

        # subtree x (1-n)
        # in subtree, shortest path (edges) <= k -- minimal point weight

        x, k = (p + last_ans) % n + 1, (q + last_ans) % n
        l, r = tin[x], tou[x]
        d = depth[x]
        # [l,r] <= d+k 的 min
        # print("-------------", (x,d), (l,r), (d+k, l,r))
        last_ans = trees[mn(n, d + k)].query(l, r)
        res.append(last_ans)
    return res


n, root = RII()
a = RILIST()
res = solve(n, root, a)
print("\n".join(map(str, res)))






