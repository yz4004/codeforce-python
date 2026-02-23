"""
https://codeforces.com/problemset/problem/1766/D

输入 T(≤1e6) 表示 T 组数据。
每组数据输入 x y(1≤x<y≤1e7)。

输出如下连续互质序列的最长长度。
(x,y), (x+1,y+1), (x+2,y+2), ..., (x+k,y+k)
其中每一对元素都是互质的。

如果 (x,y) 不互质，输出 0。
如果序列无限长，输出 -1。
"""
import sys
from math import isqrt, inf, gcd

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
N = 10 ** 7
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
    x, y = RII()
    if x > y:
        x, y = y, x

    k = y - x
    if k == 1:
        print(-1)
        continue

    if gcd(x,y) > 1:
        print(0)
        continue


    res = inf
    for d, _ in factorize(k):
        t = (x//d + 1) * d
        res = mn(res, t-x)
    print(res)