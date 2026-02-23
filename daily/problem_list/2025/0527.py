"""
https://codeforces.com/problemset/problem/1133/D

输入 n(1≤n≤2e5) 和两个长为 n 的数组 a b，元素范围 [-1e9,1e9]。

选择一个实数 d，计算数组 c，其中 c[i] = d * a[i] + b[i]。
问：c 中最多有多少个元素等于 0？

d = - b[i] / a[i]

"""
# print(4 ** 15)
# print(1 << 30)
# x << k = x * (2^k)

from collections import defaultdict
from math import gcd
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n = RI()
a, b = RILIST(), RILIST()

cnt = defaultdict(int)
res = sum(y == 0 for y in b) # 取d=0 则只靠b里的0
zeros = 0
for x,y in zip(a,b):
    if x != 0:
        g = gcd(x,y)
        x, y = x//g, y//g
        if x < 0:
            x, y = -x, -y
        cnt[(x,y)] += 1
    elif x == 0 and y == 0:
        zeros += 1
print(mx(res, max(cnt.values(), default=0) + zeros))
