"""
https://codeforces.com/problemset/problem/2121/F

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) s(-2e14≤s≤2e14) x(-1e9≤x≤1e9) 和长为 n 的数组 a(-1e9≤a[i]≤-1e9)。

输出 a 有多少个非空连续子数组 b，满足 sum(b) = s 且 max(b) = x。
"""
import sys
from math import inf
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, s, x = RII()
    nums = RILIST()
    res = 0

    ps = 0
    m, mi = -inf, -1
    pre1 = defaultdict(int)
    pre2 = defaultdict(int)
    pre1[0] = 1

    for i in range(n):
        # 在维护前缀和cnt的基础上考虑m
        # 遇到大于m的数 则此刻前缀信息应清空 （这一刻ps要计入，因为pre[ps] 此时包含大于m的数 不会被算进后面截取的子数组
        # 遇到m=x后 可考虑统计前缀，但必须考虑最近的x左侧统计的 ps[t] 固需要维护最近x的坐标
        # 可以记住坐标+二分 但其实计数也可以做 数组经过划分后 注意我们依赖哪块的信息，再加一个哈希表暂存
        ps += nums[i]
        if nums[i] > x:
            m = -inf
            mi = -1
            pre1 = defaultdict(int)
            pre2 = defaultdict(int)
            pre1[ps] = 1
            continue

        if nums[i] == x:
            for p,c in pre2.items():
                pre1[p] += c
            pre2.clear()

            mi = i
            m = x

        if m == x:
            # j = bisect.bisect_left(pre[ps - s], mi) - 1  # mi左侧的所有 pre[ps-s] 有j+1个
            # res += j + 1
            res += pre1[ps - s]
            pre2[ps] += 1
        else:
            pre1[ps] += 1
        # pre[ps].append(i)
    print(res)
