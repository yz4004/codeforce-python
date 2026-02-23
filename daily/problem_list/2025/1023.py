"""
复习。温故而知新。

https://codeforces.com/problemset/problem/703/D

输入 n(1≤n≤1e6) 和长为 n 的数组 a(1≤a[i]≤1e9)。下标从 1 开始。
然后输入 m(1≤m≤1e6) 和 m 个询问。
每个询问输入 L R(1≤L≤R≤n)，输出 a 的子数组 [L,R] 中的出现次数为偶数的元素，去重后的异或和。

对 [l,r] 整体 xor 和会把奇数保留 偶数抵消
再将其与 [l,r] 中所有 unique 的元素 xor
即消掉奇数 剩余偶数

同 HH的项链 https://www.luogu.com.cn/problem/P1972
"""
import itertools
import sys
from operator import add, xor
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


class BIT:
    def __init__(self, n: int, operator=add, nums: List = None):
        self.n = n
        self.a = [0] * (n + 1)
        self.op = operator
        # 启发式更新 i的父节点是 i + lb(i)
        if nums is not None:
            self.nums = nums
            for i, x in enumerate(nums, 1):
                # self.a[i] += x
                # self.a[i] = self.op(self.a[i], x)
                self.a[i] ^= x
                pa = i + (i & -i)
                if pa <= n:
                    # self.a[pa] = self.op(self.a[pa], self.a[i])
                    self.a[pa] ^= self.a[i]

    # nums[i] += x
    def add(self, i, x):
        i = i + 1
        a, n = self.a, len(self.a)
        while i < n:
            # self.a[i] = self.op(self.a[i], x)
            self.a[i] ^= x
            i += i & -i

    # 前缀查询 [:i] 前i个的和
    def sum(self, i: int):
        res = 0
        while i > 0:
            # res = self.op(self.a[i], res)
            res ^= self.a[i]
            i -= i & -i
        return res

    # 区间查询 [l,r] 查询闭区间
    def rsum(self, l: int, r: int) -> int:
        return self.sum(r + 1) - self.sum(l)


n, nums = RI(), RILIST()
ps = list(itertools.accumulate(nums, xor, initial=0))

queries = {}
m = RI()
for idx in range(m):
    L, R = RII()
    L, R = L-1, R-1
    if L not in queries: queries[L] = []
    queries[L].append((R,idx))


nxt = [-1]*n
seen = {}
for i in range(n-1,-1,-1):
    x = nums[i]
    if x in seen:
        nxt[i] = seen[x]
    seen[x] = i

tmp = [0]*n
for x,i in seen.items():
    if i != -1:
        tmp[i] = x

tree = BIT(n, xor, tmp)
res = [0]*m
l = 0
for L in range(n):
    while l < L:
        if tmp[l] and nxt[l] >= L:
            t = nxt[l]
            tmp[t] = 1
            tree.add(t, nums[l])
        l += 1

    if L not in queries: continue
    pl = tree.sum(L)
    for R,idx in queries[L]:
        # [L,R]
        all_unqiue_xor = tree.sum(R+1) ^ pl #tree.rsum(L,R)
        res[idx] = (ps[R+1] ^ ps[L]) ^ all_unqiue_xor

print("\n".join(map(str, res)))






