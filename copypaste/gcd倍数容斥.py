
"""
gcd倍数容斥

求 gcd=k 恰好等于k的条件下的某个量
先求 gcd=k*i 所有k的倍数的量，然后减去恰好等于 2*k 3*k...
- 那些更大的恰好在此前的计算中得出，init是 gcd=m 最大值的情况

1. 求gcd是k的倍数的量 -- 应该是个相对简单的方向
2. gcd倍数容斥

"""
import itertools
from bisect import bisect_left
from collections import Counter, defaultdict
from typing import List
MOD = mod = 10 ** 9 + 7
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

N = 10 ** 6
prime, is_prime, spf = euler_sieve(N)

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


# lc3725
# https://leetcode.cn/problems/count-ways-to-choose-coprime-integers-from-rows/
# https://chatgpt.com/c/68fd50ae-0704-832b-976f-64b711578a98
def countCoprime(self, mat: List[List[int]]) -> int:
    # 矩阵每行选一个元素，所有人互质的方案的方案数
    n = len(mat)

    # 倍数容斥
    # 统计gcd=1/互质的选择方案数 (r1,r2...rk)
    # 统计所有方案数 - gcd恰好等于k的方案数 for k >= 2

    # 如何统计gcd=k*j 即为k的倍数的选择方案数
    # - 指定k 提取每行所有k的倍数计数 - 乘
    # - 对每个k统计倍数 1.暴力枚举矩阵 2. 枚举k的倍数+哈希表 3. 求因子

    # 如何统计gcd=k 恰好为k的方案数
    # - k的倍数的所有方案数 减去 gcd=2*k 3*k... 对应的恰好方案数

    m = max(x for row in mat for x in row)  # 150

    # f[k] - 选择方案gcd为k的倍数的 (选择方案gcd=k 2k ... jk)
    f = [0] * (m + 1)
    freqs = [None for _ in range(n)]  # 枚举k的倍数+哈希表
    for i, row in enumerate(mat):
        freq = [0] * (m + 1)
        for x in row:
            freq[x] += 1
        freqs[i] = freq

    for d in range(1, m + 1):
        t = 1
        for freq in freqs:
            cnt = 0
            for kd in range(d, m + 1, d):
                cnt += freq[kd]
            t = (t * cnt) % mod
        f[d] = t

    # 恰好d = 所有d整除的case -
    for g in range(m, 0, -1):
        cur = f[g]
        for d in range(g + g, m + 1, g):  # 此时 f[k*g] 已经是恰好. 初始状态f[m] 开始就是恰好
            cur = (cur - f[d]) % mod
        f[g] = cur
    return f[1]

# lc3312 https://leetcode.cn/problems/sorted-gcd-pair-queries/
# 计算数组多少对数 GCD 恰好等于 i （查询数组）
# 变形题
# 计算有多少个子序列的 GCD 恰好等于 i。见 CF803F。
# 计算树上有多少条简单路径的点权 GCD 恰好等于 i。见 CF990G。
#
# 子数组gcd - logtrick
def gcdValues(nums: List[int], queries: List[int]) -> List[int]:
    # 统计所有 gcd(nums[i], nums[j]) 的计数. 然后支持rank查询
    n, u = len(nums), max(nums)

    # 统计恰好为d的pair数量
    # 1. f[d] = 统计gcd pair是d的倍数的数量
    # 2. 恰好为d = f[d] - f[2*d] - ... f[j*d]
    # (f[j*d] 已经更新为恰好)

    # d作为最大公因数
    # = d作为公因数 - d的倍数作为公因数 = d作为最大公因数的个数

    # 1. f[d] = 统计k的倍数 - gcd pair是d的倍数的数量 即为 comb(f[d],2)
    cnt = [0]*(u+1)
    for x in nums: cnt[x] += 1
    f = [0]*(u+1)
    for d in range(1, u+1):
        for kd in range(d, u+1, d):
            f[d] += cnt[kd]

    # 2. 恰好为d = f[d] - f[2*d] - ... f[j*d]
    for d in range(u, 0, -1):

        # 任意d的倍数（在nums中）两两组合，d是公因数
        tmp = f[d] * (f[d] - 1) // 2

        # 如果kd(d的倍数) （在nums中）作为gcd，减去
        for kd in range(2 * d, u + 1, d):
            tmp -= f[kd]
        f[d] = tmp

    # 生成gcd count数组
    # gcds 都是 1-u元素的因子, 因子成对出现，每个数x因字数不超过 2*(x)^1/2
    f = [(d,f[d]) for d in range(u+1) if f[d] > 0]
    ps = [0]*(len(f)+1)
    for i, (d,cnt) in enumerate(f):
        ps[i+1] = ps[i] + cnt

    res = []
    for q in queries:
        i = bisect_left(ps, q)
        res.append(f[i][0])
    return res
    # 常数优化 https://chatgpt.com/c/68fec868-4ba0-832b-a732-068c113782ec

