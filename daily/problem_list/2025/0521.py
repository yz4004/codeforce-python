"""
https://codeforces.com/problemset/problem/1884/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤1e5) m(1≤m≤1e9) 和 n 个闭区间 (1≤l≤r≤m)。

你有一个长为 m 的全 0 数组 a。
从输入的 n 个区间中，选择一些区间（每个区间至多选一次），执行区间 +1 操作。

输出 max(a) - min(a) 的最大值。

"""
import heapq
import sys, random
from collections import defaultdict, deque
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


def solve(m, intervals):
    # 长度为n=1e9的数组 从intervals里选一些区间 执行一些区间+1操作
    # 遍历到某个点，考虑有多少可行区间覆盖他，则是该点处的最大的叠加值
    # 选择这些所有的区间
    # 最小区间叠加发生在
    # - 考虑这些区间有多少右侧覆盖到m
    # - 考虑这些区间有多少左侧覆盖到1

    res = 0
    q = []
    intervals.sort() 
    cnt1 = 0
    cntm = 0
    for x,y in intervals:
        if x == 1:
            cnt1 += 1
        if y == m:
            cntm += 1

        while q and q[0][0] < x:
            b,a = heapq.heappop(q)
            if a == 1:
                cnt1 -= 1
        heapq.heappush(q, (y,x))

        mx_cover = len(q)
        mn_cover = mn(cnt1, cntm)
        res = mx(res, mx_cover - mn_cover)
    return  res

    # for x,y in intervals:
    #     pts[x] += 1
    #     pts[y+1] -= 1
    # pts = sorted([(x,v) for x,v in pts.items()])
    # v = 0
    # mn_cov = 0 if pts[0][0] > 1 or pts[-1][0] <= n else inf
    # mx_cov = 0
    # for i, t in pts:
    #     v += t
    #     if i <= n: mn_cov = mn(mn_cov, v)
    #     mx_cov = mx(mx_cov, v)
    # return mx_cov - mn_cov

T = RI()
for _ in range(T):
    n, m = RII()
    intervals = []
    for _ in range(n):
        x,y = RII()
        intervals.append((x,y))
    print(solve(m, intervals))
