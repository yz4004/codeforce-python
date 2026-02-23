"""
https://codeforces.com/problemset/problem/134/B

输入 n(1≤n≤1e6)。

你从 (a,b) = (1,1) 出发。
从 (a,b) 可以一步移动到 (a+b,b) 或者 (a,a+b)。

输出从 (1,1) 移动到一个包含 n 的坐标的最小步数，即移动到 (n,i) 或者 (i,n)。


5,3
    2,3
    2,1
    1,1

1,1



"""
import itertools
import sys
from functools import cache
from operator import add, xor
from typing import List
from math import gcd, lcm

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x

n = RI()
res = n-1
for i in range(2, n):
    a,b = i,n
    t = 0
    valid = True
    while a > 1:
        if b % a == 0:
            valid = False
            break
        t += b//a
        a, b = b % a, a
    if valid:
        res = min_(res, t + b-1)
print(res)











