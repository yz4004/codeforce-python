"""
https://atcoder.jp/contests/abc373/tasks/abc373_f

输入 n(1≤n≤3000) m(1≤m≤3000) 表示有 n 种物品，以及一个容量为 m 的背包。
然后输入 n 行，每行输入第 i 种物品的体积 w(1≤w≤m) 和价值 v(1≤v≤1e9)。

每种物品都有无限个。
为了避免选择过多相同类型的物品，有如下规定：
如果同一种物品选了 k 个，那么这 k 个物品的实际总价值不是 k*v，而是 k*v - k^2。

输出所选物品的价值总和的最大值。物品的体积之和不能超过 m。

"""
import itertools
import sys
from math import inf, isqrt
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, m = RII()
# weight = RILIST()
# value = RILIST()
weight = [0]*n
value = [0]*n
for i in range(n):
    w,v = RII()
    weight[i], value[i] = w, v
print(weight)
print(value)

# f = [[0]*(m+1) for _ in range(n + 1)]
# for i in range(1, n + 1):
#     for j in range(1, m + 1):
#         w, v = weight[i-1], value[i-1]
#         f[i][j] = f[i-1][j]
#         for t in range(1, (j-1)//w+2):
#             f[i][j] = mx(f[i][j], f[i-1][j-t*w] + t*v - t*t)
# print(f[n][m])

f = [[0]*(m+1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        w, v = weight[i-1], value[i-1]
        f[i][j] = f[i-1][j]
        # for t in range(1, (j-1)//w+2):
        #     f[i][j] = mx(f[i][j], f[i-1][j-t*w] + t*v - t*t)

        # t*v - t*t
        # v - 2*t
        # t = v/2
        u = min(v, (j-1)//w+1) # [0, u]

print(f[n][m])

def backpack(weight, value):
    f = [[0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            f[i][j] = f[i-1][j]
            if weight[i-1] <= j:
                f[i][j] = mx(f[i][j], f[i][j-weight[i-1]] + value[i-1])
    print(f[n][m])

    f = [0]*(m+1)
    for i in range(1, n+1):
        # for j in range(m, 0, -1):
        #     if weight[i-1] <= j:
        #         f[j] = mx(f[j], f[j-weight[i-1]] + value[i-1])
        for j in range(1, m+1):
            if weight[i-1] <= j:
                f[j] = mx(f[j], f[j-weight[i-1]] + value[i-1])
        print(f)
    print(f[m])