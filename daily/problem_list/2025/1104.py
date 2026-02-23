"""
https://codeforces.com/problemset/problem/2149/E

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n k(1≤k≤n≤2e5) L R(1≤L≤R≤n) 和长为 n 的数组 a(1≤a[i]≤1e9)。

输出 a 有多少个连续子数组 b，满足 b 的长度在 [L,R] 中，且 b 恰好有 k 个不同元素。

"""
import bisect
import itertools
import sys
from collections import defaultdict
from functools import cache
from operator import add, xor
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, k, L, R = RII()
    a = RILIST()

    tmp = sorted(list(set(a)))
    for i,x in enumerate(a):
        a[i] = bisect.bisect_left(tmp, x)


    # 容斥原理 - inclusion-exclusion principle
    # <=R, <=k
    # -  <L, <=k
    # - <=R, <k
    # + <L, <k

    # <=R, <=k  -- 第一个滑窗统计所有符合该条件的子数组
    # <L  <k -- 第二个滑窗删除满足 <L 或者 cnt<k 的子数组

    # 不超过k 且 长度不超过R
    def check(k, R):
        res = 0
        cnt = [0]*len(a) # defaultdict(int)
        l = 0
        unique = 0
        for i, x in enumerate(a):
            if cnt[x] == 0: unique += 1
            cnt[x] += 1
            # [l,i] L,R
            while unique > k or i - l + 1 > R:
                d = a[l]
                cnt[d] -= 1
                #if cnt[d] == 0: del cnt[d]
                if cnt[d] == 0: unique -= 1
                l += 1
            res += i - l + 1
        return res

    res = check(k, R) - check(k-1, R) - check(k, L-1) + check(k-1, L-1)

    print(res)

