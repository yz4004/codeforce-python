"""
https://codeforces.com/problemset/problem/1999/E

输入 T(≤1e4) 表示 T 组数据。
每组数据输入 L R(1≤L<R≤2e5)。

黑板上写有 L,L+1,...,R 一共 R-L+1 个整数。
每次操作，选择两个数字 x 和 y 擦掉，然后在黑板上写下 3x 和 floor(y/3)。

输出使黑板上的数字全为 0 的最小操作次数。可以证明，这总是可能的。

1 2 3

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    L, R = RII()


    # 2*d0 + [L+1,R]
    # d0 + [L,R]

    d0 = 0
    t = 1
    while t <= L:
        t *= 3
        d0 += 1

    # L-1] [L,R]

    # 1010101

    def check(u):
        if u == 0: return 0
        t = 1
        d = 1
        res = 0
        while t * 3 <= u:
            # [t, t*3) ... [1,3) [3,9)
            # 1 3 9 27
            # 1 2 3 4
            res += (t*3 - t) * d
            t *= 3
            d += 1
        # t] [t+1, u]
        tail = (u-t+1) * d if t <= u else 0
        return res + tail
    #print(d0, (L,R), check(L-1), check(R))
    print(check(R) - check(L-1) + d0)
