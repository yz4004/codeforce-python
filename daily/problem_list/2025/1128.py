"""
https://codeforces.com/problemset/problem/1620/G

输入 n(1≤n≤23) 和长为 n 的字符串数组 a，每个 a[i] 的长度 ≤2e4，只包含小写英文字母。
保证每个 a[i] 都是升序，例如 a[i] = aaabbccc...

对于字符串数组 b，定义 f(b) 为不同字符串（包括空串）的数量，这些字符串都至少是其中一个 b[i] 的子序列。
特别地，f([]) = 0。
-- 也就是统计 b = [s1,s2...] 每个人的子序列，全放一起去重

a 有 2^n 个子序列 b，计算这 2^n 个 f(b) % 998244353。
由于输出 2^n 个数太慢了，你只需输出 (f(b) % 998244353) * len(b) * sum(index(b)) 的异或和。
其中 index(b) 是一个长为 len(b) 的列表，表示 b 中元素在 a 中的下标（下标从 1 开始）。

1. 给定一个字符串序列 （a的子序列 ai1 ai2 ... aik）计算 f(b) 即考虑所有aij 的子序列的并集
    - 容斥原理 (aij的子序列 j=1...k) 之和 - 重复计算的
    - 10110
      10101 先不考虑重数 假设unique. 这两个交集 10100 的子序列数. 有重数取min 10100-[20300] 假设重数是2/3 - (2+1)*(3+1)
      n个序列容斥的复杂度
      c(n,1)*. + c(n,2)*. + c(n,3)*26 ... 2^n*26
      而对a的每个子序列都计算上式
      sum[ comb(n,ni) * 2^ni * 26 ]-- 长为ni的子序列个数 comb(n,ni)
      c(n,ni) * 1^(n-ni) * 2^ni ...
      = 3^n * 26
      = 3^23 * 26

      容斥一个term:
      g(c) = -1 ^ (|c|+1) * way(c)

      f[b] = (子序列的数量，是任一b中字符串的子序列) - (子序列的数量，是b中任意两个字符串的子序列) + ...

      从b中挑两个字符串 si,sj 考虑 si,sj 的公共子序列 (30241 & 10200)
      (30241 & 10200) = (10200) 有 (1+1) * (2+1) 个公共子序列
      对 (1+1) * (2+1) 个公共子序列 中的任意 字符串 t.
      这里只说他符合 si sj 的公共部分. 如果他符合 si sj sk 的公共部分. 则 (si,sj) (si,sk) (sj,sk) 都会减去一份
      初始t被重复加了3次. 然后又全被减去
      同时满足 (si,sj,sk) 再加回来一次
      每次容斥都是在子集上转移

      f[b] = g(c) for c is subset of b


2. 子集层面的相加 f[s] 的计算取决于 s的所有子集的 f[sub_i] where sub_i in s
    sos 子集转移

    对a的子集考虑sos

    f[s] - a的子集s的容斥结果
    初始
        f[s] = g[s]

"""
import itertools
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 998244353

n = RI() #<=23
a = []
f = [0] * (1<<n)
ord_a = ord("a")
for _ in range(n):
    cur = [0]*26
    ai = RS()
    for c in ai:
        cur[ord(c) - ord_a] += 1
    a.append(cur)

f[0] = 0
for s in range(1, 1<<n):
    # 考虑a的字符串子集 s = 10110...

    tmp = [inf]*26
    for j in range(n):
        if s >> j & 1:
            aj = a[j]
            for i in range(26):
                aji = aj[i]
                if aji < tmp[i]:
                    tmp[i] = aji
    gc = 1
    for mn_c in tmp:
        gc = (gc * (mn_c+1)) % MOD

    # g(c) = -1 ^ (|c|+1) * way(c) 对子集c的一个容斥单元
    sign = -1 if s.bit_count() % 2 == 0 else 1
    f[s] = sign * gc

for i in range(n):
    for s in range(1<<n):
        if s >> i & 1:
            f[s] += f[s ^ (1<<i)]
            f[s] %= MOD


f_sm = [0]*(1<<n)
for s in range(1<<n):
    lb = s & -s
    f_sm[s] = f_sm[s ^ lb] + lb.bit_length()

# (f(b) % 998244353) * len(b) * sum(index(b)) 的异或和。
res = 0
for s in range(1<<n):
    cur = f[s] * s.bit_count() * f_sm[s]
    res ^= cur
print(res)


