"""
https://www.luogu.com.cn/problem/P2513

输入 n(1≤n≤1000) k(0≤k≤1000)。
输出有多少个 1~n 的排列，满足逆序对数恰好等于 k。
答案模 10000

https://www.luogu.com.cn/record/216249630
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, k = RII()
f = [0]*(k+1)
f[0] = 1

g = [0]*(k+1)
g[0] = 1

for i in range(1, n+1):
    for j in range(1, k+1):
        # f[i][j] = sum(f[i-1][t] for t in range(max(0, j-i+1),j+1)) # 至多提供i-1个逆序对

        if j-i < 0:
            g[j] = g[j - 1] + f[j]
        else:
            g[j] = g[j - 1] + f[j] - f[j - i]
    f, g = g, f
print(f[k] % 10000)


# f[i][j] 前i个 有恰好j个逆序对
# f[i][j]  = f[i-1][j-x] 前i个内部凑j-x的方案 + 第i个填入元素t 引入了x个方案
# f = [0]*(k+1)
# f[0] = 1

# n, k = RII()
# f = [[0]*(k+1) for _ in range(n+1)]
# f[0][0] = 1
# for i in range(1, n+1):
#     f[i][0] = 1
#     for j in range(1, k+1):
#         # for t in range(n):
#         # for t in range(i):
#         #f[i][j] = sum(f[i-1][t] for t in range(max(0, j-i+1),j+1)) # 至多提供i-1个逆序对
#
#         if j-i < 0:
#             f[i][j] = f[i][j - 1] + f[i - 1][j]
#         else:
#             f[i][j] = f[i][j - 1] + f[i - 1][j] - f[i - 1][j - i]
#
# print(f[n][k])