"""
https://codeforces.com/problemset/problem/2065/G

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) 和长为 n 的数组 a(2≤a[i]≤n)。

如果 x 能表示为两个质数的乘积（两个质数可以相等），那么称 x 为半质数。
输出有多少对 (i,j) 满足 i <= j 且 LCM(a[i], a[j]) 是半质数。


枚举右维护左，注意组成以下的pattern:
pq
    p, q
    pq, d=pq,p,q,1
    d, pq
    当前是指数 -- 左侧所有单质数、左侧所有他的倍数半指数
    当前是半指数 -- 左侧所有其因子数 1 p,q,pq
"""
import sys
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

N = 2*10**5 + 1
# —— 预处理：线性筛出所有质数 + 半质数（semiprime）
prime = []
is_prime = [True] * (N + 1)
is_prime[0] = is_prime[1] = False
for i in range(2, N + 1):
    if is_prime[i]:
        prime.append(i)
    for p in prime:
        if i * p > N:
            break
        is_prime[i * p] = False
        if i % p == 0:  # 找到了i的最小素因数，后面不再继续
            break

# 半质数表：is_semi[x] = (p, q) if x = p * q
is_semi = [None]*(N+1)
for i,p in enumerate(prime):
    for j in range(i, len(prime)):
        if p * prime[j] > N: break
        is_semi[p * prime[j]] = (p, prime[j])



for _ in range(RI()):
    n, nums = RI(), RILIST()
    res = 0

    # 记录已扫过数字的各种计数
    cnt = defaultdict(int)     # 所有出现过的数字计数
    cnt_prime = 0              # 已见不同素数总数
    cnt_pq = defaultdict(int)  # 已见 semiprime 中每个素因子的出现次数
    cnt_semi = 0               # 已见 semiprime 总数

    for x in nums:
        if is_prime[x]:

            # 模式1：两个不同素数 p1,p2 → LCM = p1*p2
            #     对每个新素数 x，和之前所有“不同”素数配对
            res += (cnt_prime - cnt[x])

            # 模式2：素数 p 和之前所有含因子 p 的 semiprime → LCM = p*q
            res += cnt_pq[x]

            cnt_prime += 1
            cnt[x] += 1

        elif is_semi[x]:
            p,q = is_semi[x]

            # 模式3：两个同 semiprime x=pq → LCM=x
            # 模式4：semiprime x 和之前的素因子 p,q → LCM=x
            # 模式5：semiprime x 和之前的 1 → LCM=x
            res += cnt[x] + cnt[p] + (cnt[q] if p != q else 0) + cnt[1] + 1

            cnt[x] += 1      # 同 x 的 semiprime
            cnt_pq[p] += 1   # 含因子 p 的半质数
            if p != q:
                cnt_pq[q] += 1  # 含因子 q 的半质数（若 p≠q）
            cnt_semi += 1      # 和 1 配对
        elif x == 1:
            # 模式6：1 和任何 semiprime → LCM=semiprime
            res += cnt_semi
            cnt[1] += 1

    print(res)
