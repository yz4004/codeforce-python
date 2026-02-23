"""
https://codeforces.com/problemset/problem/911/D

输入 n(1≤n≤1500) 和 1~n 的排列 p。下标从 1 开始。
然后输入 m(1≤m≤2e5) 和 m 个操作。
每个操作输入 L R(1≤L≤R≤n)，表示反转 p 的子数组 [L,R]。
操作是永久的。

输出每次操作后，p 的逆序对个数的奇偶性。
偶数输出 even，奇数输出 odd。

"""
import sys
from typing import List

# from sortedcontainers import SortedList

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
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


    def lb(self, x):
        return x & -x

# [l, r]
# [0, l-1] [l, r]

# [l,r] -- x
# comb(k,2) - x

# comb(k,2) - 2*x

# k * (k-1) // 2



n, p = RI(), RILIST()
cnt = 0
tree = BIT(n+1)
for x in p:
    cnt += tree.rsum(x+1, n)
    tree.add(x, 1)

cnt %= 2

# sl = SortedList()
for _ in range(RI()):
    l, r = RII()

    k = r-l+1
    d = (k-1) * k // 2
    cnt ^= d & 1
    if cnt == 0:
        print("even")
    else:
        print("odd")

