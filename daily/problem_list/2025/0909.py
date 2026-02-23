"""
https://codeforces.com/problemset/problem/2074/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 m 之和 ≤2e5。
每组数据输入 n m(1≤n≤m≤2e5)，长为 n 的数组 x(-1e9≤x[i]≤1e9)，长为 n 的数组 r(1≤r[i] 且 sum(r)=m)。

在平面直角坐标系上有 n 个圆，第 i 个圆的圆心在 (x[i],0)，半径为 r[i]。

输出有多少个整点在至少一个圆内或者圆边上。

"""
import sys
from collections import defaultdict
from math import inf, isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, m = RII()
    circles = zip(RILIST(), RILIST())

    # 枚举每个圆的纵割线，x -> y (x^2+y^2=r^2) 维护最高y
    covers = defaultdict(int)
    for x, r in circles:
        # d^2 + i^2 = r^2
        # d = isqrt(r*r - i*i)
        for i in range(x-r, x+r+1):
            d = isqrt(r * r - (x - i) * (x - i))
            covers[i] = mx(covers[i], d)

    print(sum(2*d+1 for d in covers.values()))


