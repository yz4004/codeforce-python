"""
https://codeforces.com/problemset/problem/799/C

输入 n(2≤n≤1e5) c d(0≤c,d≤1e5)。
然后输入 n 座喷泉的信息，每行输入 b p(1≤b,p≤1e5) 和字母 'C' 或者 'D'，分别表示喷泉的美丽值、买入价、需要支付的货币类型是金币还是钻石。

你有 c 枚金币和 d 枚钻石。
你需要购买恰好两座喷泉。

输出这两座喷泉的美丽值之和的最大值。
如果无法做到，输出 0。

双指针，前缀最大值
    三种情况，全从c/d取 各取一个
    在满足预算的情况下选最大美丽值，只选两个则定一议二，多个就只能0/1背包
    前缀最大值 - 二分
"""
import itertools
import sys
from bisect import bisect_left
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


n, c, d = RII()

cs = []
ds = []
for _ in range(n):
    b,p, type_ = sys.stdin.readline().strip().split()
    if type_ == "C":
        cs.append((int(p), int(b)))
    else:
        ds.append((int(p), int(b)))

cs.sort()
ds.sort()
def check(cs, c):
    res = 0

    m = len(cs)
    pre_max = [0]*(m+1)
    for i in range(m):
        pre_max[i+1] = max_(pre_max[i], cs[i][1])

    for p,b1 in cs:
        if p > c: break
        r = c - p # 如果选择当前p,b 剩余的预算

        i = bisect_left(cs, r+1, key=lambda x:x[0])-1
        b2 = pre_max[i+1]
        if b2:
            res = max_(res, b1+b2)

    return res, pre_max

res1, pre_max_c = check(cs, c)
res2, pre_max_d = check(ds, d)
res = max_(res1, res2)
# print(res1, res2)
if cs and ds:
    j = bisect_left(cs, c+1, key=lambda x:x[0])-1
    r1 = pre_max_c[j+1]

    j = bisect_left(ds, d+1, key=lambda x:x[0])-1
    r2 = pre_max_d[j+1]

    if r1 and r2:
        res = max_(res, r1+r2)
print(res)










