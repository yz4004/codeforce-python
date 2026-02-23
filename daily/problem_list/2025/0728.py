"""
https://codeforces.com/problemset/problem/1987/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤1e5。
每组数据输入 n(1≤n≤1e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。

下标从 0 开始。
每一秒，我们从左到右遍历数组 a，遍历到 a[i] 时，如果 i=n-1 或者 a[i]>a[i+1]，那么把 a[i] 变成 max(a[i]-1, 0)。
把所有 a[i] 都变成 0，需要多少秒？（或者说需要遍历 a 多少次）


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
    f = 0
    for i in range(n-1, -1, -1):
        f = mx(nums[i], f+1)
    print(f)
