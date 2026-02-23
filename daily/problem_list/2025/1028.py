"""
https://codeforces.com/problemset/problem/1845/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 |s| 之和 ≤3e5。
每组数据输入一个只包含 0~9 的字符串 s(1≤|s|≤3e5)，
然后输入 m(1≤m≤10) 和两个长为 m 的只包含 0~9 的字符串 L 和 R，保证 L[i]≤R[i]。

是否存在长为 m 的，只包含 0~9 的字符串 t，满足 L[i]≤t[i]≤R[i] 且 t 不是 s 的子序列？
输出 YES 或 NO。
注：子序列不一定连续。

"""
import itertools
import sys
from functools import cache
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
    s = list(map(int, RS()))
    m = RI()
    L, R = list(map(int, RS())), list(map(int, RS()))

    def solve(s, m, L, R):
        # 0-9
        n = len(s)

        last = [n]*10
        nxt = [[n]*10 for _ in range(n+1)] # nxt[i][d] [i:] 最近的d的位置 不算i本身

        for i in range(n-1, -1, -1):
            x = s[i]
            last[x] = i
            for d in range(10):
                nxt[i][d] = last[d]


        j = 0
        for i, (l,r) in enumerate(zip(L,R)):
            t = -1
            for d in range(l,r+1):
                if t < nxt[j][d]:
                    t = nxt[j][d]
            if t == n:
                return "YES"
            j = t+1

        return "NO"
    print(solve(s, m, L, R))




