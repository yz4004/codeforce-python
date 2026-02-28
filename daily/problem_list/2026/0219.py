"""
https://codeforces.com/problemset/problem/2040/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) 和一棵 n 个节点的无向树的 n-1 条边。节点编号从 1 到 n。

给树上每个点设置整数点权，要求：
1. 点权范围 [1, 2n]。
2. 所有点权互不相同。
3. 相邻节点的点权绝对差不是质数。

输出节点 1,2,...,n 的点权。多解输出任意解。
如果无解，输出 -1。

"""
import sys, itertools
from functools import cache
from heapq import heappop, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
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
N = 2 * 10 ** 5
prime, is_prime, spf = euler_sieve(2*N)

"""
按前序遍历树+构造 
    从123...开始分配 临近都是1密铺 如果是单链则肯定没有素数差
    问题出现在拐点 当出现分岔 遍历一个子树后回来 可能出现素数差
    那就自增1. p和p+1肯定不同时为素数 (除了2/3) 因为后面p都是奇数

"""
def solve(n, g):
    res = [0]*n
    time = 1
    def dfs(i, p):
        nonlocal time

        res[i] = cur = time
        time += 1

        for j in g[i]:
            if j == p: continue

            while is_prime[time - cur]:
                time += 1
                if time > 2*n:
                    return False
            if not dfs(j, i):
                return False
        return True

    if dfs(0, -1):
        return res
    return -1


for _ in range(RI()):
    n = RI()
    g = [[] for _ in range(n)]
    for _ in range(n-1):
        a,b = RII()
        a,b = a-1, b-1
        g[a].append(b)
        g[b].append(a)
    print(" ".join(solve(n, g)))

# 星形图
# size=2
# 1-2-5 也没超过

# n=3
# 1-2-5-7 