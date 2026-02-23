"""
https://codeforces.com/problemset/problem/2104/E

输入 n(1≤n≤1e6) k(1≤k≤26) 和长为 n 的字符串 s，只包含前 k 个小写英文字母。
然后输入 q(1≤q≤2e5) 和 q 个询问，每个询问输入一个字符串 t，只包含前 k 个小写英文字母。保证所有 t 的长度之和 ≤1e6。

在 t 的末尾添加若干字母（必须是前 k 个小写英文字母），使得 t 不是 s 的子序列。
输出最少添加多少个字母。

1. t作为s子序列是从前比较 还是从后？
- 前，从后比较错误，从前

"""
from collections import defaultdict
from functools import cache
from math import comb, factorial, inf
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, k = RII()
s = [ord(c) - ord("a") for c in RS()]

# f[i]
n = len(s)
nxt = [None for _ in range(n+1)] # nxt[i][j] s[i:] 第一个字母j的位置
nxt[n] = [-1]*k
for i in range(n-1, -1, -1):
    nxt[i] = nxt[i+1].copy()
    nxt[i][ s[i] ] = i


######################################
f = [0]*(n+1)
f[n] = 1
for i in range(n-1, -1, -1):
    best = float('inf')
    for c in range(k):
        j = nxt[i][c]
        if j == -1:
            # c 在 s[i:] 全都没出现，单加 c 就能保证不匹配
            best = 1
            break
        else:
            # 跳到 j+1 继续看后缀
            best = min(best, 1 + f[j+1])
    f[i] = best

######################################
f = [0]*n + [1]
for i in range(n-1, -1, -1):
    tmp = inf
    for j in range(k):
        j = nxt[i][j] # 考虑当前 i/s[i] 的下一个j

        print([(j, f[j] + 1) for j in range(k)])

        if j == -1:
            f[i] = 1
            break
        else:
            tmp = mn(tmp, f[j] + 1)
    f[i] = tmp
    print(s[i:])
    print(f[i:])
    print()
print(s)

q = RI()
queries = []
for _ in range(q):
    queries.append([ord(c) - ord("a") for c in RS()])

# t在s中出现的最早子序列 下表最低子序列

for t in queries:
    pos = 0
    for c in t:  # 利用算好的nxt跳转数组遍历s
        j = nxt[pos][c]
        if j == -1:
            print(0)
            break
        pos = j + 1           # 下一轮从 j+1 开始匹配
    else:
        # 整个 t 完全匹配，跳到 pos，剩下后缀最短不匹配长度就是 f[pos]
        print(f[pos])