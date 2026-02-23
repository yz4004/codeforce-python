"""
https://atcoder.jp/contests/abc360/tasks/abc360_g

输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。

你可以修改 a 中恰好一个数（修改成任意整数）。
输出 a 的最长严格递增子序列（LIS）的长度。
注：子序列不一定连续。

进阶：如果可以改 2 个数呢？改 k 个数呢？改连续 k 个数呢？

- 对比0319连续子数组，考虑以[i]结尾的LIS, 不修改时 f[i] 代表长为i的lis的最小结尾值
- 引入k次修改，可以定义 f[k][i] 代表长为i 再经过k次修改后的最小结尾值
"""
import sys
from bisect import  bisect_left

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

RI()
nums = RILIST()
n = len(nums)
k = 1



# LIS
# f = []
# for x in nums:
#     i = bisect_left(f, x) # 第一个大于x的，长度同为i的情况下可以替换为x
#     if i == len(f):
#         f.append(x)
#     else:
#         f[i] = x
# print(len(f))
# 原版lis，现在可以修改一个元素，可以把x变最大，然后append在后面 扩展长度

f0 = []
f1 = []
for x in nums:

    # 不修改x 则对f1正常讨论
    i = bisect_left(f1, x)
    if i == len(f1):
        f1.append(x)
    else:
        f1[i] = x

    # 修改x 则
    # print(f1, f0, x)
    j = len(f0)
    w = f0[j-1] if j > 0 else -1
    if j < len(f1):
        f1[j] = min(f1[j], w+1)
    else:
        f1.append(w+1)

    i = bisect_left(f0, x)  # 第一个大于x的，长度同为i的情况下可以替换为x
    if i == len(f0):
        f0.append(x)
    else:
        f0[i] = x
print(len(f1))

    # f0 不修改的lis

    # print(f1, f0)
    # print()








# for j in range(1, k+1):
#     fi = []
#     for x in nums:







