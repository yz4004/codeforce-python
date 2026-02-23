"""
https://codeforces.com/problemset/problem/1670/F

输入 n(1≤n≤1e3) l r(1≤l≤r≤1e18) 和 z(1≤z≤1e18)。

输出有多少个长为 n 的非负整数数组 a，满足 l ≤ sum(a) ≤ r 且 xor(a) = z，即 a 中所有元素的异或和等于 z。
答案模 1e9+7。

a = [...]  >= 0
l <= sum(a) <= r

xor(a) = z

z所有1位置都至少有一次贡献，去除掉base后剩余部分都成对出现，可以自由分配
"""
from collections import defaultdict
from functools import cache
from math import comb, factorial, inf
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, l, r, z = RII()

MOD = mod = 1_000_000_007
MX = 1001
fac = [0] * (MX+1)  # f[i] = i!
fac[0] = 1
for i in range(1, MX+1):
    fac[i] = fac[i - 1] * i % MOD
inv_fac = [0] * (MX+1) # inv_fac[i] = i!^-1  i的阶乘在模p=10**9+7下的乘法逆元
inv_fac[-1] = pow(fac[-1], MOD-2, MOD) # pow(fac[-1], -1, MOD) 等价写法
for i in range(MX-1, -1, -1):
    inv_fac[i] = inv_fac[i+1] * (i+1) % MOD
def comb(n,k):
    return fac[n] * inv_fac[k] * inv_fac[n-k] % mod


def solve(n, l, r, z):
    if z > r:
        return 0

    m = max(r, l - 1, z).bit_length()
    def check(bound):
        # m = bound.bit_length()
        if bound == 0:
            return 0
        @cache
        def f(i, bound, carry, is_great):
            if i == m:
                return 1 if carry == 0 and not is_great else 0

            lo = z >> i & 1
            res = 0
            for j in range(lo, n+1, 2):
                c = (carry + j) >> 1
                cur_bit = (carry + j) & 1
                new_great = (cur_bit > (bound >> i & 1)) or (cur_bit == (bound >> i & 1) and is_great)
                #print((i, bound, carry,is_great), j, lo, new_great)
                res += f(i+1, bound, c, new_great) * comb(n, j)
            return res % mod
        return f(0,bound, 0, False)
    hi = check(r)
    lo = check(l-1)
    return (hi - lo + mod) % mod
print(solve(n, l, r, z))




    # 考虑整数的二进制表示
    # 满足xor和 = z
    # 总和 [l,r]
    # @cache
    # def f(i, carry, r, tight_r, is_limit, s):
    #     # 从左往右 从高到低枚举 i对应bit位 m-1 ... 0 -1
    #     # carry -- 当前后缀 [i,0] 需要向上提供的进位
    #     if i == -1:
    #         if carry == 0:
    #             print("-"*100, s)
    #         return 1 if carry == 0 else 0
    #
    #     res = 0
    #     lo = z >> i & 1
    #     # 2. r上界，如果前缀被支配 is_limit 则当前枚举最后拥有的 1 在扣除要仅供的carry后 收到 r >> i & 1 支配
    #     up = n if not is_limit else tight_r + (r >> i + 1)
    #
    #     tmp = []
    #     base = lo + carry * 2
    #
    #
    #     # [当前位置最终拥有的1] = 他应该是 [当前数组在这位填入k个1 受z支配奇偶] + [低位传来的carry] - [向上的进位]
    #     for j in range(base, up + 1):
    #
    #         # 枚举 [当前数组在这位填入k个1 受z支配奇偶] + [低位传来的carry]
    #         for k in range(lo, j+1, 2):
    #             c = j - k  # [低位传来的carry]
    #             tmp.append((j,k,c))
    #             if c >= 0:
    #                 res += f(i - 1, c, r, is_limit and j == tight_r, s + str(k)) * comb(n, k)
    #     return res



