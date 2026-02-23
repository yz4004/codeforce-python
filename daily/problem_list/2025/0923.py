"""
https://codeforces.com/problemset/problem/1996/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤1e6，x 之和 ≤1e6。
每组数据输入 n(1≤n≤1e6) 和 x(1≤x≤1e6)。

输出有多少个三元组 (a,b,c) 满足
1. a,b,c 均为正整数。
2. ab+ac+bc ≤ n。
3. a+b+c ≤ x。

注意 (1,1,2) 和 (1,2,1) 是不同的三元组。

不等式 + 观察枚举上限 + 调和级数枚举
"""
import sys
from bisect import bisect_left, bisect_right
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(n, x):
    # 123...n

    # 固定a -- a*b + a*c + b*c  = (b+a)*(c+a) - a^2 <= n^2

    # (b+a) * (c+a) <= n + a^2
    # (b+a) + (c+a) <= x + a

    # x * y <= t1
    # x + y <= t2

    # y <= mn(t1/x, t2-x) 固定x 则只关心上界下取整，需要枚举一次x [a,)

    # 除数分块可以对 [t1/x] 按相同值分块 只需要不超过 sqrt(t1) 个段数

    # c <= mn((n - ab) / (a+b), x - (a+b))

    # 1. ab是对称的，可以只枚举一半+单算a=b
    # 2. 注意随着ab的增加 分子 a+b 会使得 .../(a+b), x-(a+b) = 0.
    # 其实类似调和级数的上界约束，即使剪枝就是调和枚举 不会n^2

    # a=b
    # mn((n - a^2) / 2*a, x - 2*a)

    # res = 0
    # for a in range(1, n+1):
    #     for b in range(1, n+1):
    #         c = mn((n-a*b)//(a+b), x - (a+b))
    #         if c > 0:
    #             res += c

    res = 0
    for a in range(1,n+1):
        t = mn((n - a * a) // (2*a), x - 2*a)
        if t > 0:
            res += t

        if t <= 0: break

        for b in range(a+1, n+1):
            c = mn((n-a*b)//(a+b), x - (a+b))

            if c <= 0:
                break
            res += c * 2
    return res

for _ in range(RI()):
    n, x = RII()
    print(solve(n, x))
