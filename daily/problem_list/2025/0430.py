"""
https://www.luogu.com.cn/problem/P4310

输入 n(1≤n≤1e5) 和长为 n 的数组 a(0≤a[i]≤1e9)。

找一个 a 的子序列 b，满足 b 中任意相邻元素的 AND 不等于 0。
输出 b 的最长长度。
注：长为 1 的 b 一定满足要求。

x & y == 0
- 每次新引入一个y 至少在x的所有1-bit上有一个1 对所有子数组中的x都需要这样
-

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

n = RI()
a = RILIST()
m = max(a).bit_length()
# res = 1
# for i in range(m):
#     cnt = sum(x >> i & 1 == 1 for x in a)
#     res = mx(res, cnt)
# print(res)

# 相邻元素
b = [0]*m
res = 1
for x in a:
    tmp = 0
    for i in range(m):
        if x >> i & 1 == 1:
            tmp = mx(tmp, b[i])

    for i in range(m):
        if x >> i & 1 == 1:
            b[i] = tmp + 1
print(max(b))
