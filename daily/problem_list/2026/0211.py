"""
https://codeforces.com/problemset/problem/1980/E

输入 T(≤1e4) 表示 T 组数据。所有数据的 n*m 之和 ≤2e5。
每组数据输入 n m (1≤n*m≤2e5) 和两个 n 行 m 列的矩阵，分别记作 a 和 b，元素范围 [1,nm]。
保证矩阵 a 是一个排列，即 [1,nm] 中的每个整数恰好出现一次。
保证矩阵 b 是一个排列，即 [1,nm] 中的每个整数恰好出现一次。

每次操作，你可以：
交换 a 中的任意两行，或者，交换 a 中的任意两列。

能否通过若干次操作，把 a 变成 b？
输出 YES 或 NO。
"""
import sys, itertools
from functools import cache
from heapq import heappop, heapify, heappush
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
目标交换14 
12
34

34 - 换行
12

43 - 换列 - 发现23也换了
21

交换56 但也影响力34 不能孤立的看
12  56  65
34  34  43
56  12  21  

交换行 r1 r2 - 列里的元素shift 每个cj里的元素只是换位置
交换列 c1 c2 - 行里的元素shift 每个ri里的元素...
- 必要条件.

在满足上面情况下 一定能还原吗

先换列. 使得a的列对上b的列. (所有元素match)


"""

def solve(m, n, a, b):

    def check(a,b):
        rowb = {}
        for r2 in b:
            cur = sorted(r2)
            rowb[cur[0]] = cur

        for r1 in a:
            cur = sorted(r1)
            x = cur[0]
            if x not in rowb or any(p != q for p,q in zip(rowb[x], cur)):
                return False
        return True

    # zip(nums1,nums2) - 相当于每次 (nums1[i], nums2[i]) ...
    # zip(*a) = zip(r1, r2 ... rm) = (r1[i], r2[i] ... rm[i]) for i...

    return check(a, b) and check(zip(*a), zip(*b))


for _ in range(RI()):
    m,n = RII()

    a = [RILIST() for _ in range(m)]
    b = [RILIST() for _ in range(m)]
    print("YES" if solve(m, n, a, b) else "NO")



