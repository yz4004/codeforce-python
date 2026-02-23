"""
https://codeforces.com/problemset/problem/1999/F

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n k(1≤k≤n≤2e5) 和长为 n 的只包含 0 和 1 的数组 a。
保证 k 是奇数。

对于 a 的每个长为 k 的子序列 b，计算 b 的中位数。
所有中位数的和是多少？
答案模 1e9+7。
注：子序列不一定连续。

1 0 0 1 -- 3
001 * 2
011 * 2

"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
from math import inf, gcd, comb

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

MX = 200_000+1
fac = [0]*MX
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i-1] * i % MOD

inv_fac = [0]*MX
inv_fac[MX-1] = pow(fac[MX-1], -1, MOD) #求fac[mx-1]在mod下的乘法逆元
def extgcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = extgcd(b, a % b)
    return d, y, x - (a // b) *y
# inv_fac[MX-1] = extgcd(fac[MX-1], MOD)[1] #等价写法

for i in range(MX-1, 0, -1): # 0 / -1
    inv_fac[i-1] = inv_fac[i] * i % MOD
def comb(n, m):
    # c(m, n)  or (n, m)  n! / (n-m)! m!
    if m > n or m < 0: return 0

    return fac[n] * inv_fac[n-m] * inv_fac[m] % MOD

for _ in range(RI()):
    n, k = RII()
    a = RILIST()

    c1 = sum(a)
    c0 = n - c1

    # c0 c1

    d = k//2

    # c1 = d+1
    if c1 < d+1:
        print(0)
    else:
        # comb(c1, d+1) + ... comb(c1, k)

        # c0 c1

        # c1 - 至少提供d+1个
        # c0 -
        res = 0
        # s0 = comb(c0, d+1) % MOD
        # s1 = comb(c1, d) % MOD

        # comb(n, k+1) = n! // (k+1)! (n-k-1)!
        # comb(n,k)    = n! // k! (n-k)!

        # comb(n, k+1) = comb(n, k) * (n-k)//(k+1)

        for i in range(d+1, mn(c1, k)+1):

            res += comb(c0, k-i) * comb(c1, i)
            # res += s0 * s1
        print(res % MOD)

        #
        # print(comb(n,k) % MOD)
        # print((c1,d+1),  comb(c1, d+1))
        # print((comb(n-(d+1), d) * comb(c1, d+1))% MOD)
        # comb(n, k1+k2) = comb(n, k1) * comb(n - k1, k2)
