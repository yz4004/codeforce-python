"""
https://atcoder.jp/contests/abc346/tasks/abc346_d

输入 n(2≤n≤2e5)，长为 n 的 01 字符串 s，长为 n 的数组 a(1≤a[i]≤1e9)。

修改 s，使其中【恰好】包含一对相邻相同字符。
例如 10010 是符合要求的，11001 是不符合要求的（有两对相邻相同字符 11 和 00）。

修改 s[i] 的代价是 a[i]。
输出最小总代价。

进阶：把一对改成两对，K 对，要怎么做？
"""
import sys, itertools
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n = RI()
s = RS()
a = RILIST()

f = [[[inf]*2 for _ in range(2)] for _ in range(n)] # f[i][0/1][0/1] 前i个元素 结尾元素是0/1 无成对/有恰好一对
c = int(s[0])
f[0][c][0] = 0
f[0][c^1][0] = a[0]

# print("0:", f[0][0])
# print("1:", f[0][1])

# f[0][0] = [0, inf]
# f[0][1] = [0, inf]
# for i, (c, v) in enumerate(zip(s, a), 1):
for i in range(1, n):
    c, v = s[i], a[i]

    c = int(c)
    f[i][c][0] = f[i-1][c^1][0] # 以c结尾，没有成对
    f[i][c][1] = min(f[i-1][c^1][1], f[i-1][c][0])
    # 以c为结尾 恰好一对
    # 前面也是以c结尾，没有修改 f[i-1][c][0] - cc
    # 更早的前面已经成对，前面保持 c^1

    f[i][c^1][0] = f[i-1][c][0] + v  # 以c^1 没有成对
    f[i][c^1][1] = min(f[i-1][c][1] + v, f[i-1][c^1][0] + v)
    # 以c^1 恰好一对
    # 前面也是以c^1结尾，有修改 f[i-1][c^1][0] - c^1 c^1
    # 更早的前面已经成对，前面保持 c

#     print(i, v, s[:i+1])
#     print("0:", f[i][0])
#     print("1:", f[i][1])
#     print()
#
# print(f)
print(min(f[n-1][i][1] for i in range(2)))






