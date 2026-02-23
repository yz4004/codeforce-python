"""
https://codeforces.com/problemset/problem/1279/B

输入 T(≤100) 表示 T 组数据。所有数据的 n 之和 ≤1e5。
每组数据输入 n(1≤n≤1e5) s(1≤s≤1e9) 和长为 n 的数组 a(1≤a[i]≤1e9)。

你在找一个 a 的最长前缀，满足其元素和 <= s。
你可以删除前缀中的一个数。

输出你删除的元素的下标。下标从 1 开始。
特别地，如果 sum(a) <= s，输出 0。

"""
import itertools
import sys
from functools import cache

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, s = RII()
    a = RILIST()

    delete = False
    m = -1
    idx = -1
    for i,x in enumerate(a):
        if not delete and m < x:
            idx = i
            m = x

        s -= x
        if s < 0:
            if not delete:
                delete = True
                s += m
                print(idx+1)
                break
            else:
                pass

    if not delete:
        print("0")
