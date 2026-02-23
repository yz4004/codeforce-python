"""
https://codeforces.com/problemset/problem/1470/B

输入 T(≤1e5) 表示 T 组数据。所有数据的 n 之和 ≤3e5，q 之和 ≤3e5。
每组数据输入 n(1≤n≤3e5) 和长为 n 的数组 a(1≤a[i]≤1e6)。
然后输入 q(1≤q≤3e5) 和 q 个询问。
每个询问输入 w(0≤w≤1e18)。

如果 lcm(x,y) / gcd(x,y) 是完全平方数，那么称 x 与 y 相邻。
每过一秒，所有 a[i] 同时被替换成 a 中所有与 a[i] 相邻的数的乘积（包括 a[i]）。
定义 d[i] 为与 a[i] 相邻的元素个数（包括 a[i]）。
对于每个询问，输出 w 秒后，max(d) 的值。每个询问互相独立。

ai-aj <=> ai * aj = t^2

ai -> ai1...aik -- 1100

aj -> aj1...ajl -- 1011

0s -- 平方核最多的人
1s -- 所有偶数次出现的人变0，奇数不变
2s ...


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

# 欧拉筛/Euler + spf (smallest prime factor)
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
N = 10 ** 6 + 1
primes, is_prime, spf = euler_sieve(N)


def factorize(x):
    res = []
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        res.append((p,cnt))
    return res

for _ in range(RI()):
    n, a = RI(), RILIST()

    # lcm(x,y) / gcd(x,y) = t*t
    # lcm(x,y) = gcd(x,y) * t*t = k1*x = k2*y. where (k1,k2) = 1

    # lcm * gcd = x*y
    # l/g * g*g = x*y

    # t*t * g*g = x*y

    # x,y 相邻 <=> x*y 是完全平方 == 平方剩余核一样

    kernels = defaultdict(int)
    for x in a:
        core = 1
        for p,cnt in factorize(x):
            if cnt % 2 == 1:
                core *= p

        if core == 1:
            kernels[1] += 1 # 已经是完全平方, 包括1
        else:
            kernels[core] += 1

    d0 = max(kernels.values())


    sq = kernels[1]
    del kernels[1]

    d1_even = sum(v for v in kernels.values() if v % 2 == 0) + sq
    d1_odd = max([v for v in kernels.values() if v%2 == 1], default=0)

    d = mx(d1_odd, d1_even)

    # ai: a1...ak
    for q in range(RI()):
        w = RI()
        if w == 0:
            print(d0)
        else:
            print(d)



