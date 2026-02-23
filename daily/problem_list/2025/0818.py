"""
https://codeforces.com/problemset/problem/1207/F

一开始，你有一个长为 N=5e5 的数组 a，初始值全为 0。
输入 q(1≤n≤5e5) 和 q 个询问，格式如下：
"1 x y"：把 a[x] 增加 y。其中 1≤x≤N，-1e3≤y≤1e3。
"2 x y"：对于 [1,N] 中满足 i%x = y 的下标 i，输出这些 a[i] 的和。其中 0≤y<x≤N。
"""
import sys
from math import isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


N = 500000
B = 256 # isqrt(N) + 1

a = [0] * (N + 1)
small = [ [0]*i for i in range(B) ]  # small[m][r] = sum of a[i] with i % m == r


out = []
append = out.append

for _ in range(RI()):
    t, x, y = RII()
    if t == 1:
        a[x] += y
        # update all small mod buckets
        for m in range(1, B):
            small[m][x % m] += y

    else:
        if x < B:
            append(str(small[x][y]))
        else:
            s = 0
            start = x if y == 0 else y
            for i in range(start, N + 1, x):
                s += a[i]
            append(str(s))

print('\n'.join(out))
