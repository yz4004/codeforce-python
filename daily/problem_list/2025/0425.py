"""
https://codeforces.com/problemset/problem/825/F

输入长度 ≤8000 的字符串 s，只包含小写英文字母。

你需要压缩 s = s1 * c1 + s2 * c2 + ...
例如 abababcc = ab * 3 + c * 2。

压缩后的长度定义为 |s1| + |c1| + |s2| + |c2| + ...
其中 |c1| 表示整数 c1 的十进制长度。
例如 ab * 3 + c * 2 的长度为 2 + 1 + 1 + 1 = 5。

输出 s 压缩后的最短长度。

... [i-2*l, i-l) [i-l, i) [i,i+l=j)

i//l

i

划分型 DP。

从右往左 DP（因为下面要做 KMP，方便套模板），定义 f[i] 表示 [i,n-1] 压缩后的最短长度。

如何计算 f[i]？我们将子串左端点固定为 i，右端点枚举 j=i,i+1,...,n-1。
用 KMP 计算子串 [i,j] 的 周期，设最短周期串长为 k（如果周期=1，长度就是 j-i+1），那么 [i,j] 由 (j-i+1)/k 个长为 k 的字符串组成，所以压缩后的长度为 len10((j-i+1)/k) + k。其中 len10(x) 表示 x 的十进制长度。

所以有转移（枚举 j，所有转移来源取最小值）
f[i] <- f[j+1] + len10((j-i+1)/k) + k
其中 f[j+1] 表示 [i,n-1] 去掉 [i,j] 后的子问题 [j+1,n-1]。

初始值 f[n] = 0，f[i] = min(n-i+1, f[i+1]+2)。其中 n-i+1 表示 [i,n-1] 作为一个子串，周期=1；f[i+1]+2 表示 [i,i] 作为一个子串，周期=1。
答案为 f[0]，即原问题，[0,n-1] 压缩后的最短长度。




"""


import sys, itertools
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

s = RS()
def log10(x):
    return len(str(x))
