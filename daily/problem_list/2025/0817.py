"""
https://codeforces.com/problemset/problem/2112/C

输入 T(≤1e3) 表示 T 组数据。所有数据的 n 之和 ≤5e3。
每组数据输入 n(3≤n≤5e3) 和长为 n 的递增数组 a(1≤a[i]≤1e5)。

一开始有 n 个无色球，第 i 个球上的数字为 a[i]。
Alice 选 3 个球涂成红色，然后 Bob 选 1 个球（可以是红色）涂成蓝色。
注：上述过程只执行一轮。

要求无论 Bob 怎么操作，都有红色球元素和 > 蓝色球的元素值。
问：Alice 有多少种不同的涂色方案。即涂成红色的下标三元组 (i,j,k) 的数量，其中 i<j<k。
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, nums = RI(), RILIST()

    # a1 a2 a3  > m
    # a1 a2     > a3

    # 5000

    # a1+a2 > max(m-a3, a3)
    nums.sort()
    res = 0
    m = nums[-1]
    for k in range(2, n):
        t = mx(nums[k], m-nums[k])
        # [:k] > t
        # 对向双指针，每次都能唯一的决定应该移动i/j 指针

        l, r = 0, k-1
        cur = 0
        while l < r:
            if nums[l] + nums[r] <= t:
                l += 1
            else:
                cur += r-l
                r -= 1
        res += cur
    print(res )


