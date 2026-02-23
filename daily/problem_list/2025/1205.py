"""
https://codeforces.com/problemset/problem/840/D

输入 n q(1≤n,q≤3e5) 和长为 n 的数组 a(1≤a[i]≤n)。下标从 1 开始。
然后输入 q 个询问，每个询问输入 L R(1≤L≤R≤n) 和 k(2≤k≤5)。

对于每个询问，输出 a 的子数组 [L,R] 中出现次数严格大于 floor((R-L+1)/k) 的最小元素值。如果不存在这样的数，输出 -1。


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
    __slots__ = "l", "r", "lo", "ro", "cnt", "sm"

    # [l,r] lo/ro + 该线段维护内容 - [l,r] 的子区间 cnt, sum
    def __init__(self, l, r, lo=None, ro=None, cnt=0, sm=0):
        self.l = l
        self.r = r
        self.lo = lo
        self.ro = ro
        self.cnt = cnt
        self.sm = sm

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
        self.cnt = self.lo.cnt + self.ro.cnt
        self.sm = self.lo.sm + self.ro.sm

    def add(self, i, x) -> "Node":
        l, r, lo, ro = self.l, self.r, self.lo, self.ro
        o = Node(self.l, self.r, self.lo, self.ro, self.cnt, self.sm)
        # 自根节点下 新增一条path 对应着更新版本后的树 -- 在i处增加x后的版本
        if self.l == self.r:
            o.cnt += 1
            o.sm += x
            return o

        mid = (self.l + self.r) // 2
        if i <= mid:
            o.lo = self.lo.add(i, x)
        if mid + 1 <= i:
            o.ro = self.ro.add(i, x)
        # self.merge()
        o.merge()  # 要对新版本的节点维护，旧版本不动
        return o

    def kth(self, old: "Node", k) -> int:  # 1-based -- 认为第一个是 1th 2dn...
        if self.l == self.r:
            return self.l
        cnt_l = self.lo.cnt - old.lo.cnt
        if k <= cnt_l:
            return self.lo.kth(old.lo, k)
        else:
            return self.ro.kth(old.ro, k - cnt_l)

    def query(self, old: "Node", L, R) -> (int, int):
        l, r, lo, ro = self.l, self.r, self.lo, self.ro
        if L <= self.l and self.r <= R:
            return self.cnt - old.cnt, self.sm - old.sm

        res_cnt = res_sm = 0
        mid = (self.l + self.r) // 2
        if L <= mid:
            cnt, sm = self.lo.query(old.lo, L, R)
            res_cnt += cnt
            res_sm += sm
        if mid + 1 <= R:
            cnt, sm = self.ro.query(old.ro, L, R)
            res_cnt += cnt
            res_sm += sm
        return res_cnt, res_sm

def solve(n, a, queries) -> List[int]:

    # k=2...5
    # m=[n//k]
    # >= m+1
    # [1,m] - m
    # [m+1, 2*m+1] - m+1
    # [2m+2, 3m+2] - m+1
    # [3m+3, ...
    # 只许检查 0 m+1, 2m+2 3m+3 ...


    trees:List["Node"] = [None]*(n+1)
    trees[0] = Node.build(0, n)
    for i in range(n):
        trees[i+1] = trees[i].add(a[i], 1)

    res = []
    for L,R,k in queries:

        # [L,R] 中出现次数严格大于 floor((R-L+1)/k) 的最小元素值
        m = (R-L+1) // k

        cur = -1
        for ki in range(0, R-L+1, m+1):

            x = trees[R+1].kth(trees[L], ki+1)
            # kth element = x

            cnt_x = trees[R+1].query(trees[L], x, x)[0]
            # print((L,R,k), ki, (x, cnt_x))
            if cnt_x > m:
                cur = x
                break

        res.append(cur)
    return res




n, q = RII()
a = RILIST()
queries = []
for _ in range(q):
    L,R,k = RII()
    L, R = L - 1, R - 1
    queries.append((L,R,k))

res = solve(n, a, queries)
print("\n".join(map(str, res)))




