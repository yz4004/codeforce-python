"""
https://codeforces.com/problemset/problem/1921/F

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤1e5，q 之和 ≤2e5。
每组数据输入 n(1≤n≤1e5) q(1≤q≤2e5) 和长为 n 的数组 a(-1e8≤a[i]≤1e8)。
然后输入 q 个询问，每个询问输入 L d k，满足 1≤L,d,k≤n 且 L+(k-1)*d≤n。
输出 a[L]*1 + a[L+d]*2 + a[L+2d]*3 + ... + a[L+(k-1)*d]*k。
"""
import itertools
import sys
from math import isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, Q = RII()
    a = RILIST()

    B = isqrt(n) #mn(isqrt(n), 300)

    small = [None]*B
    for d in range(1, B):
        # d 2d ... kd, r in [0,d)
        m = (n-1)//d + 1
        ps = [None]*(m+1)
        for l in range(d):
            # l+d l+2d ...
            p0 = list(itertools.accumulate(a[l::d], initial=0))
            # l+d*i < n
            # d*i < n-l
            p1 = list(itertools.accumulate([a[l+d*i] * (i+1) for i in range(0, (n-l-1)//d+1)], initial=0))

            ps[l] = (p0, p1)

        small[d] = ps

    res = []
    for _ in range(Q):
        L, d, k = RII()
        L -= 1
        if d >= B:
            res.append(sum(a[L+d*(i-1)] * i for i in range(1, k+1)))
        else:
            l = L % d

            offset = L // d
            l0, r0 = offset, offset + k - 1

            # [l0, r0]
            p0, p1 = small[d][l]

            tmp0 = p0[r0+1] - p0[l0]
            tmp1 = p1[r0+1] - p1[l0]
            res.append(tmp1 - tmp0 * offset)
    print(" ".join(map(str, res)))