# https://codeforces.com/problemset/problem/803/F
# 子序列gcd=1 的计数
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
def solve(n, nums):
    # n, nums = RI(), RILIST()

    # 1. f[d] - 子序列gcd为d的倍数 - d的所有倍数的幂集 -- 2^cnt_d - 1
    # 2. 恰好为d = f[d] - f[2*d] ... f[j*d]
    m = max(nums)
    cnt = Counter(nums)

    # f[d] d的倍数的计数，幂集放在后面算
    f = [0] * (m + 1)
    for d in range(1, m + 1):
        # d 2d ...
        for g in range(d, m + 1, d):
            f[d] = (f[d] + cnt[g]) % MOD

    h = [0] * (m + 1)
    for d in range(m, 0, -1):
        t = pow(2, f[d], MOD) - 1  # 一个d的倍数计算得到的某个量 t 这里是子序列的数量，该子序列所有人以d为倍数
        # 初始m 会得到所有m的子序列数量，当m的因子d计算 2^f[d] ，需扣掉完全由m参与的子序列计数

        for kd in range(2 * d, m + 1, d):  # 枚举 d的所有倍数kd 的对应纯粹由kd 组成的instance
            t = (t - h[kd]) % MOD
        h[d] = t

    print(h[1] % MOD)

# cf990g
# https://codeforces.com/problemset/problem/990/G gcd容斥 + gcd连通性
# 树上路径gcd恰好为k的路径个数
# - 如果是单链 即为子数组gcd 用 logtrick nlogU - 但是logtrick延展，没新增一个元素要压缩前面的列表。但切换分支我们不能破坏祖先链，则每次递归都要复制祖先链的数组信息，单链意味着n^2
# - gcd恰好形问题 提示我们倍数容斥
#   f[d] 初始化为被因子d整除的简单路径数量 - （该简单路径上所有元素都是d的倍数 才能路径联通）
#   d公因子联通性 -> 并查集找连通块，size为sz的连通块有 comb(sz,2) 个简单路径. 每个连通块需独立计
#   对每个d都要单独做连通性
def solve_cf990g(n, nums, edges, graph):
    m = max(nums)

    # 欧拉筛/Euler + spf (smallest prime factor)
    prime, is_prime, spf = euler_sieve(m)

    nodes_by_d = defaultdict(list) # d对应的树上node d作为他们的公因子
    for i, x in enumerate(nums):
        factors = factorize(x)
        for d in factors:
            nodes_by_d[d].append(i)
        nodes_by_d[1].append(i)

    f = {} # 对每个d单独统计连通性
    for d, nodes in nodes_by_d.items():
        pa = {i: i for i in nodes}
        sz = {i: 1 for i in nodes}

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
        for i, j in itertools.combinations(nodes, 2):
            if (i, j) in edges:
                merge(i, j)

        components = {find(i) for i in nodes}
        f[d] = sum(sz[i] * (sz[i] - 1) // 2 + sz[i] for i in components)

        # gcd容斥
        for d in sorted(f.keys(), reverse=True):
            for g in range(2 * d, m + 1, d):
                if g in f:
                    f[d] -= f[g]

        res = ""
        for i, x in sorted(f.items()):
            if x:
                res += str(i) + " " + str(x) + "\n"
        print(res)







#######################################

def subsequencePairCount(self, nums: List[int]) -> int:
    n = len(nums)
    u = max(nums)
    # f[d1][d2] - d1/d2 倍数
    # 子序列1的gcd是d1倍数，子序列2的gcd是d2倍数，且不想交

    f = [[0]*(u+1) for _ in range(u+1)]

    for x in nums:
        t = x

        g = [[0] * (u + 1) for _ in range(u + 1)]

        while True:
            # x的因子t 参与到子数组贡献

            for i in range(1, u+1):
                g[i][t] = 2*f[i][t] + 1 #

            for i in range(1, u + 1):
                if i == t: continue
                f[t][i] += f[t][i] + 1  #

            if t == 1:
                break
            p = spf[t]
            t //= p

    print(f)




