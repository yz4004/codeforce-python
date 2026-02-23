"""
https://codeforces.com/problemset/problem/2145/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) 和一个长为 n 的字符串，只包含 'a' 和 'b'。

从 s 中删除一个连续子串 t（可以为空），使得剩余字符串的 a 和 b 的个数相等。

输出 t 的最短长度。
如果必须把整个 s 删除，输出 -1。

进阶：如果 s 包含前三种字母呢？
"""
import itertools
import sys
from collections import defaultdict
from functools import cache
from math import inf
from operator import add, xor
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, s = RI(), RS()

    def solve(n, s):
        ps = [0]*(n+1)
        for i,ch in enumerate(s):
            ps[i+1] = ps[i] + (1 if ch == "b" else -1)
        s = ps[-1]

        if s == 0:
            return 0

        res = n
        pre = {0:-1}
        for i in range(n):
            t = ps[i+1]
            if t-s in pre and i-pre[t-s] < res:
                res = i-pre[t-s]
            pre[t] = i

        return -1 if res == n else res
    print(solve(n, s))





