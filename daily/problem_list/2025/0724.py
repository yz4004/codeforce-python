"""
https://codeforces.com/problemset/problem/803/F

输入 n(1≤n≤1e5) 和长为 n 的数组 a(1≤a[i]≤1e5)。

输出 a 有多少个非空子序列 b，满足 gcd(b) = 1。（注：子序列不一定连续）
答案模 1e9+7。

子序列gcd=1.
gcd(A) = a, gcd(B) = b
A -- 两两 (p,q)=ga
-
调和级数枚举
n//1  n//2 ... n//n
n(1+1/2 + 1/3 ... 1/n)  = nlogn

倍数枚举 - 调和级数
统计d的倍数的数量（含有d作为因子的数的数量）
for d in range(2, n):
    for g in range(d, n, d):  # n//d --
        ...

d作为gcd(a,b) => d是a,b的因子 + a,b不含以d更大的因子

排除法 -- 任何gcd不为1的子序列
"""
import sys
from collections import Counter

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

MOD = 10 ** 9 + 7
n, nums = RI(), RILIST()

m = max(nums)
cnt = Counter(nums)

# d 作为因子, d的倍数
f = [0]*(m+1) # f[d] d的倍数
for d in range(1, m+1):
    # d 2d ...
    for g in range(d, m+1, d):
        f[d] = (f[d] + cnt[g]) % MOD

h = [0]*(m+1)
for d in range(m, 0, -1):
    t = pow(2, f[d], MOD) - 1  # 一个d的倍数计算得到的某个量 t 这里是子序列的数量，该子序列所有人以d为倍数
                               # 初始m 会得到所有m的子序列数量，当m的因子d计算 2^f[d] ，需扣掉完全由m参与的子序列计数

    for kd in range(2*d, m+1, d):  # 枚举 d的所有倍数kd 的对应纯粹由kd 组成的instance
        t = (t - h[kd]) % MOD

    h[d] = t

print(h[1] % MOD)
