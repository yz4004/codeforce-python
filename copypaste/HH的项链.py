
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


class BIT:  # 1-based - 值域树状数组
    def __init__(self, n): # [1,n]
        self.n = n
        self.tree = [0] * (n + 1)

    def build(self, nums):
        # 启发式更新 i的父节点是 i + lb(i)
        n = self.n
        tree = self.tree
        if nums is not None:
            for i, x in enumerate(nums, 1):
                tree[i] += x
                pa = i + (i & -i)
                if pa <= n:
                    tree[pa] += tree[i]

    def add(self, i, delta): # a[i] += 1
        n = self.n
        tree = self.tree
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix_sum(self, i): # [1,i]
        res = 0
        tree = self.tree
        while i > 0:
            res += tree[i]
            i -= i & -i
        return res

    def kth(self, k): # 1-based 1...k
        idx = 0
        bit = 1 << (self.n.bit_length() - 1)
        tree = self.tree
        while bit:
            nxt = idx + bit
            if nxt <= self.n and tree[nxt] < k:
                k -= tree[nxt]
                idx = nxt
            bit >>= 1
        return idx + 1


def HH_necklace(n, a, Q, groups):
    # HH的项链
    # https://www.luogu.com.cn/problem/P1972
    # 查询 [l,r] 内unique的元素数量
    # 记录每个元素出现的第一个位置 然后区间和
    # 离散化 从低到高对查询区间左端点排序 标记 [L, 每个新x出现的位置
    tree = BIT(n) # [1,n]

    nxt = [-1]*n # nxt[i] 下一个和 a[i] 相同值的元素的索引位置 位置链表
    seen = [-1] * (max(a) + 1)
    for i in range(n - 1, -1, -1):
        x = a[i]
        if seen[x] != -1:
            nxt[i] = seen[x]
        seen[x] = i

    label = [0]*n
    for x, i in enumerate(seen):
        if i != -1:
            # tree.add(i+1, 1)
            label[i] = 1
    tree.build(label)

    res = [0]*Q
    for i in range(n):

        if groups[i]:
            pre = tree.prefix_sum(i)
            for r, idx in groups[i]:
                # [i,r]
                # [i+1,r+1] 对应闭区间. 左侧减去应该是 prefix_sum(i) - [1,i]
                # t = tree.prefix_sum(r+1) - tree.prefix_sum(i)
                t = tree.prefix_sum(r + 1) - pre
                res[idx] = t

        # 当前i是一个标记，查询区间即将右移，标记 [i+1,中下一个 x=a[i] 的位置
        if label[i] == 1:
            j = nxt[i]
            if j != -1:
                label[j] = 1
                tree.add(j+1, 1)

    return res

# n, a = RI(), RILIST()
# # queries = [tuple(RII()) for _ in range(RI())]
# groups = [None for _ in range(n)]
# Q = RI()
# for idx in range(Q):
#     l,r = RII()
#     if not groups[l - 1]: groups[l - 1] = []
#     groups[l - 1].append((r - 1, idx))
# res = HH_necklace(n, a, Q, groups)
# print("\n".join(map(str, res)))

"""
https://www.luogu.com.cn/problem/P1972 - 原题 查询子区间内unique元素的数量
https://codeforces.com/problemset/problem/703/D - 查询子区间内偶数频次元素的xor
https://codeforces.com/problemset/problem/1028/H
3721. 最长平衡子数组 II  - 查询 [l,) 最长的和为0子数组 + 前缀和线段树 + 离散中值定理

    
"""