def solve(s):
    n = len(s)
    # lcp[i][j]
    lcp = [[0]*(n+1) for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        for j in range(n-1, i-1, -1):
            if s[i] == s[j]:
                lcp[i][j] = lcp[i+1][j+1] + 1

    f = [inf]*(n+1)  # f[i] 前i个字符的最短划分
    f[0] = 0

    for i in range(0, n+1):
        for j in range(i+1,n+1):
            #  f[..i] s[i..j) 作为压缩段
            l = j-i
            f[j] = mn(f[j], f[i] + l + 1)

            # s[i..j) 最大重复次数 k_mx (向后看）
            # lcp[i][i+l] lcp[i][i+2*l] ... lcp[i][i+(k-1)*l] 都 >= l
            # ！但是仔细发现 其实 lcp[i][j] j=i+l 如果大于l 则同时切掉l的prefix后，
            # lcp[i+l][j+l] i+l=j 开头的部分和i是一样的，如果他仍大于l 说明 lcp[i][i+2*l] >= l
            match = lcp[i][j]
            k_max = match // l + 1
            for k in range(2, k_max+1):
                f[i + l * k] = mn(f[i + l * k], f[i] + l + log10(k))
    return f[n]
print(solve(s))
# sys.exit(0)

def solve1(s):
    n = len(s)

    # [,i]
    # [j,i] 考虑以j-i 为段，向前尽可能的延展 []

    f = [inf]*(n+1)  # f[i] 前i个字符的最短划分
    f[0] = 0
    for i in range(1, n+1):
        for j in range(i): # 枚举前一个划分点/状态 f[j] [j,i] * c
            seg = s[j:i]
            l = i-j
            cnt = 1
            f[i] = mn(f[i], f[j] + l + 1)
            while l <= j and s[j-l:j] == seg:
                cnt += 1
                # [j-l:j]
                f[i] = mn(f[i], f[j-l] + l + len(str(cnt)))
                j -= l
    # print(f[n])
    return f[n]


print("s1", solve1(s))


def z_func(s):
    n = len(s)
    z = [0] * (n+1)
    l = r = 0
    for i in range(1, n):
        if i <= r:  # [l, r]  x-0 = i-l
            z[i] = min(z[i - l], r - i + 1)
        while i + z[i] < n and s[i + z[i]] == s[z[i]]:
            l, r = i, i + z[i]
            z[i] += 1
    return z

def solve2(s):
    n = len(s)

    # [,i]
    # [j,i] 考虑以j-i 为段，向前尽可能的延展 []
    # 8000

    # f = [inf]*(n+1)  # f[i] 前i个字符的最短划分
    # f[0] = 0
    # for i in range(0, n+1):
    #     # f[0-i] 已经计算完毕
    #     for j in range(i+1,n+1): # 枚举前一个划分点/状态 f[i] [i:j]
    #         seg = s[i:j]
    #         l = j-i
    #         cnt = 1
    #         f[j] = mn(f[j], f[i] + l + 1)
    #         while l <= i and s[i-l:i] == seg:
    #             cnt += 1
    #             # [i-l:i]
    #             i -= l
    #             f[j] = mn(f[j], f[i] + l + len(str(cnt)))
    # return f[n]

    zs = [None]*n
    for i in range(n):
        # s[i:] 计算得到的z函数 s[i:][j] 代表 s[i+j:] 和 s[i:] 的最长公共前缀；反之，问 lcp(s[i:], s[j:]) = zs[i][j-i]
        zs[i] = z_func(s[i:])

    # zs[i]

    f = [inf]*(n+1)  # f[i] 前i个字符的最短划分
    f[0] = 0
    for i in range(0, n+1):
        # f[0-i] 已经计算完毕

        # [i+1 ... ]
        for j in range(i+1,n+1): # 枚举前一个划分点/状态 f[i] [i:j]
            # [] [i,j)
            l = j-i
            cnt = 1
            p = i
            f[j] = mn(f[j], f[p] + l + 1)
            # while l <= i and s[i-l:i] == seg:
            # print(i, i-l, l, zs[i-l], j)
            while l <= p and zs[p-l][i-(p-l)] >= l:
                cnt += 1
                # [i-l:i]
                p -= l
                f[j] = mn(f[j], f[p] + l + len(str(cnt)))
    return f[n]
print("s2", solve2(s))

def log10(x):
    return len(str(x))

# def solve3(s):
#     n = len(s)
#     # lcp[i][j]
#     lcp = [[0]*(n+1) for _ in range(n+1)]
#     for i in range(n-1, -1, -1):
#         for j in range(n-1, i-1, -1):
#             if s[i] == s[j]:
#                 lcp[i][j] = lcp[i+1][j+1] + 1
#
#     f = [inf]*(n+1)  # f[i] 前i个字符的最短划分
#     f[0] = 0
#
#     for i in range(0, n):
#         for j in range(i+1, n+1):
#             #  f[..i] s[i..j) 作为压缩段
#             l = j-i
#             f[j] = mn(f[j], f[i] + l + 1)
#
#             # s[i..j) 最大重复次数 k_mx (向后看）
#             # lcp[i][i+l] lcp[i][i+2*l] ... lcp[i][i+(k-1)*l] 都 >= l
#             # ！但是仔细发现 其实 lcp[i][j] j=i+l 如果大于l 则同时切掉l的prefix后，
#             # lcp[i+l][j+l] i+l=j 开头的部分和i是一样的，如果他仍大于l 说明 lcp[i][i+2*l] >= l
#             match = lcp[i][j]
#             k_max = match // l + 1
#             for k in range(2, k_max+1):
#                 f[i + l * k] = mn(f[i + l * k], f[i] + l + log10(k))
#     return f[n]

def solve3(s):
    n = len(s)
    # lcp[i][j]

    f = [inf]*(n+1)  # f[i] -- s[i:] 最优划分
    f[n] = 0
    n = len(s)
    
    log10 = [0]*(n+1)
    for x in range(1, n+1):
        log10[x] = log10[x//10] + 1

    for i in range(n-1, -1, -1):

        f[i] = f[i+1] + 2
        
        m = n - i 
        pi = [0]*m
        k = 0 # prefix match s[i:] 
        #  s[i..j) 作为压缩段
        for l in range(1, m):
            j = i + l

            # 计算pi -- pi[i]
            while l > 0 and s[]



            # s[i:] s[j:]
            match = z[l]
            k_max = match // l + 1
            for k in range(2, k_max+1):
                f[i + l * k] = mn(f[i + l * k], f[i] + l + log10[k])
    return f[n]


print("s3", solve3(s))
# # c2z1ab2
#
sys.exit(0)

import random
# 对拍测试
for _ in range(10):
    n = random.randint(1, 1000)
    # a = random.sample(range(1 << 30), n)
    # s = [random.randint(0, 26) for _ in range(n)]

    s = [chr(ord("a") + random.randint(0, 25)) for _ in range(n)]

    expected = solve1(s)
    actual = solve3(s)

    if expected != actual:
        print("Mismatch!")
        print(f"a = {s}")
        print(f"expected = {expected}, actual = {actual}")
        break
else:
    print("✅ All tests passed!")




