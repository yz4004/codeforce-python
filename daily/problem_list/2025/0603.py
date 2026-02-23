"""
https://codeforces.com/problemset/problem/1994/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) x(1≤x≤1e9) 和长为 n 的数组 a(1≤a[i]≤1e9)。

对于 a 的一个连续非空子数组 b，执行如下过程：
初始化 s = 0。
从左到右遍历 b：
1. 把 s 增加 b[i]。
2. 如果增加后 s > x，则把 s 重置为 0；否则 s 不变。
3. 继续遍历下一个数。

如果遍历结束后 s > 0，则称 b 为好子数组。
输出 a 中有多少个好子数组。

"""
from collections import defaultdict
from functools import cache
from math import comb, factorial
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(n,t, nums):
    # [i,j]
    j = n-1
    s = 0
    f = [0]*(n+1)
    for i in range(n-1, -1, -1):
        s += nums[i]
        while s > t:
            s -= nums[j]
            j -= 1
        # [i,j] j+1 j+2
        if j < i:
            f[i] = f[i+1]
        if i <= j:
            f[i] = (j - i + 1) + (f[j+2] if j+2 < n else 0)
    return sum(f)

T = RI()
for _ in range(T):
    n,x = RII()
    nums = RILIST()
    print(solve(n,x, nums))



