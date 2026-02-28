# noinspection LanguageDetectionInspection
"""
https://codeforces.com/problemset/problem/986/E

输入 n(1≤n≤1e5) 和一棵 n 个节点的无向树的 n-1 条边。节点编号从 1 开始。
然后输入长为 n 的数组 a(1≤a[i]≤1e7)，表示节点点权。
然后输入 q(1≤q≤1e5) 和 q 个询问，每个询问输入 u v(1≤u,v≤n) x(1≤x≤1e7)。

对于每个询问，设从 u 到 v 的简单路径的点权序列为 b，
输出 gcd(x,b[1]) * gcd(x,b[2]) * ... * gcd(x,b[k]) % (1e9+7)，其中 k 是 b 的长度。

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

"""
u-v 点权序列
gcd(x, b1) * ... gcd(x, bi) ...

1. gcd没法aggregation
    不存在 gcd(x,a) * gcd(x,b) != gcd(x^2, ab)
    (p^3, p^2) * (p^1, p^2) = p^3
    就一个质因数来说 gcd 是对其次幂设置了 min 

2. 如果可以对每个质数单独检查
    u-v 对于因子p的分布有幂次序列 p^c1 p^c2 ... 对应x里p的幂次 p^cx 
    求 min(c1,cx) + min(c2,cx) ...
    
    
3. 对u到祖先节点的路径 + lca
    树状数组维护幂次分布和 下标是幂次 值是前缀和 
     
4. 范围1e7 的素数有很多 但幂次不会很多 对每个质因子维持幂次数组 
    2^24 > 1e7
    
5. 树上路径 u-lca-v 可以分解为 root-u, root-v - 2*root-lca
    这里因为计入节点 lca算一次 即 
        root-u, root-v - root-lca - root-pa[lca]
    
"""

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
def factorize(x) -> list[tuple]:
    res = []
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        res.append((p,cnt))
    return res

N = int(1e7)
prime, is_prime, spf = euler_sieve(N)



def solve(n, g, a, queries):

    # 节点u 到祖先节点路径 素数p的前缀和

    # u-v 路径 乘积计算拆开独立算 u-lca-v
    # (u,v,x) - (u,lca,x), (v,lca,x) -- lca = lca(u,v)
    ##### lca部分
    # 2. 深度表 st跳表 （有时还需跳表跳跃路径对应值）
    m = n.bit_length()
    depth = [0]*n
    st = [[-1]*m for _ in range(n)]
    pa = [-1]*n

    # 2.1 dfs初始化 深度/parent
    def dfs(i, p, d):
        depth[i] = d
        pa[i] = p
        for j in g[i]:
            if j == p: continue
            st[j][0] = i
            dfs(j, i, d+1)
    dfs(0, -1, 0)

    # 2.2 初始化st表
    for j in range(1, m):
        for i in range(n):
            if st[i][j - 1] != -1: #必须要有-1检查 否则越界造成错乱
                st[i][j] = st[st[i][j - 1]][j - 1]

    # 3. 简单LCA模板 - 只求lca （扩展可以维护求lca路径上的信息）
    def getLCA(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        # 3.1 先让ab同深度
        k = depth[a] - depth[b] # 将所有非空二进制bit对应的跳跃都作用上去
        for i in range(m):
            if k >> i & 1 == 1:
                a = st[a][i]

        # 3.2 如果a是b的祖先 则ab会想同。否则两者同时向上跳，直到lca的两个直连子节点为止
        if a != b:
            for i in range(m - 1, -1, -1): #从大到小bit尝试，如果没有跳过就作用上
                if st[a][i] != st[b][i]:
                    a, b = st[a][i], st[b][i]
            a = st[a][0]
        lca = a
        return lca

    # u-v被查询 对 u-v 路径分解
    # root-u, root-v - root-lca - root-pa[lca]
    # 记录当前查询编号 和 贡献正负值
    # 不能只累计正值
    query_bucket = defaultdict(list)
    for idx, (u,v,x) in enumerate(queries):
        ancestor = getLCA(u,v)

        query_bucket[u].append((x,idx,1))
        query_bucket[v].append((x,idx,1))
        query_bucket[ancestor].append((x,idx,-1))
        if pa[ancestor] != -1:
            query_bucket[pa[ancestor]].append((x,idx,-1))


    tmp = defaultdict(int)
    powers = defaultdict(lambda: [0]*24) # 2^24 >

    def dfs(u, pa):

        # 截止到u root-u 的所有素因子幂次之和
        for p,cnt in factorize(a[u]):
            powers[p][cnt] += 1

        for x, idx, sign in query_bucket[u]:
            # ancestor - u. cap
            # 频次<cap 的部分求和; 大于cap部分计数 * cap
            # m = tree0.rsum(1, cap) + cap * tree1.rsum(cap + 1, M)

            for p, cap in factorize(x):
                cnts = powers[p]
                m = 0
                for e in range(1, 24):
                    m += min(e, cap) * cnts[e]
                # 只记幂次
                # 注意查询 u=v u,v 就重复叠加了
                tmp[(idx, p)] += sign * m

        for j in g[u]:
            if j == pa: continue
            dfs(j, u)

        for p,cnt in factorize(a[u]):
            powers[p][cnt] -= 1
    dfs(0, -1)

    res = [0]*len(queries)
    for i,(u,v,x) in enumerate(queries):
        # w = getLCA(u,v)
        cur = 1
        for p,_ in factorize(x):
            # 不在查询做容斥，因为重合的点会叠加
            # if pa[w] != -1:
            #     power = tmp[(p,i)] + tmp[(p,i)] + tmp[(p,i)] - tmp[(pa[w],p, i)] # ancestor
            # else:
            #     power = tmp[(u,p,i)] + tmp[(v,p,i)] - tmp[(w,p,i)]

            power = tmp[(i,p)]
            cur = cur * pow(p, power, MOD) % MOD
        res[i] = cur
    return res

n = RI()
g = [[] for _ in range(n)]
for _ in range(n-1):
    a,b = RII()
    a,b = a-1,b-1
    g[a].append(b)
    g[b].append(a)
a = RILIST()

queries = []
for _ in range(RI()):
    u,v,x = RII()
    # u -> v - weight sequence
    # gcd(x, b1) * ... gcd(x, bi) ...
    u,v = u-1,v-1
    queries.append((u,v,x))

print("\n".join(map(str, solve(n, g, a, queries))))



