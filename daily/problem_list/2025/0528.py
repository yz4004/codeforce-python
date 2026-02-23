"""
https://codeforces.com/problemset/problem/2086/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 c[i] 之和 ≤5e5。
每组数据输入长为 26 的数组 c(0≤c[i]≤5e5)，保证 sum(c)>0。

计算满足如下全部要求的字符串 s 的数量：
1. 长为 sum(c)。
2. 第 i 种小写字母出现 c[i] 次。
3. 对于满足 s[i]=s[j] 的 i 和 j，下标之差 |i-j| 必须是偶数。
答案模 998244353。

"""
from math import comb, factorial
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

mod = 998244353
N = 5 * 10 ** 5 + 1
fac = [0] * (N+1)  # f[i] = i!
fac[0] = 1
for i in range(1, N+1):
    fac[i] = fac[i - 1] * i % mod
inv_fac = [0] * (N+1) # inv_fac[i] = i!^-1  i的阶乘在模p=10**9+7下的乘法逆元
inv_fac[-1] = pow(fac[-1], mod-2, mod) # pow(fac[-1], -1, mod) 等价写法
for i in range(N-1, -1, -1):
    inv_fac[i] = inv_fac[i+1] * (i+1) % mod

def comb(n, k):
    if n<0 or k < 0 or n < k: return 0
    # n! / k! (n-k)!
    return fac[n] * inv_fac[k] * inv_fac[n-k] % mod

def solve(nums):
    m = sum(nums)
    # m//2, (m+1)//2
    m1, m2 = (m+1)//2, m//2
    # 背包1恰好填入x个，剩余偶数cnt部分去第二个背包，若可以放下
    # o = sum(x == 1 for x in nums)
    # nums = [x for x in nums if x > 1]
    # f = [0]*(m1+1) # 只考虑 i
    # f[0] = 1
    # for x in nums:
    #     for i in range(m1, x-1, -1):
    #         f[i] = f[i-x] * comb(m1 - (i-x), x) % mod
    #
    # res = 0
    # for i in range(0, o+1): # i个在第一组里, (o-i) 在第二组里
    #     res += f[m1 - i] * f[m2 - (o - i)] % mod
    #     res %= mod
    # res *= factorial(o)
    # return res % mod

    f = [0]*(m1+1) # 只考虑 i
    f[0] = 1
    s = 0
    nums = [x for x in nums if x > 0]
    for x in nums:
        s += x
        # for i in range(m1, x-1, -1):
        for i in range(m1, -1, -1):
            # x放在m1里 -- m1现在有i个      i = x + (i-x)
            # x放进m2里 -- m2现在有s-i个  s-i = x + (s-i-x)

            # f[i] = (f[i-x] * comb(m1 - (i-x), x) % mod  # i-x个已经在m1里就位，剩余 m1-(i-x) 里选x个位置
            #         + f[i] * comb(m2 - (s-i-x), x) % mod) # s-i-x个已经在m2里就位，剩余 m2-(s-i-x) 里选x个位置
            # f[i] %= mod

            way1 = way2 = 0
            if i - x >= 0:
                way1 = f[i-x] * comb(m1 - (i-x), x) % mod

            if m2 >= (s-i-x):
                way2 = f[i] * comb(m2 - (s-i-x), x) % mod

            f[i] = (way1 + way2) % mod

    return f[-1]


T = RI()
for _ in range(T):
    a = RILIST()
    print(solve(a))
