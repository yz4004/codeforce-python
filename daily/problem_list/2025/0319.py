"""
https://codeforces.com/problemset/problem/446/A

输入 n(1≤n≤1e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。

你可以修改 a 中的至多一个数（修改成任意整数）。
输出 a 的最长严格递增子数组的长度。
注：子数组是连续的。

进阶：如果可以改 2 个数呢？改 k 个数呢？

- 在当前i  把前一个数改到 [i]-1 最有可能创造最长的以i结尾的子数组
    （前一个大于i则这么改，即使前面小于i 也可能是 【103】 改成 【123】
- 如果扩展到修改k个，则考虑前面修改j个 则呈现阶梯下降，[i-j, i-1] [i]
    关注 i-j-1 能否小于 [i]-j
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

RI()
nums = RILIST()
n = len(nums)
# f0, f1 = 1, -inf

f = [[0, 0] for _ in range(n)] # f[i][0/1]
f[0] = [1,1]
res = 1
for i in range(1, n):
    # 不修改 vs 修改 i-1
    if nums[i-1] < nums[i]:
        f[i][0] = f[i-1][0] + 1
        f[i][1] = max(f[i-1][1] + 1, (f[i-2][0] + 2) if i-2>=0 and nums[i]-nums[i-2]>1 else 2)
    else:
        f[i][0] = 1
        f[i][1] = (f[i-2][0] + 2) if i-2>=0 and nums[i]-nums[i-2]>1 else 2
    res = max(res, f[i][1], f[i][0], f[i-1][0] + 1)
print(res)

