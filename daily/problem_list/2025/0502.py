"""
https://codeforces.com/problemset/problem/543/C

输入 n m(1≤n,m≤20) 和长为 n 的字符串数组 s，长度均为 m，只包含小写英文字母。
输入 n 行 m 列的矩阵 cost，元素范围 [0,1e6]。

对于字符串 s[i] 来说，如果存在一个 j，满足 s[i][j] 与第 j 列的其他字母都不一样，那么称 s[i] 是容易记忆的。
你可以修改 s[i][j] 为任意小写英文字母，花费为 cost[i][j]。

把这 n 个字符串都变成容易记忆的，最小总花费是多少？

4 3
abc
aba
adc
ada
10 10 10
10 1 10
10 10 10
10 1 10
输出 2

- 20 * 2^20
"""
import sys
from math import inf
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

m, n = RII()
val = []
for _ in range(m):
    s = RS()
    val.append([ord(c) - ord("a") for c in s])
mat = [RILIST() for _ in range(m)]


f = [inf]*(1<<m) # f[s] set s is covered - min cost
f[0] = 0
# f[-1] = sum(min(row) for row in mat)
mn_c = [min(row) for row in mat]

for j, col in enumerate(zip(*val)):
    # column j, (i,c)
    mp = [0]*26
    group_cost = [0]*26
    group_max  = [0]*26
    for i in range(m):
        c = val[i][j]
        mp[c] |= 1<<i
        group_cost[c] += mat[i][j]
        group_max[c] = mx(group_max[c], mat[i][j])

    # mp[c] 只需要提供除了最大值以外的值的和
    col_trans = []
    for c in range(26):
        t = mp[c]
        if t:
            col_trans.append((t, group_cost[c]-group_max[c]))

    # for i in range(m):
    #     if mat[i][j] == mn_c[i]:
    #         for s in range(0, 1<<m):
    #             f[s | (1<<i)] = mn(f[s | (1<<i)], f[s] + mn_c[i])
    for i in range(m):
        if mat[i][j] == mn_c[i]:
            col_trans.append((1<<i, mn_c[i]))

    # t - 要枚举的相同字母集合
    # for t, c in col_trans:
    #     for s in range(0, 1<<m):
    #         f[s | t] = mn(f[s | t], f[s] + c)

    for s in range(0, 1<<m):
        base = f[s]
        for t, c in col_trans:
            f[s | t] = mn(f[s | t], base + c)
print(f[(1<<m)-1])
