"""
https://codeforces.com/problemset/problem/2114/F

输入 T(≤1e4) 表示 T 组数据。所有数据的 x 之和 ≤1e8，y 之和 ≤1e8。
每组数据输入 x y k (1≤x,y,k≤1e6)。

每次操作，你可以选择一个 [1,k] 中的整数 a，把 x 乘以 a，或者（在 x 能被 a 整除的前提下）把 x 除以 a。

输出把 x 变成 y 的最小操作次数。
如果无法做到，输出 -1。

x * a1 / a2 * a3 ... = y
相当于从[1,k]选两个独立子集，分别赋予x,y 使得乘积相等.
    x * a1 * ... ak = y * b1 ... bj
类似背包的子集枚举思路


提示：从整除性质思考
x -> y
    乘法变换，总会经过y的因数，然后乘就行了.
    如果 x | y, 则目标是构造出因数 d = y/x
    不整除则可以通过构造gcd/lcm 中转
    lcm * gcd = x*y

    x -> gcd(x,y) -> y
    先除再乘，其实站在gcd视角都是乘

x 如何分解成 [1,k] 的因数乘积， x,y,k < 1e6
x = a1 * a2 ... aj



"""

import sys
from collections import defaultdict
from math import gcd, inf, isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

N = int(1e6)
# facs = [[] for _ in range(N+1)]
# # 调和级数枚举 1, 2 ... d ... 作为因数去枚举
# for d in range(2, N+1):
#     for n in range(d, N+1, d):0.2
#         facs[n].append(d)

# spf = list(range(N+1))
# for p in range(2, isqrt(N)+1):
#     if spf[p] == p:
#         for m in range(p*p, N+1, p):
#             if spf[m] == m:
#                 spf[m] = p

def solve(x, k) -> int:
    # fac = []
    # for i in range(2, k+1):
    #     if x % i == 0:
    #         fac.append(i)

    #fac = facs[x]

    # # 1. 质因数分解 + 生成因子列表
    # fac = defaultdict(int)
    # t = x
    # while t > 1:
    #     p = spf[t]
    #     fac[p] += 1
    #     t //= p
    # #print(x, spf[t], fac)
    #
    # items = list(fac.items())
    # def dfs(idx):
    #     if idx == len(items):
    #         return [1]
    #     p, exp = items[idx]
    #     sub_divs = dfs(idx + 1)   # 后面部分的约数
    #     res = []
    #     # 对每一个后面部分的约数 d，乘上 p^0, p^1, …, p^exp
    #     val = 1
    #     for e in range(exp + 1):
    #         for d in sub_divs:
    #             res.append(d * val)
    #         val *= p
    #     return res
    # fac = sorted(dfs(0))
    #print(fac)

    # fac =[]
    # for d in range(2, isqrt(N)+1):
    #     if x % d == 0:
    #         fac.append(d)
    #         if d * d < x:
    #             fac.append(x//d)
    # fac.sort()

    # f = [inf]*(x+1)
    # f[1] = 0
    # for i in range(2, x+1):
    #     for d in fac:
    #         if d > i or d > k: break
    #         if i % d == 0:
    #             f[i] = mn(f[i], f[i//d] + 1)
    # return f[x]

    #
    fac = []
    for d in range(1, isqrt(N)+1):
        if x % d == 0:
            fac.append(d)
            if d * d < x:
                fac.append(x//d)
    fac.sort()

    posi = {x:i for i,x in enumerate(fac)}

    m = len(fac)
    f = [inf] * m
    f[0] = 0
    for i in range(1, m):
        # 因数 fac[i-1]
        # for j in range(1, i):
        #     if fac[i] % fac[j] == 0 and fac[j] <= k:
        #         pre = fac[i]//fac[j]
        #         f[i] = mn(f[i], f[posi[pre]] + 1)

        for j in range(0, i):
            if fac[i] % fac[j] == 0:
                a = fac[i] // fac[j]
                if a <= k:
                    f[i] = min(f[i], f[j] + 1)
    return f[posi[x]] if x in posi else inf


for _ in range(RI()):
    x, y, k = RII()
    d = gcd(x,y)
    # [1,m]

    # x/d, y/d 按照 [1,k] 因子分解的最少因子次数
    # 1. 得到 x/d 在 [1,k] 的因子数
    # 2. 线性dp
    a,b = x//d, y//d
    #print(x,y,k, "-", d, a,b)
    res = solve(a,k) + solve(b,k)
    print(res if res < inf else -1)









