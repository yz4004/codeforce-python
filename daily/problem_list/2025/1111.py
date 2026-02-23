"""
https://codeforces.com/problemset/problem/1857/E

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 x(1≤x[i]≤1e9)。

一维数轴上有 n 个点，第 i 个点的坐标为 x[i]。
你从这 n 个点中选了一个点 p，然后连接 p 和每个 x[i]，可以得到 n 条线段。
线段 [L,R] 覆盖整点 L,L+1,...,R。
定义 f(a) 为坐标为 a 的点被覆盖的次数。
定义 g(p) = f(1) + f(2) + ... + f(1e9)。

输出 g(x[1]), g(x[2]), ..., g(x[n])。

x1 ... xi ... xn

[xi, xi]
...
[xi, xj]
...
[xi. xn]
区间 (xi, xi+1] 被覆盖 n-i ... n-i-1 ... 1

----------------------------------------
1 10 100 1000

(1,10]
(1,100]
(1,1000]
9+99+999+4

[1,10]
[10,100]
[10,1000]
9+90+990+1

[1,100]
[10,100]
[100,1000]
x-li+1 + ... x-lj+1


[li, x] [x, ri]


1 10 100 1000
[1,1000)
[10,1000)
[100,1000)
999+990+900+4

"""
import itertools
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, a = RI(), RILIST()

    sr = sum(a)
    a = sorted([(x,i) for i,x in enumerate(a)])
    res = [0]*n
    sl = 0
    for j, (x,i) in enumerate(a):
        sr -= x
        cl, cr = j, n-j-1
        res[i] = (x*cl - sl + cl) + (sr - x*cr + cr) + 1
        sl += x
    print(" ".join(map(str, res)))