"""
https://codeforces.com/problemset/problem/1028/H

输入 n(2≤n≤194598) q(1≤q≤1049658) 和长为 n 的数组 a(1≤a[i]≤5032107)，下标从 1 开始。
然后输入 q 个询问，每个询问输入 L R(1≤L<R≤n)，表示 a 的一个子数组 b，下标范围 [L,R]。

对于子数组 b，如果 b 中存在一对下标不同的数 x 和 y，满足 x*y 是完全平方数，那么称 b 为好子数组。
每次操作，你可以：
选择 b 中的一个数 b[i]，执行 b[i] *= p，其中 p 是任意一个质数。
或者，选择 b 中的一个数 b[i]，以及 b[i] 的一个质因子 p，执行 b[i] /= p。

输出把 b 变成子好数组的最小操作次数。
所有询问互相独立。

5*10^6

10101
10001

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

# print(2*3*5*7*11*13*17)
# print(5032107)
# print(2*3*5*7*11*13*17*19)
# 510510
# 5032107 -- 最长的组合是 2 3 5 7 11 13 17 <= 7
# 9699690

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
N = 5032107
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

n, Q = RII()
a = RILIST()
b = [None]*n
for i,x in enumerate(a):
    core = []
    k = 1
    for p,c in factorize(x):
        if c % 2:
            core.append(p)
            k *= p
    b[i] = (k, core)

# x - s1 s2 ... sm
# 0 1...14

# [L,... i j
#
queries = defaultdict(list)
for idx in range(Q):
    l,r = RII()
    l,r = l-1, r-1
    queries[r].append((l,idx))

# 按R排序 加入计算，按L 计入范围
# 对L,R 找大于L的 最小操作
# 对操作数 j=0 1 ... 14 维护满足改操作最大的 L 即大于L的数里有两个点距离为j
# x

ans = [-1]*Q

ops = [-1]*15  # 0-14
s_j = defaultdict(lambda:[-1]*8)
for i, (x, xs) in enumerate(b):
    # x - 当前素数集合
    # 枚举子集 s 作为桥 和对应操作为 len(s)+1...+7 的最右侧集合

    m = len(xs)
    f = [1] * (1 << m)
    for s in range(0, 1 << m):
        lb = s & -s
        if s:
            f[s] = v = f[s - lb] * xs[lb.bit_length() - 1]

        # s - x
        # d2
        # s - y
        # d1
        c = s.bit_count()
        d2 = m - c
        for d1 in range(8): # 0-7
            # tmp[c + d1] 最右侧的数字
            recent_s_d1 = s_j[f[s]][d1]
            if recent_s_d1 != -1:
                # d1 - d2 存在
                ops[d1+d2] = mx(ops[d1+d2], recent_s_d1)


    for s in range(0, 1 << m):
        # 当前 x 是 s右侧的更大集合，更新距离
        d2 = m - s.bit_count()
        s_j[f[s]][d2] = i

    if i in queries:
        for l,idx in queries[i]:
            for d in range(15):
                if ops[d] >= l:
                    ans[idx] = d
                    break

print("\n".join(map(str, ans)))

sys.exit(0)

i = 0
for l,r,idx in queries:

    while i <= r:
        x_ps = b[i]


        # (y,x) 操作距离为d
        # 枚举中间子集 s.

        m = len(x_ps)
        f = [1] * (1 << m)
        for s in range(1, 1<<m):
            lb = s & -s
            f[s] = v = f[s - lb] * x_ps[lb.bit_length()-1]

            d1 = m - s.bit_count()
            for d in range(d1, 15):
                # x - s - y 操作总数为d. 是否有 s-y 操作为d2的y，有则更新最近的y
                d2 = d - d1


            # s -

        i += 1


    for d in range(15):
        if g[d] >= l:
            res[idx] = d




for _ in range(Q):
    L, R = RII()
    L, R = L-1, R-1
    # [L,R]
    # 所有的 x1...xk 表现为一些素因子子集
    # 10110  10101001
    # 集合的最小距离

    # a -> b 先删掉a的 再添加一些到b -- 存在一个a/b的公共子集. 作为桥
    # a和其最近子集的距离 -- a的某个子集sa到a的距离，该sa到非a以外的某个b的最近的距离 b in [L,R]
    # 对a的每个子集，处理两个最近的距离

    res = inf
    pre = {}
    # print(a[L:R+1]) # 2, 2,11
    for i in range(L,R+1):
        x = b[i]

        # 枚举 ps 的子集
        ps = []
        while x > 1:
            p = spf[x]
            ps.append(p)
            x //= p

        #print(i, ps, pre)

        m = len(ps)
        f = [1]*(1<<m)

        #
        if 0 in pre: res = mn(res, pre[0] + m)
        for s in range(1, 1<<m):
            lb = s & -s
            f[s] = v = f[s - lb] * ps[lb.bit_length()-1]

            # d(v, x) = m - s.bit_count()
            d = m - s.bit_count()
            if v in pre:
                res = mn(res, d + pre[v])

        if 0 in pre:
            pre[0] = mn(pre[0], m)
        else:
            pre[0] = m

        for s in range(1, 1<<m):
            v = f[s]
            d = m - s.bit_count()
            if v in pre:
                pre[v] = mn(pre[v], d)
            else:
                pre[v] = d
    print(res)












