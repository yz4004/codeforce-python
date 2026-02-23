"""
https://www.luogu.com.cn/problem/P1972

输入 n(1≤n≤1e6) 和长为 n 的数组 a(1≤a[i]≤1e6)。数组下标从 1 开始。
然后输入 m(1≤m≤1e6) 和 m 个询问，
每个询问输入 L R(1≤L≤R≤n)。

对于每个询问，输出 a 的子数组 [L,R] 中有多少种不同元素。
"""
import sys
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

class BIT:
    def __init__(self, n: int, nums: List = None):
        self.n = n
        self.a = [0] * (n + 1)
        # 启发式更新 i的父节点是 i + lb(i)
        if nums is not None:
            self.nums = nums
            for i, x in enumerate(nums, 1):
                self.a[i] += x
                pa = i + (i & -i)
                if pa <= n:
                    self.a[pa] += self.a[i]

    # nums[i] += x
    def add(self, i, x):
        i = i + 1
        a, n = self.a, len(self.a)
        while i < n:
            a[i] += x
            i += i & -i

    # 前缀查询 [:i] 前i个的和
    def sum(self, i: int):
        res = 0
        while i > 0:
            res += self.a[i]
            i -= i & -i
        return res

    # 区间查询 [l,r] 查询闭区间
    def rsum(self, l: int, r: int) -> int:
        return self.sum(r + 1) - self.sum(l)


n, nums = RI(), RILIST()

queries = [None for _ in range(n)]
m = RI()
for idx in range(m):
    L, R = RII()
    L, R = L-1, R-1
    if not queries[L]: queries[L] = []
    queries[L].append((R,idx))


nxt = [-1]*n
seen = [-1]*(max(nums)+1)
for i in range(n-1,-1,-1):
    x = nums[i]
    if seen[x] != -1:
        nxt[i] = seen[x]
    seen[x] = i

tmp = [0]*n
for x,i in enumerate(seen):
    if i != -1:
        tmp[i] = 1

tree = BIT(n, tmp)
res = [0]*m
l = 0
for L in range(n):
    while l < L:
        if tmp[l] and nxt[l] >= L:
            t = nxt[l]
            tmp[t] = 1
            tree.add(t, 1)
        l += 1

    if not queries[L]: continue
    pl = tree.sum(L)
    for R,idx in queries[L]:
        # [L,R]
        res[idx] = tree.sum(R+1) - pl  #tree.rsum(L,R)

print("\n".join(map(str, res)))






