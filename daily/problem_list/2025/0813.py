"""
https://codeforces.com/problemset/problem/2129/B

输入 T(≤1e3) 表示 T 组数据。所有数据的 n 之和 ≤5e3。
每组数据输入 n(2≤n≤5e3) 和 1~n 的排列 p。

对于每个 p[i]，可以保持不变，也可以改成 2n-p[i]。
目标是让 p 的逆序对个数最小。

输出最小逆序对个数。

"""
import sys
from functools import cache
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

class BIT:
    # 树状数组维护前缀和 (1-base)
    # 单点更新 + 区间查询 + BIT二分
    # 所有入参坐标均对应原数组坐标
    # - 前缀查询 [:i] 前i个
    # - 区间查询 [l,r] 查询闭区间
    # - 二分查询 [:i] 最小的i使得前缀 [:i] >= target
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

    # 二分查询 [:i] 最小的i使得前缀 [:i] >= target （对比静态前缀和数组上二分）
    # 目标i=0b10110 对应从左向右要跳过的管辖区间, 我们从高位向低找 如果 0b10000 对应长度的和小于target就减去，初始枚举段长的n的最高比特位
    # 只有前缀和数组单调递增才能二分
    def lower_bound(self, target):
        # 返回最小 idx，使 self.sum(idx) >= target;
        step = 1 << (self.n.bit_length() - 1)  # 0b1011 取1<<3 = 0b1000
        i = 0  # 从虚节点开始，在位跳里维护的是已确定可以跳过的最大右端点 i，是上一轮跳过后的前缀右端点, [0,i] 计入到target里  sum(idx) < target
        while step:
            j = i + step  # j-右端点候选, 尝试跳过 (i,j] 长度为 2^p
            if j <= self.n and self.a[j] < target:
                target -= self.a[j]
                i = j
            step = step >> 1
        return i + 1

    def lb(self, x):
        return x & -x



for _ in range(RI()):
    n, a = RI(), RILIST()

    # 1 - 2n-1
    # 翻转 引入的新增逆序对： -前面的逆序对 + 后面的顺序对
    f = [0]*(n+1)
    tree = BIT(n)

    for i, x in enumerate(a):
        x -= 1 # 0-n-1
        #
        rev = tree.rsum(x, n-1) # [x, n-1]

        f[n-x] = mn(rev, n-1-x-rev) # [x, n-1] n-x个元素

        tree.add(x, 1)

    for i in range(n):
        f[i+1] += f[i]

    print(f[n])
