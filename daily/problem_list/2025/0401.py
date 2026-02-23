"""
https://codeforces.com/problemset/problem/1492/C

输入 n m(2≤m≤n≤2e5)，长为 n 的字符串 s，长为 m 的字符串 t，只包含小写英文字母。
保证 t 是 s 的子序列。

设 s 中的一个等于 t 的子序列的下标为 p1,p2,...,pm。
定义其宽度为 max(p[i+1] - p[i])。

输出 s 中所有等于 t 的子序列中的最大宽度。

变形：求最小宽度。


"""
import sys
from math import inf
from collections import defaultdict
from bisect import  bisect_left

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, m = RII()
s = RS()
t = RS()

# 前后缀分解
suf = []



# # f[i][j] s[:i] t[:j] max width
# f = [[0]*(m+1) for _ in range(n+1)]
# pre = [[inf]*(m+1) for _ in range(n+1)]
#
# for i in range(1, n+1):
#     for j in range(1, m+1):
#         f[i][j] = f[i-1][j]
#         # s[i-1] == t[j-1]
#         if s[i-1] == t[j-1]:
#             if pre[i][j] == inf:
#                 pre[i][j] = i-1
#             cur = max(f[i-1][j-1], i-1 - pre[i-1][j-1]) # 查询 s[:i] 往前一个等于 t[j-1] 的位置，第一次f[i-1][j-1]得到更新的位置
#             f[i][j] = max(f[i][j], cur)
#             print(i,j, cur)
#     print(s[:i])
#     print(t)
#     print(f)
#     print(pre)
#     print()
# print(f[n][m])


# f = [0]*(m+1)
# g = [0]*(m+1)
# r = {}
# for x in s:
#     for i in range(m):
#         g[i] = f[i]
#         if x == t[i]:
#             g[]

