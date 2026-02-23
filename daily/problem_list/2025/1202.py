"""
https://www.luogu.com.cn/problem/P5322

输入 s(1≤s≤100) n(1≤n≤100) m(1≤m≤2e4)。
然后输入 s 个长度都为 n 的非负整数数组 a[1],a[2],...,a[n]，每个 a[i] 都满足 sum(a[i]) <= m。

你需要构造一个长为 n 的非负整数数组 b，满足 sum(b) <= m。
然后遍历 a[i][j]，如果 b[j] > a[i][j] * 2，那么得到 j 分。

输出你的最大总得分。

注：O(snm) 可过。

"""
import itertools
import sys
from bisect import bisect_left
from collections import defaultdict
from functools import cache
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

row_n, n, m = RII()
a = []
for _ in range(row_n):
    a.append(RILIST())
    # sum(a) < m
# b[j] > a[i][j] * 2 -- i

ta = []
for j in range(n):
    col = []
    for i in range(row_n):
        if a[i][j] * 2 > m: continue
        col.append(a[i][j] * 2)
    col.sort()
    ta.append(col)

# j] - s
# @cache
# def dfs(j, s):
#     if j == n:
#         return 0
#
#     res = 0
#     col = ta[j]
#     score = 0
#     earn = j+1
#     for i in range(row_n):
#         cost = col[i]
#         if cost + 1 > s:
#             break
#         score += earn
#
#         tmp = dfs(j+1, s-(cost+1))
#         if tmp + score > res:
#             res = tmp + score
#     return res
# print(dfs(0, m))

# f[j][s] 前j个用分数s
# f[s] first j column. with score cap to s
f = [0] * (m + 1)
g = [0] * (m + 1)
for j in range(1, n + 1):

    col = ta[j - 1]
    for s in range(1, m + 1):

        gs = f[s]
        for p in range(len(col)):
            cur = col[p] + 1
            if cur > s: break
            gs = mx(gs, f[s - cur] + (p + 1) * j)  # s-cur 随着j增大减小

        # f[j][s] 在第j列的背包 相当于多个物品 0/1 背包 - 对每个物品选或不选
        # 不是完全背包在这里可以选择平行的多个物品，选一个可以从这一行前面的位置转移
        # 这里物品尺寸为填入分数 一旦设定 这行不能再选其他，而收益是小于分数的aij数量 * j

        # f[s] = max(f[s-col[p]-1] + (p+1)*j for all p)
        g[s] = gs
    f, g = g, f

print(max(f))





