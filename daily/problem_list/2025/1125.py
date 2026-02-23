"""
https://codeforces.com/problemset/problem/2160/C

输入 T(≤1e4) 表示 T 组数据。
每组数据输入 n(0≤n<2^30)。

是否存在一个正整数 x，使得 x XOR rev(x) = n？
其中 rev(x) 表示翻转 x 的二进制（不含前导零）后的整数。例如 rev(1101) = 1011。
输出 YES 或 NO。

进阶：做到 O(1) 时间。
"""
import itertools
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


def solve(n):
    lb = n & -n
    if lb > 1:
        n1 = n >> lb.bit_length() - 1
        s = bin(n1)[2:]
    else:
        s = bin(n)[2:]

    if s != s[::-1]:
        return "NO"

    m = len(s)
    if m % 2 and s[m//2] == "1":
        return "NO"

    return "YES"

for _ in range(RI()):
    n = RI()
    print(solve(n))
