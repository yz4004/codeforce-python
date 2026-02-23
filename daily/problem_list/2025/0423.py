"""
https://www.luogu.com.cn/problem/P1966

输入 n(1≤n≤1e5) 和两个长为 n 的数组 a 和 b，元素范围 [0,2^31)。保证 a 中没有重复元素，b 中没有重复元素。

每次操作，你可以交换 a 中的一对相邻元素，或者 b 中的一对相邻元素。
为了最小化 (a[i]-b[i])^2 之和，至少要操作多少次？
输出【最小操作次数】模 1e8 - 3 的结果。

x1, x2
y1, y2

(x1-y1)^2 + (x2-y2)^2 -- f1
(x1-y2)^2 + (x2-y1)^2 -- f2

f1 - f2 = -2(x2 - x1) (y2 - y1) > 0 交换后缩小，需要f1-f2差为正数
即 (x2 - x1) (y2 - y1) < 0

a b c d
 最小的最大的相互组合
相邻之间组合

https://www.luogu.com.cn/record/214898253
"""

import sys, itertools
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

mod = 10**8 - 3
n = RI()

class BIT: # 维护区间sum(nums[l,r])
    def __init__(self, n: int, nums: List=None): #初始数组为0时启用
        self.a = [0] * (n + 1)
        if nums is not None:
            # 预处理nums 计算初始树状数组前缀和
            self.nums = nums
            for i, x in enumerate(nums, 1): # 所有nums[i] => a[i+1]
                self.a[i] += 1
                pa = i + (i & -i) # i 父节点，其管辖着i所在的区间
                if pa <= n:
                     self.a[pa] += self.a[i] # 启发式更新

    # 单点更新 nums[idx]+=x
    def add(self, i, x): # 原数组i映射到bit上需加一 nums[i] => a[i+1]
        i = i + 1
        a, n = self.a, len(self.a)
        while i < n:
            a[i] += x
            i += i & -i

    def sum(self, i: int): # nums[:i], [0,i) 这里无需串位，原数组i取不到
        res = 0
        while i > 0:
            res += self.a[i]
            i -= i & -i
        return res

    def rsum(self, l:int, r:int) -> int: # 区间sum(nums[l,r])
        return self.prefix_sum(r+1) - self.prefix_sum(l)

def solve(a, b):
    # a-discretization
    n = len(a)
    def discretization(a):
        # to_ranked_array
        idx = sorted(set(a))
        return [bisect_left(idx, x) for x in a]

    a = discretization(a)
    b = discretization(b)

    # 1. 将ab离散化 转化成坐标
    # 1 0 3 2
    # 7 6 9 8 -- a
    # 3 2 1 0 -- b
    # 3 2 1 0

    # 0 1 2 3
    # 1 0 3 2 a的顺序
    # 3 2 1 0 b现在的顺序
    # 1 0 3 2 b应该按照这个顺序排列
    # 2 3 0 1 当前b的每个元素，应该映射到的索引位置。以对齐a 将这个排序后代表b的现在元素映射到对应索引上

    mp = {x:i for i,x in enumerate(a)}
    c = [0]*n
    for i, x in enumerate(b):
        c[i] = mp[x] # x在a中的位置

    # def to_ranked_array(arr):
    #     sorted_arr = sorted(arr)
    #     return [sorted_arr.index(x) for x in arr]
    #
    # # 将 a, b 离散化为排名（无重复，index可直接用）
    # a_rank = to_ranked_array(a)
    # b_rank = to_ranked_array(b)
    # n = len(a)
    # 构造 p[a[i]] = i，表示 a 排序后，每个值应该在的位置
    # p = [0] * n
    # for i, x in enumerate(a_rank):
    #     p[x] = i
    #
    # # 将 b 中每个值 v 映射到 a 排序后的目标位置，即变换后的 b
    # c = idx = [p[v] for v in b_rank]

    tree = BIT(n)

    res = 0
    for cnt, x in enumerate(c, 1):
        res += cnt - 1 - tree.sum(x+1)
        # print(c[:cnt], x)
        # print(tree.sum(x+1),  cnt - 1 - tree.sum(x+1), "----", res)
        # print()
        tree.add(x, 1)
    return res
a, b = RILIST(), RILIST()
print(solve(a, b)%mod)

sys.exit(0)

def solver2(a, b):
    mod = 10**8 - 3
    n = len(a)

    def to_ranked_array(arr):
        sorted_arr = sorted(arr)
        return [sorted_arr.index(x) for x in arr]

    # 将 a, b 离散化为排名（无重复，index可直接用）
    a_rank = to_ranked_array(a)
    b_rank = to_ranked_array(b)

    # 构造 p[a[i]] = i，表示 a 排序后，每个值应该在的位置
    p = [0] * n
    for i, x in enumerate(a_rank):
        p[x] = i

    # 将 b 中每个值 v 映射到 a 排序后的目标位置，即变换后的 b
    mapped = [p[v] for v in b_rank]
    print("mapped", mapped)

    # 归并排序统计逆序对
    def merge_sort(arr):
        def sort(lo, hi):
            if hi - lo <= 1:
                return 0
            mid = (lo + hi) // 2
            inv = sort(lo, mid) + sort(mid, hi)
            i = j = 0
            left = arr[lo:mid]
            right = arr[mid:hi]
            for k in range(lo, hi):
                if i < len(left) and (j == len(right) or left[i] <= right[j]):
                    arr[k] = left[i]
                    i += 1
                else:
                    inv += len(left) - i
                    arr[k] = right[j]
                    j += 1
            return inv
        return sort(0, len(arr))

    return merge_sort(mapped) % mod


def brute_force_inversions(arr):
    cnt = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                cnt += 1
    return cnt
import random
# 对拍测试
for _ in range(1):
    n = random.randint(1, 1000)
    # random.sample(range(1 << 30), n)
    # a = [random.randint(1, 1<<30) for _ in range(n)]
    # b = [random.randint(1, 1<<5) for _ in range(n)]

    a = random.sample(range(1 << 30), n)
    b = random.sample(range(1 << 30), n)

    # a = [8, 4, 9, 3, 2, 5, 6, 1, 0, 7]
    # b = [0, 2, 1, 5, 6, 0, 4, 4, 3, 3]

    # a = [0, 4, 1, 3, 2]
    # b = [4, 0, 2, 1, 3]

    # a = [1,2,2,2]
    # b = [0,3,2,1]

    # for brute force
    # nums = sorted(zip(a, b))
    # b_sorted = [x[1] for x in nums]
    #
    # # 构造b_sorted在b中的位置顺序
    # pos = {v: i for i, v in enumerate(sorted(b_sorted))}
    # mapped = [pos[x] for x in b_sorted]
    #
    # expected = brute_force_inversions(mapped)
    expected = solver2(a, b)
    actual = solve(a, b)

    if expected != actual:
        print("Mismatch!")
        print(f"a = {a}")
        print(f"b = {b}")
        print(f"expected = {expected}, actual = {actual}")
        break
else:
    print("✅ All tests passed!")