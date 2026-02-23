"""
https://codeforces.com/problemset/problem/1750/D

输入 T(≤100) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) m(1≤m≤1e9) 和长为 n 的数组 a(1≤a[i]≤m)。

计算有多少个长为 n 的数组 b，元素范围 [1,m]，且 b 的前缀 gcd 数组恰好等于 a，即 gcd(b[1],b[2],...,b[i]) 恰好等于 a[i]（下标从 1 开始）。
答案模 998244353。

b1...bi...
gcd(b1...bi) = ai

尝试引入bi+1 满足 gcd(b1...bi,bi+1) - gcd(ai,bi+1) = ai+1

再保证ai是ai+1的倍数的前提下
    即考虑 a=ai+1 的倍数中 k*a, (k*a, ai) = a

    1 ... t=m//a[i+1] 中与 d=(ai//ai+1) 互质的数量

"""
import itertools
import sys
from functools import cache
from operator import add, xor
from typing import List
from math import gcd, lcm, isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 998244353

# 2 3 5
# print(2*3*5*7*11*13*17*19*23*29) 6469693230 -- 不同的质因子不超过9

# n=p*q
# 大于sqrt(n) 的质因子不会有两个 （因子）

def euler_sieve(N):
    primes = []
    is_prime = [True] * (N+1)
    is_prime[0] = is_prime[1] = False
    spf = [0]*(N+1)   # spf[x] = x 的最小质因数

    for i in range(2, N+1):
        if is_prime[i]:
            primes.append(i)
            spf[i] = i

        # 按递增素数p 作为spf去筛 t=p*i 保证每个p是x的spf (当p到达i的spf就应停止 见下break)
        for p in primes:
            t = i * p
            if t > N: break

            spf[t], is_prime[t] = p, False

            if i % p == 0: # p|i 从小到大遍历p 的第一个 p|i 说明p=spf[i] 对后面大于p的 p'*i 就多余了，因为p`*i已被i的spf过滤掉
                break
    return primes, is_prime, spf
N = 10 ** 5
prime, is_prime, spf = euler_sieve(N)


for _ in range(RI()):
    n, m = RII()
    a = RILIST()

    res = 1
    for i in range(1, n):
        #print(a[i-1], a[i], a[i-1] % a[i])
        # k*a[i-1]
        # gcd(b1...bi-1)=ai-1
        # gcd(b1...bi-1, bi) = ai
        # gcd(ai-1, bi) = ai

        if a[i-1] % a[i] != 0:
            res = 0
            break
        d = a[i-1]//a[i]
        t = m//a[i]
        # [1...t] (x,d)=1
        # bi=ai*x
        # ai-1=ai*d
        # -- gcd(bi,ai-1) = ai*(x,d)=1

        # [1...t] (x,d)=1
        # 考虑d的因子
        r = d
        ps = []
        for i in range(2, isqrt(d)+1):
            if d % i > 0 or not is_prime[i]: continue
            ps.append(i)
            while r % i == 0:
                r //= i
        # 检查剩余的r是不是素数
        # 已经过滤掉d所有 小于 sqrt(d)的素因子. 如果剩余r > 1 说明必是素数 否则会被d的因子过滤
        if r > 1:
            ps.append(r)

        cnt = t
        for s in range(1, 1<<len(ps)):
            sign = 1 if s.bit_count() % 2 == 0 else -1

            g = 1
            for i in range(len(ps)):
                if s >> i & 1:
                    g *= ps[i]

            cnt += sign * (t//g)
        res = (res * cnt) % MOD
    print(res)

