"""
https://codeforces.com/problemset/problem/2098/B

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤1e5。
每组数据输入 n(1≤n≤1e5) k(0≤k<n) 和长为 n 的数组 a(1≤a[i]≤1e9)。

一条街道（坐标轴）上有 n 个酒吧，第 i 个酒吧的位置为 a[i]。
你可以移除至多 k 个酒吧。

这条街道的房子整齐排列，位置为 1,2,3,...,1e9。
定义 f(x) 表示位置为 x 的房子到所有剩余酒吧的距离之和。
对于位置为 i 的房子，如果存在一种移除酒吧的方案，可以让 f(i) = min(f(x))，则称 i 为好房子。
输出好房子的个数。

- 中位数贪心，移除不超过k个房子后的中位数段是被覆盖的好房子
- 所以考虑移除最左 最右k个是覆盖的最远范围
- [l,r] 的中位数 m-l = r-m => m = (l+r)//2
    n=4 0123 下中位数 (n-1)//2 上 n//2
    n=5 01234 中位数 (n-1)//2 = n//2
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, k = RII()
    nums = RILIST()

    # 对于nums，移除k个元素后会创造出中间区域，求最大覆盖
    nums.sort()

    m = n-k
    right = nums[k + m//2]
    left = nums[(m-1)//2]
    print(right - left + 1)


