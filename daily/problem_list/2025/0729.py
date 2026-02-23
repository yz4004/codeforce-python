"""
https://codeforces.com/problemset/problem/2057/C

输入 T(≤1e4) 表示 T 组数据。
每组数据输入 L R，范围 0 到 2^30 - 1，且 R-L > 1。

从 [L,R] 中找三个不同的整数 a,b,c，最大化 (a XOR b) + (b XOR c) + (a XOR c)。
输出 a,b,c。多解输出任意解。

1..
1..



在利用高斯消元求线性基的过程中，比如最高位我消去了其他人的最高位，但这为什么能反映出最大xor

"""

import sys


RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    L, R = RII()

    # 1...
    #    1...

    # 考虑R的最高位

    # 10001
    # 10000  - 当他不是底时，
    # 01111

    # 10000
    # 01111
    # 01110

    t = L ^ R
    hi = 1 << (t.bit_length()-1)
    base = (-1 ^ (hi - 1)) & L

    t = R - base

    #print(L, R, bin(base), base,t,  hi)

    # hi += base

    # print((hi + 1) & hi & (hi - 1))
    # s = (hi + 1,  hi, hi - 1)
    # print(s[0] ^ s[1] + s[1] ^ s[2] + s[2] ^ s[0])


    if hi < t:
        s = (hi + 1,  hi, hi - 1)
    else:
        s = (hi,  hi - 1, hi - 2)

    print(" ".join(map(str, [x + base for x in s])))




