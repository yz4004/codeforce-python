"""
https://codeforces.com/problemset/problem/1982/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n*m 之和 ≤2.5e5。
每组数据输入 n m(1≤n,m≤500) k(1≤k≤min(n,m))
然后输入 n 行 m 列的矩阵 a，元素范围 [0,1e9]。
然后输入 n 行 m 列的 0-1 矩阵，表示 a 中每个元素的类型是 0 还是 1。

每次操作，你可以选择 a 的一个 k*k 的子矩阵，把其中所有元素增加任意整数（可以是负数）。

能否让所有类型 0 的元素之和等于所有类型 1 的元素之和？
输出 YES 或 NO。
"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
from math import inf, gcd

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(m,n,k,a,b):
    # k*k
    s0 = s1 = 0
    for i in range(m):
        row_a, row_b = a[i], b[i]
        for x,t in zip(row_a, row_b):
            if t == 0:
                s0 += x
            else:
                s1 += x
    gap = abs(s1 - s0)

    if gap == 0:
        return "YES"

    #print(s0,s1, gap, b)

    # 0 -> 1
    pre = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            pre[i+1][j+1] = pre[i+1][j] + pre[i][j+1] - pre[i][j] + b[i][j]

    # i,i+k-1
    # i+k-1 = m-1
    k2 = k * k
    g = -1
    for i in range(0, m-k+1):
        for j in range(0, n-k+1):
            # (i,j) * (i+k-1,j+k-1)
            one = pre[i+k][j+k] + pre[i][j] - pre[i+k][j] - pre[i][j+k]
            zero = k2 - one
            d = one - zero

            if d != 0:
                d = abs(d)
                g = d if g == -1 else gcd(g, d)
                #print(gap, d, g)

    # d1...dk
    # gap
    # print(gap, g)

    # d1*a1 + ... + dk*ak = gap
    return "YES" if g != -1 and gap % g == 0 else "NO"




for _ in range(RI()):

    n,m,k = RII()
    # n*m a (0-1e9)
    # n*m b (0-1)
    a = [RILIST() for _ in range(n)]
    b = [list(map(int, RS())) for _ in range(n)]

    print(solve(n,m,k, a, b))