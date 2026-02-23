"""
https://codeforces.com/problemset/problem/525/E

输入 n(1≤n≤25) k(0≤k≤n) S(1≤S≤1e16) 和长为 n 的数组 a(1≤a[i]≤1e9)。

从 a 中选一个子序列 b。（子序列不一定连续）
你可以把 b 中的至多 k 个数 x 变成 x!，即 x 的阶乘。每个数只能操作一次。

设 b 操作后变成 b'。
有多少个子序列 b 满足 sum(b') = S？

2^19 = 2^9 * 1000 = 512 * 1000
"""
import sys
from collections import defaultdict
from functools import cache
from math import factorial, inf
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7



n, limit, s = RII()
a = RILIST()
# 1,18

fac = [1]*19
for i in range(2, 19):
    fac[i] = fac[i-1] * i

m = 1
while m < 19 and fac[m] <= s:
    m += 1


# factorial(19) > 10 ** 16

# 2^25 - 32 * 10^7


def generate(nums):
    f = [defaultdict(int) for _ in range(limit+1)]
    f[0][0] = 1

    for x in nums:
        for i in range(limit, -1, -1):
            for k in sorted(f[i].keys(), reverse=True):
                f[i][k + x] += f[i][k]
                if i < limit and x < m and k + fac[x] <= s:
                    f[i+1][k + fac[x]] += f[i][k]
    return f

f1 = generate(a[:n//2])
f2 = generate(a[n//2:])

# print(f1)
# print(f2)

g1 = defaultdict(list)
g2 = defaultdict(list)

for i in range(limit+1):
    for k, cnt in f1[i].items():
        g1[k].append((i,cnt))

    for k, cnt in f2[i].items():
        g2[k].append((i,cnt))

for tmp in g1.values(): tmp.sort()
for tmp in g2.values(): tmp.sort()

# print(a[:n//2])
# print(g1)
#
# print(a[n//2:])
# print(g2)
res = 0
for x in sorted(g1.keys()):
    if s - x not in g2: continue
    # k,cnt ...
    tmp1 = g1[x]
    tmp2 = g2[s-x]

    pre_cnt = 0
    j = 0
    for k, cnt in tmp1[::-1]:
        while j < len(tmp2) and tmp2[j][0] + k <= limit:
            pre_cnt += tmp2[j][1]
            j += 1
        res += pre_cnt * cnt

print(res)




