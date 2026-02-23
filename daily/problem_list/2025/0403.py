"""
https://codeforces.com/problemset/problem/1175/D

输入 n k(1≤k≤n≤3e5) 和长为 n 的数组 a(-1e6≤a[i]≤1e6)。

把 a 分割成恰好 k 个非空连续子数组。
设 S = 第一个子数组的元素和乘以 1 + 第二个子数组的元素和乘以 2 + ... + 第 k 个子数组的元素和乘以 k。
输出 S 的最大值。

"""
import itertools
import sys
from math import inf
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, k = RII()
nums = RILIST()
nums = nums[::-1]
ps = list(itertools.accumulate(nums, initial=0))
f = [[-inf]*(n+1) for _ in range(k+1)]
f[0][0] = 0
print(nums)
for i in range(1, k+1):
    tmp = -inf
    for j in range(1, n+1):
        tmp = mx(tmp, f[i-1][j-1] - ps[j-1] * (k-i+1))
        f[i][j] = tmp + ps[j] * (k-i+1)

        # (xj, yj) = (ps[j-1], f[i-1][j-1])
        # A = k-i+1
        # yj - xj * A
        # xj，yj - 无单调，A递减，但是仍然维持上凸包？
    # print(f[i])


print(f[k][n])

for i in range(1, k+1):
    tmp = -inf
    for j in range(1, n+1):
        # f[i][j] = f[i][j-1] + nums[j-1] * (k-i+1)
        # for l in range(0,j):
        #     # [0,l) [l, i)
        #     f[i][j] = mx(f[i][j], f[i-1][l] + (ps[j] - ps[l]) * (k-i+1))

        # tmp = max(f[i-1][l] + (ps[j] - ps[l]) * (k-i+1) for l in range(j))
        # tmp = max(f[i-1][l] - ps[l] * (k-i) for l in range(j)) + ps[j] * (k-i+1)
        tmp = mx(tmp, f[i-1][j-1] - ps[j-1] * (k-i+1))
        f[i][j] = tmp + ps[j] * (k-i+1)
print(f[k][n])




nums = nums[::-1]
ps = list(itertools.accumulate(nums, initial=0))


# ps = list(itertools.accumulate(nums, initial=0))
# f = [[-inf]*(n+1) for _ in range(k+1)]
# f[0][0] = 0
# for i in range(1, k+1):
#     for j in range(1, n+1):
#         f[i][j] = f[i][j-1] + nums[j-1] * i
#         for l in range(0,j):
#             # [0,l) [l, i)
#             f[i][j] = mx(f[i][j], f[i-1][l] + (ps[j] - ps[l]) * i)
#         # f[i][j] = max(f[i-1][l] + (ps[j] - ps[l]) * i for l in range(j))

# for i in range(1, k + 1):
#     tmp = 0
#     for j in range(1, n + 1):
#         # f[i][j] = f[i][j - 1] + nums[j - 1] * i
#         # for l in range(0, j):
#         #     # [0,l) [l, i)
#         #     f[i][j] = mx(f[i][j], f[i - 1][l] + (ps[j] - ps[l]) * i)
#         # f[i][j] = max(f[i-1][l] + (ps[j] - ps[l]) * i for l in range(j))
#         # tmp = max(f[i-1][l] - ps[l] * i for l in range(j)) + ps[j] * i
#         tmp = max(tmp, f[i-1][j-1] - ps[j-1] * i)
#         f[i][j] = max(tmp + ps[j] * i, f[i][j - 1] + nums[j - 1] * i)
# print(f[k][n])



# f = [[-inf]*(n+1) for _ in range(k+1)]
# f[0][0] = 0
# for i in range(1, k + 1):
#     tmp = 0
#     for j in range(1, n + 1):
#         tmp = max(tmp, f[i-1][j-1] - ps[j-1] * i)
#         f[i][j] = max(tmp + ps[j] * i, f[i][j - 1] + nums[j - 1] * i)
#     # (xj,yj) = (ps[j-1], f[i-1][j-1])
#     # A = i
#     # yj - xj * A 的最大值  xj没有递增规律（负数）, A递增
#     # 维护上凸包 不行，因为ps[j-1] 不递增

# f = [[-inf]*(n+1) for _ in range(k+1)]
# f[0][0] = 0
# for i in range(1, k + 1):
#     tmp = 0
#     for j in range(1, n + 1):
#         tmp = max(tmp, f[i-1][j-1] - ps[j-1] * i)
#         f[i][j] = max(tmp + ps[j] * i, f[i][j - 1] + nums[j - 1] * i)
    # (xj,yj) = (ps[j-1], f[i-1][j-1])
    # A = i
    # yj - xj * A 的最大值  xj没有递增规律（负数）, A递增
    # 维护上凸包 不行，因为ps[j-1] 不递增

f = [[-inf]*(n+1) for _ in range(k+1)]
f[0][0] = 0
for i in range(1, k + 1):
    tmp = 0
    for j in range(1, n + 1):
        tmp = max(tmp, f[i-1][j-1] - ps[j-1] * i)
        f[i][j] = max(tmp + ps[j] * i, f[i][j - 1] + nums[j - 1] * i)
print(f[k][n])
