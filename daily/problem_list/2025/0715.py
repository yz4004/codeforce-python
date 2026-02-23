"""
https://codeforces.com/problemset/problem/2106/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) m(1≤m≤n) 和长为 n 的数组 a(1≤a[i]≤1e9)，长为 m 的数组 b(1≤b[i]≤1e9)。

你可以往 a 中的任意位置插入一个整数 k，也可以不插入。
能否让 a 有一个长为 m 的子序列 c，满足 c[i] >= b[i]？（注：子序列不一定连续）

如果无法做到，输出 -1。
如果可以不插入整数，输出 0。
否则输出 k 的最小值。
"""
import sys
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, m = RII()
    a, b = RILIST(), RILIST()

    suf = [0]*(n+1)
    j = m-1
    for i in range(n-1,-1,-1):
        if j >= 0 and a[i] >= b[j]:
            j -= 1
            suf[i] = suf[i+1] + 1
        else:
            suf[i] = suf[i+1]
    if suf[0] == m:
        print(0)
        continue
    #print(suf)

    j = 0
    k = inf
    for i in range(n):
        if j + 1 + suf[i] >= m:
            k = mn(k, b[j])

        if a[i] >= b[j]:
            j += 1
            if j + 1 + suf[i+1] >= m:
                k = mn(k, b[j])
        # else:
        #     if j + 1 + suf[i] >= m:
        #         k = mn(k, b[j])

    if j+1 >= m:
        k = mn(k, b[j])
    print(k if k < inf else -1)

