"""
https://codeforces.com/contest/2039/problem/C2

输入 T(≤1e4) 表示 T 组数据。所有数据的 x 之和 ≤1e7。
每组数据输入 x(1≤x≤1e6) 和 m(1≤m≤1e18)。

输出有多少个在 [1,m] 中的 y，满足 x XOR y 能被 x 或者 y 整除（也可以同时被 x 和 y 整除）。

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
    x, m = RII()

    # x^y = k*x or k*y

    # 对于大的那个人（假设高位不一样）他肯定不是除数，否则k*max(x,y) 最高位一定大于 x^y 最高位
    # 当 y < x 可以暴力 1e6
    # 当 y > x
    # x^y = k*x
    # y = (k*x) ^ x 对一任意k=1 2 ... 只要y不超过m 都是合法的 （反过来可以得到k）
    # x 只能通过 xor 控制低位，高位小于m的高位则没有问题，如果恰好等于m的高位，则x对应的xor部分不能超过

    k = x.bit_length()

    # (m >> k)  高位取 1 ... (m>>k)-1 都不受任何限制 低位任意取 0- (1<<k)-1

    # ((m>>k) - 1) * (1<<k)





