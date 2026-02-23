"""
https://codeforces.com/problemset/problem/990/G

输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤2e5)。
然后输入一棵无向树的 n-1 条边，节点编号从 1 到 n。节点 i 的点权为 a[i]。

对于每个满足 x ≤ y 的节点对 (x,y)，计算从 x 到 y 的简单路径的点权 GCD。
定义 f(i) 表示 GCD 等于 i 的简单路径个数。

对于每个 [1,2e5] 中的 i，如果 f(i) > 0，输出 i 和 f(i)。


- 统计树上路径gcd的数量
如果是单链 即为子数组gcd 用 logtrick nlogU
但是logtrick延展，没新增一个元素要压缩前面的列表。但切换分支我们不能破坏祖先链，则每次递归都要复制祖先链的数组信息，单链意味着n^2

gcd倍数容斥
1. f[d]=gcd为d的倍数的简单路径数量
- 给定一个d 可找树上d的倍数的点，如何统计路径 - 连通块 sz - comb(sz,2) 为简单路径数量

2. 再gcd倍数容斥即可
"""
import itertools
import sys
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, nums = RI(), RILIST()
edges = set()
graph = [[] for _ in range(n)]
for _ in range(n-1):
    a, b = RII()
    a, b = a-1, b-1
    if a > b: a,b = b,a

    graph[a].append(b)
    graph[b].append(a)
    edges.add((a,b))

m = max(nums)

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
prime, is_prime, spf = euler_sieve(m)

def factorize(x) -> defaultdict:
    res = defaultdict(int)
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        res[p] = cnt
    return res


nodes_by_d = defaultdict(list)
for i, x in enumerate(nums):
    factors = factorize(x)
    for d in factors:
        nodes_by_d[d].append(i)
    nodes_by_d[1].append(i)

f = {}
for d, nodes in nodes_by_d.items():
    pa = {i:i for i in nodes}
    sz = {i:1 for i in nodes}

    def find(x):
        root = pa[x]
        while pa[root] != root:
            root = pa[root]

        while x != root:
            tmp = pa[x]
            pa[x] = root
            x = tmp
        return root

    def merge(x, y):
        x, y = find(x), find(y)
        if x == y:
            return 0
        else:
            if sz[x] <= sz[y]:
                sz[y] += sz[x]
                pa[x] = y
            else:
                sz[x] += sz[y]
                pa[y] = x
            return 1

    nodes = sorted(list(nodes))
    for i,j in itertools.combinations(nodes, 2):
        if (i,j) in edges:
            merge(i,j)

    components = {find(i) for i in nodes}
    f[d] = sum(sz[i] * (sz[i] - 1) // 2 + sz[i] for i in components)

res = 0
for d in sorted(f.keys(), reverse=True):
    for g in range(2*d, m+1, d):
        if g in f:
            f[d] -= f[g]

res = ""
for i,x in sorted(f.items()):
    if x:
        res += str(i) + " " + str(x) + "\n"
print(res)