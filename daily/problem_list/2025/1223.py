"""
复习。温故而知新。

https://codeforces.com/problemset/problem/1822/E

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的字符串 s，只包含小写字母。

如果对于每个 0 到 n-1 的下标 i，都满足 s[i] != s[n-1-i]，那么称 s 为反回文串。

每次操作，你可以交换 s 中的任意两个字母。
最少操作多少次，可以使 s 是反回文串？

输出最小操作次数。如果无法做到，输出 -1。

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

def solve(n, s):
    # i 的对称位置 n-1-i
    # 如果和对称位置相等 则需交换
    # 奇数长度中间永远和自己对称 换不了
    if n%2:
        return -1

    # 1 2 3 3 2 1
    # 1 2 3
    # 对称位置其实可以翻转过来 则问题变成lc3785
    # 同值尽量放一边 在回文语义下很直观 因为无分左右半 而且不消耗交换次数
    # 则无解条件是一类值超过一般长度 则必然有对称点

    # 最小交换
    # 交换等价于 每次减去两个不同值的数
    # 在所有冲突对中 内部消化. 如果可以 则等于 (c+1)//2
    # 1 2
    # 1 2
    # 如果不可以 即某个众数超过剩余人，则再找外部

    conflict = defaultdict(int)
    cnt = defaultdict(int)
    total = 0
    for i in range(n//2):
        a, b = s[i], s[n-1-i]
        if a == b:
            conflict[a] += 1
            total += 1
        cnt[a] += 1
        cnt[b] += 1

    if max(cnt.values()) > n//2:
        return -1

    m = max(conflict.values(), default=0)
    return max(m, (total+1)//2)

for _ in range(RI()):
    n, s = RI(), RS()
    print(solve(n, s))





