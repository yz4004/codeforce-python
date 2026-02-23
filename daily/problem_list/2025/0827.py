"""
https://codeforces.com/problemset/problem/2125/D

输入 n(1≤n≤2e5) m(1≤m≤2e5)。
然后输入 n 个闭区间，每个区间输入 l r(1≤l≤r≤m) p q(1≤p<q<998244353)，表示这个区间存在的概率为 p/q。

有 m 个点，编号从 1 到 m。
输出每个点都恰好被一个区间覆盖的概率。

注：设答案为最简分数 x/y，你需要输出 x*pow(y,mod-2)%mod，其中 mod=998244353。

[1,x]

"""
import sys
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 998244353



# ------------------------------------------------------
# fermat's little theorem: x^(p-1) = 1 mod p 对质数p 求质数模逆元
# p / q
# p * inv_q  (inv_q with respect to MOD, inv_q * q = 1 mod M)
# inv_q = pow(q, MOD-2, MOD)
prob = lambda p,q: p * pow(q, MOD-2, MOD) % MOD
inv = lambda x: pow(x, MOD-2, MOD)
# ------------------------------------------------------

# 要求密铺，且只能一组线段紧密排列，其余不能选.
# 从左往右看 f[x] 两种定义
# [1,x] 密铺的概率，不管 [x+1,m]
# [1,x] 密铺的概率，且 [x+1,m] 都不选中
# 前者比较直观，但是转移麻烦，后者转移好写
# 前者 [,l-1] [l,r] 如果要转移，需要带上 [l,r] 无任何区间的概率, 定义g[x] 为后缀 [x,]无区间 ，即 P([l,r])  = g[l]/g[r+1]
# 且还要免去 [l,r] 不选的概率 /(1-p/q) * p/q 因为 g[l] 包含了 (1-p/q) 不选当前 [l,r]

# 后者即可从初始都不选开始 (1-p/q) for pi qi. 转移即尝试翻转一个[l,r] /(1-p/q) * p/q

# 概率dp的难点
# https://chatgpt.com/c/68ae8ccb-2980-8332-acbb-ef3bbc65bc15
#

n, m = RII()
intervals = sorted(tuple(RII()) for _ in range(n))

g = [0]*(m+2) # g[i]: [i:] 没有任何区间的概率
g[m+1] = 1

rev_intervals = sorted(intervals, key=lambda x:x[1], reverse=True)
j = 0
cur = 1
for i in range(m, 0, -1):
    while j < n and rev_intervals[j][1] >= i:
        _,_,p,q = rev_intervals[j]
        pb = (q-p) * inv(q) % MOD
        cur = cur * pb % MOD
        # cur = cur * (q-p)/q
        j += 1
    g[i] = cur


# f[i] 截止到i的唯一覆盖概率, 且右侧没有覆盖
f = [0]*(m+2)
f[0] = 1
for l,r,p,q in intervals:
    p_lr = g[l] * inv(g[r+1])
    p_lr *= q * inv(q-p) % MOD
    f[r] += f[l-1] * prob(p,q) * p_lr % MOD
    f[r] %= MOD
print(f[m])

sys.exit(0)


g = 1
for l,r,p,q in intervals:
    g = g * prob(q-p, q) % MOD

# f[i] 截止到i的唯一覆盖概率, 且右侧没有覆盖
f = [0]*(m+2)
f[0] = g
for l,r,p,q in intervals:
    f[r] += f[l - 1] * prob(p, q) * prob(q, q - p) % MOD
    f[r] %= MOD

print(f[m])


