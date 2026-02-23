"""
https://codeforces.com/problemset/problem/731/F

输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤2e5)。

选择 a 中的一个数 x = a[i]，然后把其余元素 a[j] 都修改为 <= a[j] 且是 x 的倍数的数。

输出修改后的 sum(a) 的最大值。

"""
import itertools
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(n, a):   # usage

    # 和位置无关 考虑排序后枚举x
    # 对每个 x，枚举 kx，阶梯状的向后枚举
    # [kx - (k+1)x) 所有出现在数组里的数每人可以提供 kx
    # 排序后二分搜索可以，也可以调和级数枚举，U*logU 范围不大更快

    res = 0
    u = max(a)
    cnt = [0]*(u+1)
    for x in a:
        cnt[x] += 1

    ps = list(itertools.accumulate(cnt, initial=0)) # ps[x] - 小于x的所有数的计数
    for x in range(1, u+1):
        # x 2x ...
        if cnt[x] == 0: continue

        cur = 0
        for kx in range(x, u+1, x):
            cur += ps[-1] - ps[kx]

        cur *= x
        if cur > res:
            res = cur
    return res

    # sum (u//x * logn for x in a)  -- 近似于稀疏极限枚举 [1,1,1, 100000] 则是 skew 情况
    # ~ n * logn * logn


n, a = RI(), RILIST()
print(solve(n, a))